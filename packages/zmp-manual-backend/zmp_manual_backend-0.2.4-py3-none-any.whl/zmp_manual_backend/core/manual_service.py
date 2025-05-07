import asyncio
import logging
import os
import re
import shutil
import uuid
import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union, Any, NamedTuple

import git
from dotenv import load_dotenv
import aiofiles
import pickle

from zmp_manual_backend.models.manual import (
    Manual,
    Folder,
    Notification,
    NotificationSourceType,
    NotificationStatus,
    PublishStatus,
    SolutionType,
    JobState,
    FailureReason,
    NodeModel,
)
from zmp_notion_exporter import NotionPageExporter
from zmp_notion_exporter.utility import transform_block_id_to_uuidv4, validate_page_id
from zmp_notion_exporter.node import Node
from zmp_md_translator import MarkdownTranslator
from zmp_md_translator.settings import Settings

# Load environment variables
load_dotenv()

logger = logging.getLogger("appLogger")

# Define NotificationClient type
NotificationClient = NamedTuple(
    "NotificationClient", [("queue", asyncio.Queue), ("user_id", Optional[str])]
)


class ManualService:
    def __init__(
        self,
        notion_token: str,
        root_page_id: str,
        repo_path: str = "./repo",
        source_dir: str = "docs",
        target_dir: str = "i18n",
        github_repo_url: Optional[str] = None,
        github_branch: Optional[str] = "develop",
        target_languages: Optional[Set[str]] = None,
        cache_path: str = "./cache",
        openai_api_key: Optional[str] = None,
        openai_model: Optional[str] = None,
        max_chunk_size: Optional[str] = None,
        max_concurrent_requests: Optional[str] = None,
    ):
        """Initialize the manual service.

        Args:
            notion_token: The Notion API token
            root_page_id: The root page ID for the manual
            repo_path: Path to the repository
            source_dir: Source directory for the manual
            target_dir: Target directory for translations
            github_repo_url: URL of the GitHub repository
            github_branch: Branch to use in the repository
            target_languages: Set of target languages for translation
            cache_path: Path to the cache directory
            openai_api_key: OpenAI API key for translation
            openai_model: OpenAI model to use for translation
            max_chunk_size: Maximum chunk size for translation
            max_concurrent_requests: Maximum number of concurrent translation requests
        """
        self.notion_token = notion_token
        self.repo_path = Path(repo_path)
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.github_repo_url = github_repo_url
        self.github_branch = github_branch
        self.target_languages = target_languages or {"ko"}
        self.cache_path = Path(cache_path)
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        self.max_chunk_size = max_chunk_size
        self.max_concurrent_requests = max_concurrent_requests
        self.initialized = False

        # Initialize solution-specific root page IDs
        self.root_page_ids = {}
        if isinstance(root_page_id, dict):
            self.root_page_ids.update(root_page_id)
        else:
            # For backward compatibility, use the single root_page_id for ZCP
            self.root_page_ids[SolutionType.ZCP] = root_page_id

        # Initialize exporters dictionary
        self.exporters: Dict[SolutionType, Optional[NotionPageExporter]] = {
            SolutionType.ZCP: None,
            SolutionType.APIM: None,
            SolutionType.AMDP: None,
        }

        # Initialize caches
        self.manuals_cache: Dict[SolutionType, List[Union[Manual, Folder]]] = {}
        self.cache_last_updated: Dict[SolutionType, datetime] = {}
        self.docs_nodes: Dict[SolutionType, Node] = {}
        self.static_nodes: Dict[SolutionType, Node] = {}

        # Initialize cache directory structure
        self.manuals_cache_dir = (
            self.cache_path / "manuals"
        )  # For node information JSON files
        self.manuals_cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize notification system
        self.notification_clients: Dict[str, NotificationClient] = {}
        self.notifications: List[Notification] = []
        self.max_notifications = 1000

        # Initialize job tracking
        self.active_jobs: Dict[str, PublishStatus] = {}

        # Initialize settings
        self.settings = {
            "repo_path": str(self.repo_path),
            "source_dir": self.source_dir,
            "target_dir": self.target_dir,
            "github_repo_url": self.github_repo_url,
            "github_branch": self.github_branch,
            "target_languages": list(self.target_languages),
            "cache_path": str(self.cache_path),
            "notion_token": self.notion_token,
            "root_page_ids": self.root_page_ids,
            "openai_api_key": self.openai_api_key,
            "openai_model": self.openai_model,
            "max_chunk_size": self.max_chunk_size,
            "max_concurrent_requests": self.max_concurrent_requests,
        }

        # Initialize cache directory structure
        self.manuals_cache_dir = (
            self.cache_path / "manuals"
        )  # For node information JSON files

        # Create necessary directories
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.manuals_cache_dir.mkdir(parents=True, exist_ok=True)

        # Create base directories for each solution
        for solution_type in SolutionType:
            # Create docs directory structure
            docs_dir = self.repo_path / self.source_dir / solution_type.value.lower()
            docs_dir.mkdir(parents=True, exist_ok=True)

            # Create static/img directory structure
            img_dir = self.repo_path / "static" / "img" / solution_type.value.lower()
            img_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initialized directory structure at {self.repo_path}")

        # Initialize exporters for each solution
        self.exporters = {}
        self.root_page_ids = {}
        self.docs_nodes = {}  # Store docs nodes for each solution
        self.static_nodes = {}  # Store static nodes for each solution

        # First try to get solution-specific root page IDs from environment variables
        for solution_type in SolutionType:
            env_var = f"{solution_type.value.upper()}_ROOT_PAGE_ID"
            solution_root_id = os.environ.get(env_var)
            if solution_root_id:
                try:
                    formatted_id = self._format_page_id(solution_root_id)
                    self.root_page_ids[solution_type] = formatted_id
                    # Initialize exporter for this solution
                    self.exporters[solution_type] = NotionPageExporter(
                        notion_token=self.notion_token,
                        root_page_id=formatted_id,
                        root_output_dir=str(
                            self.cache_path
                        ),  # Use cache_path as root, exporter will create docs/{solution}
                    )

                    logger.info(f"Initialized exporter for {solution_type.value}")
                except ValueError as e:
                    logger.error(
                        f"Invalid root page ID for {solution_type.value}: {str(e)}"
                    )

        # Initialize static content exporter if configured
        static_root_id = os.environ.get("STATIC_ROOT_PAGE_ID")
        if static_root_id:
            try:
                formatted_id = self._format_page_id(static_root_id)
                self.static_exporter = NotionPageExporter(
                    notion_token=self.notion_token,
                    root_page_id=formatted_id,
                    root_output_dir=str(
                        self.cache_path
                    ),  # Use cache_path as root, exporter will create static/img/{solution}
                )
                logger.info("Initialized static content exporter")
            except ValueError as e:
                logger.error(f"Invalid static root page ID: {str(e)}")
                self.static_exporter = None
        else:
            self.static_exporter = None

        # Initialize caches
        self.manuals_cache = {}  # For node information
        self.cache_last_updated = {}
        self.active_jobs = {}
        self.notifications = []
        self.notification_clients = {}

        # Store the original repo path as a class variable
        self.original_repo_path = repo_path

    def _create_translation_progress_callback(self, job_id: str):
        """Create a progress callback for the translator.

        Args:
            job_id: ID of the job to track progress for

        Returns:
            An async function that can be used as a translation progress callback
        """
        if job_id not in self.active_jobs:
            logger.error(
                f"Job {job_id} not found when creating translation progress callback"
            )
            return

        job_status = self.active_jobs[job_id]
        solution_value = job_status.solution  # Store the solution value

        # Variables to track translation progress
        file_count = 0
        total_files = 0
        current_file = ""
        current_lang = ""

        async def translation_progress_callback(progress):
            """Callback for translation progress updates.

            Args:
                progress: Either a value between 0.0 and 1.0 indicating translation progress
                        or a TranslationProgress object with more details
            """
            if job_id not in self.active_jobs:
                logger.warning(
                    f"Job {job_id} not found during translation progress update"
                )
                return

            try:
                nonlocal file_count, total_files, current_file, current_lang

                # Handle different types of progress objects
                percentage = 0.0

                # Check for TranslationProgress by class name
                if str(type(progress).__name__) == "TranslationProgress":
                    # It's a TranslationProgress object from zmp_md_translator
                    # Log the object attributes for debugging
                    logger.debug(
                        f"Received TranslationProgress object with attributes: {dir(progress)}"
                    )

                    # Extract attributes safely
                    if hasattr(progress, "current"):
                        file_count = progress.current
                    if hasattr(progress, "total"):
                        total_files = progress.total
                    if hasattr(progress, "current_file"):
                        current_file = progress.current_file

                    # Extract language from current_file if possible
                    if current_file and "[" in current_file and "]" in current_file:
                        lang_match = re.search(r"\[([a-z]{2})\]", current_file)
                        if lang_match:
                            current_lang = lang_match.group(1)

                    # Extract status and message if available
                    status = getattr(progress, "status", None)
                    message = getattr(progress, "message", None)

                    if status:
                        logger.info(f"Translation status: {status}")

                    if message:
                        logger.info(f"Translation message: {message}")

                    # Calculate percentage from current and total
                    if total_files > 0:  # Avoid division by zero
                        percentage = file_count / total_files

                    # Log successful object processing
                    logger.info(
                        f"Processed TranslationProgress: {percentage:.1%}, file {file_count}/{total_files}, current: {current_file}, lang: {current_lang}"
                    )
                elif isinstance(progress, (float, int)) or isinstance(progress, str):
                    # It's a simple numeric type or string that can be converted
                    percentage = float(progress)
                else:
                    # Log the type for debugging
                    logger.warning(
                        f"Unknown progress type: {type(progress)}, using default 0.0"
                    )
                    # Try to extract percentage attribute if it exists
                    if hasattr(progress, "percentage"):
                        try:
                            percentage = (
                                float(progress.percentage)
                                if progress.percentage is not None
                                else 0.0
                            )
                        except (TypeError, ValueError):
                            percentage = 0.0
                    elif (
                        hasattr(progress, "current")
                        and hasattr(progress, "total")
                        and getattr(progress, "total", 0) > 0
                    ):
                        # Try to calculate percentage from current and total
                        try:
                            percentage = float(progress.current) / float(progress.total)
                        except (TypeError, ValueError, ZeroDivisionError):
                            percentage = 0.0
                            logger.error(
                                "Failed to calculate percentage from current/total values"
                            )
                    else:
                        # As a last resort, try to convert the whole object to float
                        try:
                            percentage = float(progress)
                        except (TypeError, ValueError):
                            percentage = 0.0
                            logger.error(
                                f"Failed to extract percentage from progress object: {progress}"
                            )
                            import traceback

                            logger.error(traceback.format_exc())

                # Convert to percentage (0-100 scale)
                percentage_display = percentage * 100

                # Update status with progress - round to 1 decimal place
                self.active_jobs[job_id].translation_progress = round(
                    percentage_display, 1
                )

                # Translation is the second half of the process (50-100%)
                total_progress = 50.0 + (percentage_display * 0.5)
                self.active_jobs[job_id].total_progress = round(total_progress, 1)

                # Make sure solution field is preserved
                if solution_value and not self.active_jobs[job_id].solution:
                    self.active_jobs[job_id].solution = solution_value

                # Format the message properly with file information if available
                if current_file:
                    # For specific file translation (e.g. "5.7%(12/210) - user-guide/development-tools.mdx [zh]")
                    file_display = current_file
                    lang_display = f" [{current_lang}]" if current_lang else ""
                    formatted_message = f"{percentage_display:.1f}%({file_count}/{total_files}) - {file_display}{lang_display}"
                else:
                    # For general progress (e.g. "0.0%(0/210) - Translating pages")
                    formatted_message = f"{percentage_display:.1f}%({file_count}/{total_files}) - Translating pages"

                self.active_jobs[job_id].message = formatted_message

                # Log significant progress points
                logger.info(
                    f"Translation progress for job {job_id}: {percentage:.1%} complete, "
                    f"total progress: {total_progress:.1f}, solution={solution_value}"
                )
            except Exception as e:
                logger.error(f"Error in translation progress callback: {str(e)}")
                # Add traceback for better debugging
                import traceback

                logger.error(traceback.format_exc())

        return translation_progress_callback

    def _format_page_id(self, page_id: str) -> str:
        """Format page ID to match Notion's expected format.

        Args:
            page_id: The page ID to format

        Returns:
            str: Formatted page ID in UUID format

        Raises:
            ValueError: If the page ID is invalid
        """
        try:
            # First transform to UUID format
            formatted_id = transform_block_id_to_uuidv4(page_id)

            # Validate the format
            if not validate_page_id(formatted_id):
                raise ValueError(f"Invalid page ID format: {page_id}")

            return formatted_id
        except Exception as e:
            logger.error(f"Error formatting page ID {page_id}: {str(e)}")
            raise ValueError(f"Invalid page ID: {page_id}")

    async def get_manuals(
        self,
        selected_solution: SolutionType = SolutionType.ZCP,
    ) -> List[Union[Manual, Folder]]:
        """Retrieve the manual list from Notion and organize it into a tree structure.

        Args:
            exporter: The exporter instance to use
            selected_solution: The solution type selected by the user in the frontend (defaults to ZCP)

        Returns:
            List[Union[Manual, Folder]]: A hierarchical list of manuals and folders

        Raises:
            ValueError: If the root page ID is invalid or not configured
        """
        try:
            # Check if we have cached data in memory for this solution
            if selected_solution in self.manuals_cache:
                logger.info(
                    f"Using in-memory cached manuals data for {selected_solution.value}"
                )
                return self.manuals_cache[selected_solution]

            # Check if we have cached data in the filesystem
            cache_loaded = await self._load_tree_cache_from_file(selected_solution)
            if cache_loaded and selected_solution in self.manuals_cache:
                logger.info(
                    f"Using file-cached manuals data for {selected_solution.value}"
                )
                return self.manuals_cache[selected_solution]

            # If not in memory or filesystem cache, fetch from Notion
            logger.info(
                f"Cache miss for {selected_solution.value}, fetching from Notion"
            )

            # Get the root page ID for the selected solution
            root_page_id = self.root_page_ids.get(selected_solution)
            if not root_page_id:
                error_msg = f"No root page ID configured for solution {selected_solution.value}. Check environment variables."
                logger.error(error_msg)
                logger.error(f"Available solutions: {list(self.root_page_ids.keys())}")
                logger.error(
                    f"Environment variable {selected_solution.value.upper()}_ROOT_PAGE_ID is not set"
                )
                raise ValueError(error_msg)

            # Format and validate the root page ID
            try:
                formatted_root_id = self._format_page_id(root_page_id)
            except ValueError as e:
                error_msg = f"Invalid root page ID for solution {selected_solution.value}: {str(e)}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Clean up old files before export
            try:
                await self._cleanup_old_files(selected_solution)

                logger.info("Cleaned up old files before export")
            except Exception as e:
                logger.error(
                    f"Failed to clean up old files: {str(e)}"
                )  # Reset repo path to original
                self.repo_path = self.original_repo_path
                raise e

            # Get the exporter for this solution type
            exporter = self.exporters.get(selected_solution)
            if not exporter:
                error_msg = f"No exporter found for solution {selected_solution.value}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            logger.info(
                f"Using root page ID for {selected_solution.value}: {formatted_root_id}"
            )

            # Get all nodes from the exporter
            # Run the synchronous get_tree_nodes method in a thread pool to avoid blocking
            try:
                # Use a thread pool to run the synchronous get_tree_nodes method
                # This prevents blocking the event loop for other requests
                nodes = await asyncio.to_thread(exporter.get_tree_nodes)

                if not nodes:
                    error_msg = f"No nodes returned for page ID: {formatted_root_id}"
                    logger.error(error_msg)
                    return []
                logger.info(f"Retrieved {len(nodes)} nodes from Notion")

                # Store in memory cache
                self.manuals_cache[selected_solution] = nodes
                self.cache_last_updated[selected_solution] = datetime.now()
                logger.info(f"Updated in-memory cache for {selected_solution.value}")

                # Also save to filesystem cache
                await self._save_cache_to_file(selected_solution)

                return nodes
            except Exception as e:
                error_msg = f"Error getting tree nodes: {str(e)}"
                logger.error(error_msg)
                return []

        except Exception as e:
            logger.error(f"Error retrieving manuals from Notion: {str(e)}")
            return []

    async def publish_manual(
        self,
        notion_page_id: str,
        selected_solution: Union[SolutionType, str],
        target_languages: Optional[Set[str]] = None,
        user_id: Optional[str] = None,
        job_id: Optional[str] = None,
        title: Optional[str] = None,
        is_directory: Optional[bool] = None,
        parent_id: Optional[str] = None,
    ) -> str:
        """Publish a manual by exporting it from Notion and translating it.

        Args:
            notion_page_id: The Notion page ID of the selected node to publish
            selected_solution: The solution type (ZCP/APIM/AMDP)
            target_languages: Optional set of target languages for translation
            user_id: Optional user ID to associate with notifications
            job_id: Optional job ID to use (if one was already created)
            title: Optional title of the page to be published
            is_directory: Optional flag indicating if the page is a directory
            parent_id: Optional parent page ID in the hierarchy

        Returns:
            str: The job ID for tracking the publication progress

        Raises:
            ValueError: If the notion_page_id is invalid
        """
        # Get the job ID if it already exists in active_jobs
        # We process previously queued jobs first

        if target_languages:
            self.target_languages = target_languages

        # Convert string to SolutionType if needed
        if isinstance(selected_solution, str):
            try:
                selected_solution = SolutionType(selected_solution.lower())
            except ValueError:
                # Handle invalid solution type
                if not job_id:
                    job_id = str(uuid.uuid4())

                self.active_jobs[job_id] = PublishStatus(
                    job_id=job_id,
                    notion_page_id=notion_page_id,
                    status=JobState.FAILED,
                    message=f"Invalid solution type: {selected_solution}",
                    failure_reason=FailureReason.EXPORT_FAILED,
                )

                # Create notification for failure
                if user_id:
                    notification = Notification(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        title="Manual Publication Failed",
                        message=f"Invalid solution type: {selected_solution}",
                        status=NotificationStatus.ERROR,
                        created_at=datetime.now(),
                        job_id=job_id,
                        notification_type=NotificationSourceType.JOB_RESULT,
                    )
                    asyncio.create_task(self.add_notification(notification))
                    logger.info(f"Created failure notification for job {job_id}")

                return job_id

        # If no job_id was provided, check active jobs or create new one
        if not job_id:
            # Find the job ID from the active jobs
            # This allows us to continue a job that was created in the background tasks
            for jid, job in self.active_jobs.items():
                # Check for jobs that were just queued and are waiting to be processed
                if (
                    job.status == JobState.STARTED
                    and job.notion_page_id == notion_page_id
                ):
                    job_id = jid
                    break
                # Also continue any job that matches this request and is still in progress
                elif (
                    job.notion_page_id == notion_page_id
                    and job.solution == selected_solution.value
                    and job.status not in [JobState.COMPLETED, JobState.FAILED]
                ):
                    job_id = jid
                    break

            # If no job found, create a new one
            if not job_id:
                job_id = str(uuid.uuid4())
                self.active_jobs[job_id] = PublishStatus(
                    job_id=job_id,
                    notion_page_id=notion_page_id,
                    solution=selected_solution.value,
                    status=JobState.STARTED,
                    message="Starting publication process",
                    progress=0.0,
                    initiated_by=user_id,  # Track which user initiated this job
                    title=title,  # Store title
                    is_directory=is_directory,  # Store is_directory flag
                    parent_id=parent_id,  # Store parent_id
                )
        else:
            # Make sure the job exists and is properly initialized
            if job_id not in self.active_jobs:
                self.active_jobs[job_id] = PublishStatus(
                    job_id=job_id,
                    notion_page_id=notion_page_id,
                    solution=selected_solution.value,
                    status=JobState.STARTED,
                    message="Starting publication process",
                    progress=0.0,
                    initiated_by=user_id,  # Track which user initiated this job
                    title=title,  # Store title
                    is_directory=is_directory,  # Store is_directory flag
                    parent_id=parent_id,  # Store parent_id
                )
            elif not self.active_jobs[job_id].notion_page_id:
                # Update the job with appropriate details if not already set
                self.active_jobs[job_id].notion_page_id = notion_page_id
                self.active_jobs[job_id].solution = selected_solution.value

                # Store additional fields
                if title is not None:
                    self.active_jobs[job_id].title = title
                if is_directory is not None:
                    self.active_jobs[job_id].is_directory = is_directory
                if parent_id is not None:
                    self.active_jobs[job_id].parent_id = parent_id

                # Also ensure the user ID is set
                if (
                    not hasattr(self.active_jobs[job_id], "initiated_by")
                    or not self.active_jobs[job_id].initiated_by
                ):
                    self.active_jobs[job_id].initiated_by = user_id

        # Store a job context for use in callbacks
        self._current_job_context = {"job_id": job_id}

        try:
            # Create a job-specific repository path
            job_repo_path = os.path.join(self.original_repo_path, job_id)

            # Update the repo path for this job
            self.repo_path = Path(job_repo_path).absolute()

            # Log the updated path and branch
            logger.info(f"Created job-specific repository path: {self.repo_path}")
            logger.info(f"Using GitHub branch for job: {self.github_branch}")

            # Make sure the job directory exists - or clean it if it already exists
            if os.path.exists(job_repo_path):
                logger.info(f"Cleaning existing job repository at {job_repo_path}")
                try:
                    # Remove the directory and recreate it for a clean start
                    shutil.rmtree(job_repo_path)
                except Exception as e:
                    logger.warning(f"Failed to clean existing job repository: {str(e)}")

            # # Create a fresh directory
            # os.makedirs(job_repo_path, exist_ok=True)

            # Format the notion page ID
            formatted_page_id = self._format_page_id(notion_page_id)
            notion_page_id = formatted_page_id
            # Check and prepare repository
            self.active_jobs[job_id].status = JobState.CHECKING_REPO
            self.active_jobs[job_id].message = "Checking repository status"

            if not await self._ensure_repository():
                # Repository check failed
                self.repo_path = self.original_repo_path
                return job_id

            # Clean up old files before export
            try:
                await self._cleanup_old_files(selected_solution)

                logger.info("Cleaned up old files before export")
            except Exception as e:
                logger.error(f"Failed to clean up old files: {str(e)}")
                self.active_jobs[job_id].status = JobState.FAILED
                self.active_jobs[job_id].failure_reason = FailureReason.EXPORT_FAILED
                self.active_jobs[job_id].message = "Failed to clean up old files"
                # Reset repo path to original
                self.repo_path = self.original_repo_path
                return job_id

            # Export from Notion
            self.active_jobs[job_id].status = JobState.EXPORTING
            self.active_jobs[job_id].message = "Initializing export from Notion..."
            self.active_jobs[job_id].export_progress = 0.0

            # Log callback creation for consistency with export callback
            logger.info(f"Creating export progress callback for job: {job_id}")

            # Get the solution value
            solution_value = (
                selected_solution.value
                if isinstance(selected_solution, SolutionType)
                else selected_solution
            )

            # Export the content
            export_success, export_path, mdx_files = await self.export_repository(
                notion_page_id=notion_page_id,
                output_dir=os.path.join(self.repo_path, self.source_dir),
                selected_solution=SolutionType(solution_value.lower()),
                job_id=job_id,
                is_directory=is_directory,
            )

            # If export failed, mark job as failed and return
            if not export_success or not export_path:
                self.active_jobs[job_id].status = JobState.FAILED
                self.active_jobs[job_id].failure_reason = FailureReason.EXPORT_FAILED
                self.active_jobs[job_id].message = "Export from Notion failed"

                # Create notification for failure
                if hasattr(self, "_current_job_context"):
                    solution_value = (
                        selected_solution.value
                        if hasattr(selected_solution, "value")
                        else selected_solution
                    )
                    notification = Notification(
                        id=str(uuid.uuid4()),
                        user_id=self._current_job_context.get("user_id"),
                        title="Manual Export Failed",
                        message=f"The manual for '{solution_value}' could not be exported from Notion.",
                        status=NotificationStatus.ERROR,
                        created_at=datetime.now(),
                        job_id=job_id,
                        solution=selected_solution,
                        notification_type=NotificationSourceType.JOB_RESULT,
                    )
                    asyncio.create_task(self.add_notification(notification))
                    logger.info(f"Created failure notification for job {job_id}")

                # Reset repo path to original
                self.repo_path = self.original_repo_path
                return job_id

            # Update status with file count
            self.active_jobs[job_id].message = f"Exported {mdx_files} MDX files"
            self.active_jobs[job_id].export_files = mdx_files
            self.active_jobs[job_id].export_progress = 100.0
            self.active_jobs[job_id].total_progress = 50.0  # Export is first 50%

            # Copy original docs from main repository to job-specific repository
            main_repo_base = os.path.join(
                self.original_repo_path, self.source_dir, solution_value.lower()
            )
            job_docs_base = os.path.join(
                self.repo_path, self.source_dir, solution_value.lower()
            )
            if os.path.exists(main_repo_base):
                shutil.copytree(main_repo_base, job_docs_base, dirs_exist_ok=True)
                logger.info(
                    f"Copied docs from main repository {main_repo_base} to job repository {job_docs_base}"
                )

            # Commit export changes
            if not await self._commit_export_changes(
                f"Export manual content for solution {solution_value}"
            ):
                self.active_jobs[job_id].status = JobState.FAILED
                self.active_jobs[job_id].failure_reason = FailureReason.GIT_ERROR
                self.active_jobs[job_id].message = "Failed to commit export changes"
                # Reset repo path to original
                self.repo_path = self.original_repo_path
                return job_id

            # # Clean up any existing translations under i18n before translating
            # await self._cleanup_i18n_content(
            #     selected_solution,
            #     dir_name="",  # directory cleanup wipes the 'current' folder
            #     is_directory=True,
            # )
            # logger.info(f"Cleaned up existing i18n content for solution {solution_value} before translation")

            # Get the source path to translate (path to the specific manual being published)
            source_path = os.path.join(
                self.repo_path, self.source_dir, selected_solution.value.lower()
            )

            # Ensure all required images are available for translation
            await self._ensure_images_for_translations(
                selected_solution=selected_solution,
                target_languages=target_languages or self.target_languages,
            )

            # Translate the content
            self.active_jobs[job_id].status = JobState.TRANSLATING
            self.active_jobs[job_id].message = "Starting translation..."
            self.active_jobs[job_id].translation_progress = 0.0

            logger.info(f"Starting translation from {source_path}")

            # Log callback creation for consistency with export callback
            logger.info(f"Creating translation progress callback for job: {job_id}")

            # Translate the manual
            try:
                export_path_str = str(export_path)
                # Convert the export_path to use the job-specific path
                job_specific_source_path = os.path.join(
                    self.repo_path,
                    os.path.relpath(export_path_str, os.path.dirname(self.repo_path)),
                )
                translation_success = await self.translate_repository(
                    source_path=job_specific_source_path,
                    target_dir=self.target_dir,
                    target_languages=target_languages or self.target_languages,
                    selected_solution=selected_solution.value,
                    job_id=job_id,
                )

                if translation_success:
                    # Push changes to GitHub repository
                    self.active_jobs[job_id].status = JobState.PUSHING
                    self.active_jobs[
                        job_id
                    ].message = "Pushing changes to GitHub repository..."

                    # Call the _push_changes method to push to GitHub
                    push_success = await self._push_changes()

                    if push_success:
                        # Update job status to completed
                        self.active_jobs[job_id].status = JobState.COMPLETED
                        self.active_jobs[
                            job_id
                        ].message = "Manual published successfully and pushed to GitHub"
                        self.active_jobs[job_id].total_progress = 100.0
                        self.active_jobs[job_id].translation_progress = 100.0

                        # Create notification for successful completion
                        if user_id:
                            solution_value = (
                                selected_solution.value
                                if hasattr(selected_solution, "value")
                                else selected_solution
                            )
                            notification = Notification(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                title="Manual Publication Complete",
                                message=f"The manual for '{solution_value}' has been published successfully and pushed to GitHub.",
                                status=NotificationStatus.SUCCESS,
                                created_at=datetime.now(),
                                job_id=job_id,
                                solution=selected_solution,
                                notification_type=NotificationSourceType.JOB_RESULT,
                            )
                            await self.add_notification(notification)
                            logger.info(
                                f"Created success notification for job {job_id}"
                            )

                        # Log completion and ensure clients are updated
                        logger.info(f"Job {job_id} completed successfully")
                    else:
                        # Update job status to failed
                        self.active_jobs[job_id].status = JobState.FAILED
                        self.active_jobs[
                            job_id
                        ].message = "Failed to push changes to GitHub"
                        self.active_jobs[
                            job_id
                        ].failure_reason = FailureReason.GIT_OPERATION_FAILED

                        # Create notification for failure
                        if user_id:
                            solution_value = (
                                selected_solution.value
                                if hasattr(selected_solution, "value")
                                else selected_solution
                            )
                            notification = Notification(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                title="Manual Publication Failed",
                                message=f"The manual for '{solution_value}' could not be pushed to GitHub.",
                                status=NotificationStatus.ERROR,
                                created_at=datetime.now(),
                                job_id=job_id,
                                solution=selected_solution,
                                notification_type=NotificationSourceType.JOB_RESULT,
                            )
                            await self.add_notification(notification)
                            logger.info(
                                f"Created failure notification for job {job_id}"
                            )
            except Exception as e:
                logger.error(f"Error during translation: {str(e)}")
                self.active_jobs[job_id].status = JobState.FAILED
                self.active_jobs[
                    job_id
                ].failure_reason = FailureReason.TRANSLATION_FAILED
                self.active_jobs[job_id].message = f"Translation failed: {str(e)}"

                # Create notification for failure
                if user_id:
                    solution_value = (
                        selected_solution.value
                        if hasattr(selected_solution, "value")
                        else selected_solution
                    )
                    notification = Notification(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        title="Manual Translation Failed",
                        message=f"The manual for '{solution_value}' could not be translated: {str(e)}",
                        status=NotificationStatus.ERROR,
                        created_at=datetime.now(),
                        job_id=job_id,
                        solution=selected_solution,
                        notification_type=NotificationSourceType.JOB_RESULT,
                    )
                    asyncio.create_task(self.add_notification(notification))
                    logger.info(f"Created failure notification for job {job_id}")

        except Exception as e:
            logger.error(f"Error during publication process: {str(e)}")
            self.active_jobs[job_id].status = JobState.FAILED
            self.active_jobs[job_id].message = f"Publication failed: {str(e)}"
            self.active_jobs[job_id].failure_reason = FailureReason.UNKNOWN

            # Create notification for failure
            if user_id:
                solution_value = (
                    selected_solution.value
                    if hasattr(selected_solution, "value")
                    else selected_solution
                )
                notification = Notification(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    title="Manual Publication Failed",
                    message=f"The manual for '{solution_value}' could not be published: {str(e)}",
                    status=NotificationStatus.ERROR,
                    created_at=datetime.now(),
                    job_id=job_id,
                    solution=selected_solution,
                    notification_type=NotificationSourceType.JOB_RESULT,
                )
                asyncio.create_task(self.add_notification(notification))
                logger.info(f"Created failure notification for job {job_id}")

        finally:
            # Always reset repo path to original
            self.repo_path = self.original_repo_path
            logger.info(
                f"Reset repository path from {self.repo_path} to {self.original_repo_path}"
            )

            # Clean up job context
            if hasattr(self, "_current_job_context"):
                delattr(self, "_current_job_context")

        return job_id

    async def get_job_status(self, job_id: str) -> Optional[PublishStatus]:
        """Get the status of a publishing job.

        Args:
            job_id: The ID of the job to check

        Returns:
            Optional[PublishStatus]: The job status if found, None otherwise
        """
        return self.active_jobs.get(job_id)

    async def _cleanup_i18n_content(
        self, selected_solution: SolutionType, dir_name: str, is_directory: bool
    ) -> None:
        """Clean up i18n content for all target languages.

        Args:
            selected_solution: The solution type being processed
            dir_name: The name of the directory/file to clean
            is_directory: Whether this is a directory cleanup (True) or file cleanup (False)
        """
        for lang in self.target_languages:
            # Construct the base i18n path
            i18n_base = os.path.join(
                self.repo_path,
                self.target_dir,
                lang,
                f"docusaurus-plugin-content-docs-{selected_solution.value.lower()}",
            )

            # Create the directory structure if it doesn't exist
            i18n_current = os.path.join(i18n_base, "current")
            os.makedirs(i18n_current, exist_ok=True)
            logger.info(f"Ensuring i18n directory structure exists: {i18n_current}")

            if self.initialized:
                # Use the find_and_remove_content approach
                self._find_and_remove_i18n_content(i18n_current, dir_name, is_directory)
            else:
                # Use the delete_i18n_content approach
                self._delete_i18n_content(i18n_current, dir_name)

    def _delete_i18n_content(self, i18n_current: str, dir_name: str) -> None:
        """Delete i18n content for a given directory.

        Args:
            i18n_current: The path to the i18n current directory
            dir_name: The name of the directory to delete
        """
        # Delete the i18n directory
        shutil.rmtree(i18n_current)
        os.makedirs(i18n_current, exist_ok=True)
        logger.info(f"Deleted i18n directory: {i18n_current}")

    def _find_and_remove_i18n_content(
        self, base_dir: str, dir_name: str, is_directory: bool
    ) -> None:
        """Find and remove content within the i18n directory.

        Args:
            base_dir: The base directory to search in
            dir_name: The name of the directory/file to find and remove
            is_directory: Whether this is a directory (True) or file (False)
        """
        # Walk through the directory tree
        for root, dirs, files in os.walk(base_dir, topdown=False):
            # Check for matching directory
            if is_directory:
                # Get the current directory name from the path
                current_dir = os.path.basename(root)
                if current_dir == dir_name:  # Compare with the target directory name
                    target_path = root
                    logger.info(f"Found matching i18n directory: {target_path}")
                    try:
                        shutil.rmtree(target_path)
                        logger.info(
                            f"Removed i18n directory and contents: {target_path}"
                        )
                        # Recreate empty directory
                        os.makedirs(target_path, exist_ok=True)
                        logger.info(f"Recreated empty i18n directory: {target_path}")
                    except Exception as e:
                        logger.error(
                            f"Error removing i18n directory {target_path}: {str(e)}"
                        )
            else:
                # Check for matching file (with or without .mdx extension)
                base_name = os.path.splitext(dir_name)[
                    0
                ]  # Get filename without extension

                # Create possible filename variants to match
                possible_filenames = [
                    dir_name,  # Original name (could already have extension)
                    f"{base_name}.mdx",  # With .mdx extension
                ]

                matching_files = [f for f in files if f in possible_filenames]
                for file in matching_files:
                    target_path = os.path.join(root, file)
                    logger.info(f"Found matching i18n file: {target_path}")
                    try:
                        os.remove(target_path)
                        logger.info(f"Removed i18n file: {target_path}")
                    except Exception as e:
                        logger.error(
                            f"Error removing i18n file {target_path}: {str(e)}"
                        )

    async def _cleanup_old_files(self, selected_solution: SolutionType) -> None:
        """Clean up old files before export.

        Args:
            selected_solution: The solution type being processed
        """
        try:
            if self.initialized:
                if not hasattr(
                    self, "_current_job_context"
                ) or not self._current_job_context.get("job_id"):
                    logger.warning("No job context found, skipping cleanup")
                    return

                job_id = self._current_job_context["job_id"]
                if job_id not in self.active_jobs:
                    logger.warning(
                        f"Job {job_id} not found in active jobs, skipping cleanup"
                    )
                    return

                job = self.active_jobs[job_id]
                notion_page_id = job.notion_page_id
                is_directory = job.is_directory
                title = job.title

                if not notion_page_id or not title:
                    logger.warning(
                        "Missing notion_page_id or title in job, skipping cleanup"
                    )
                    return

                # Log cleanup parameters
                logger.info(
                    f"Starting cleanup for: notion_page_id={notion_page_id}, title={title}, is_directory={is_directory}"
                )
                # Convert title to directory/file name format and handle special characters
                dir_name = title.lower()
                special_chars = {
                    "/": "-",
                    "\\": "-",
                    ":": "-",
                    "*": "",
                    "?": "",
                    '"': "",
                    "<": "",
                    ">": "",
                    "|": "-",
                    ".": "-",
                    " ": "-",
                }
                for char, replacement in special_chars.items():
                    dir_name = dir_name.replace(char, replacement)
                dir_name = re.sub(r"-+", "-", dir_name).strip("-")
                logger.info(
                    f"Looking for directory/file with name after cleanup: {dir_name}"
                )
            else:
                is_directory = True
                logger.info(
                    f"Starting cleanup for: {selected_solution} in startup mode"
                )
                dir_name = selected_solution.value.lower()

            # Define base paths to clean for docs and static/img
            base_paths = [
                os.path.join(
                    self.repo_path, self.source_dir, selected_solution.value.lower()
                ),
                os.path.join(
                    self.repo_path, "static", "img", selected_solution.value.lower()
                ),
            ]

            def find_and_remove_content(base_dir: str):
                if not os.path.exists(base_dir):
                    logger.info(f"Directory does not exist, skipping: {base_dir}")
                    return
                found_matching = False
                # Walk through the directory tree
                for root, dirs, files in os.walk(base_dir, topdown=False):
                    # Check for matching directory
                    if is_directory:
                        # Get the current directory name from the path
                        current_dir = os.path.basename(root)
                        if (
                            current_dir == dir_name
                        ):  # Compare with the target directory name
                            target_path = root
                            logger.info(f"Found matching directory: {target_path}")
                            try:
                                shutil.rmtree(target_path)
                                logger.info(
                                    f"Removed directory and contents: {target_path}"
                                )
                                found_matching = True
                                # Recreate empty directory
                                os.makedirs(target_path, exist_ok=True)
                                logger.info(f"Recreated empty directory: {target_path}")
                                break
                            except Exception as e:
                                logger.error(
                                    f"Error removing directory {target_path}: {str(e)}"
                                )
                    else:
                        # Check for matching file (with or without .mdx extension)
                        base_name = os.path.splitext(dir_name)[
                            0
                        ]  # Get filename without extension

                        # Create possible filename variants to match
                        possible_filenames = [
                            dir_name,  # Original name (could already have extension)
                            f"{base_name}.mdx",  # With .mdx extension
                        ]

                        matching_files = [f for f in files if f in possible_filenames]
                        for file in matching_files:
                            target_path = os.path.join(root, file)
                            logger.info(f"Found matching file: {target_path}")
                            try:
                                os.remove(target_path)
                                logger.info(f"Removed file: {target_path}")
                                found_matching = True
                                break
                            except Exception as e:
                                logger.error(
                                    f"Error removing file {target_path}: {str(e)}"
                                )
                        if found_matching:
                            break

            # Clean up docs and static/img directories
            for base_path in base_paths:
                logger.info(f"Searching in base path: {base_path}")
                await asyncio.to_thread(find_and_remove_content, base_path)

            # Clean up i18n directories separately
            await self._cleanup_i18n_content(selected_solution, dir_name, is_directory)

            logger.info(
                f"Cleanup completed for {dir_name} (is_directory={is_directory})"
            )

        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise

    async def _ensure_repository(self) -> bool:
        """Ensure repository exists and is up to date.
        Returns True if successful, False otherwise."""
        try:
            repo_path = Path(self.repo_path)
            is_job_specific = False

            # Check if this is a job-specific repository
            if hasattr(self, "_current_job_context") and self._current_job_context.get(
                "job_id"
            ):
                job_id = self._current_job_context["job_id"]
                if job_id in self.active_jobs:
                    is_job_specific = True
                    logger.info(
                        f"Setting up job-specific repository for job {job_id} at {repo_path}"
                    )
                    logger.info(f"Using branch: {self.github_branch}")

            should_clone = False

            # Check available disk space before cloning
            try:
                total, used, free = shutil.disk_usage(str(repo_path.parent))
                free_mb = free // (1024 * 1024)  # Convert to MB

                # Log the available space
                logger.info(f"Available disk space: {free_mb}MB")

                # Check if we have at least 500MB free (adjust threshold as needed)
                if free_mb < 500:
                    logger.error(f"Insufficient disk space: only {free_mb}MB available")
                    if hasattr(self, "_current_job_context"):
                        job_id = self._current_job_context["job_id"]
                        if job_id in self.active_jobs:
                            self.active_jobs[job_id].status = JobState.FAILED
                            self.active_jobs[
                                job_id
                            ].failure_reason = FailureReason.REPO_ACCESS
                            self.active_jobs[
                                job_id
                            ].message = (
                                f"Insufficient disk space: only {free_mb}MB available"
                            )
                    return False
            except Exception as e:
                logger.warning(f"Failed to check disk space: {str(e)}")
                # Continue with the operation, but log the warning

            # For job-specific repositories, always do a fresh clone to ensure clean state
            if is_job_specific:
                should_clone = True
                if repo_path.exists():
                    logger.info(f"Removing existing job repository at {repo_path}")
                    await asyncio.to_thread(shutil.rmtree, repo_path)
            else:
                # Function to check if a directory is a valid git repository
                def is_valid_git_repo(path):
                    try:
                        git.Repo(path)
                        return True
                    except git.exc.InvalidGitRepositoryError:
                        return False

                # Check if directory exists and is not empty
                if not repo_path.exists():
                    should_clone = True
                else:
                    # Check if directory is empty
                    if not any(repo_path.iterdir()):
                        should_clone = True
                    else:
                        # Check if it's a valid git repository (potentially blocking operation)
                        try:
                            is_valid = await asyncio.to_thread(
                                is_valid_git_repo, repo_path
                            )
                            if not is_valid:
                                should_clone = True
                        except Exception:
                            should_clone = True

            if should_clone:
                # Update job status for cloning
                if hasattr(self, "_current_job_context"):
                    job_id = self._current_job_context["job_id"]
                    if job_id in self.active_jobs:
                        current_job = self.active_jobs[job_id]
                        # Create a dictionary of current values excluding the ones we want to update
                        current_values = current_job.model_dump()
                        current_values.update(
                            {
                                "status": JobState.CLONING,
                                "message": f"Cloning repository from {self.github_repo_url} (branch: {self.github_branch})",
                            }
                        )
                        updated_job = PublishStatus(**current_values)
                        self.active_jobs[job_id] = updated_job

                logger.info(
                    f"Cloning repository from {self.github_repo_url} with branch {self.github_branch}"
                )

                # Remove directory if it exists but is empty or not a valid repo
                if repo_path.exists():
                    await asyncio.to_thread(shutil.rmtree, repo_path)

                # Use GitHub token from environment if available
                github_token = os.environ.get("GITHUB_TOKEN")
                repo_url = self.github_repo_url

                if not github_token:
                    logger.error("No GitHub token found in environment variables")
                    if hasattr(self, "_current_job_context"):
                        job_id = self._current_job_context["job_id"]
                        if job_id in self.active_jobs:
                            self.active_jobs[job_id].status = JobState.FAILED
                            self.active_jobs[
                                job_id
                            ].failure_reason = FailureReason.REPO_ACCESS
                            self.active_jobs[
                                job_id
                            ].message = (
                                "GitHub token not found in environment variables"
                            )
                    return False

                # Modify URL to include token
                if "https://github.com" in repo_url:
                    # Replace https://github.com with https://oauth2:TOKEN@github.com
                    repo_url = repo_url.replace(
                        "https://github.com",
                        f"https://oauth2:{github_token}@github.com",
                    )
                    logger.info(
                        "Using GitHub token from environment variables for authentication"
                    )
                else:
                    logger.warning(f"Unexpected GitHub URL format: {repo_url}")

                # Configure the git environment
                git_env = {
                    "GIT_TERMINAL_PROMPT": "0",  # Disable interactive prompts
                    "GIT_ASKPASS": "echo",  # Simple askpass handler
                }

                # Clone the repository
                try:
                    logger.info(
                        f"Cloning repository {self.github_repo_url} with branch {self.github_branch}"
                    )

                    # Clone with token authentication and specific branch
                    await asyncio.to_thread(
                        git.Repo.clone_from,
                        repo_url,
                        repo_path,
                        env=git_env,
                        branch=self.github_branch,  # Explicitly specify the branch
                    )
                    logger.info(
                        f"Successfully cloned repository branch {self.github_branch}"
                    )

                    # Verify we're on the correct branch
                    repo = git.Repo(repo_path)
                    current_branch = repo.active_branch.name
                    logger.info(f"After clone: current branch is {current_branch}")

                    if current_branch != self.github_branch:
                        logger.warning(
                            f"Branch mismatch after clone. Expected: {self.github_branch}, Got: {current_branch}"
                        )
                        # Explicitly checkout the correct branch
                        logger.info(f"Checking out {self.github_branch} branch")
                        repo.git.checkout(self.github_branch)
                        logger.info(f"Now on branch: {repo.active_branch.name}")

                except Exception as e:
                    logger.error(f"Failed to clone repository: {str(e)}")
                    if hasattr(self, "_current_job_context"):
                        job_id = self._current_job_context["job_id"]
                        if job_id in self.active_jobs:
                            self.active_jobs[job_id].status = JobState.FAILED
                            self.active_jobs[
                                job_id
                            ].failure_reason = FailureReason.REPO_ACCESS
                            self.active_jobs[
                                job_id
                            ].message = f"Failed to clone repository: {str(e)}"
                    return False

                # Create necessary working directories
                work_dirs = [
                    os.path.join(self.repo_path, self.source_dir),
                    os.path.join(self.repo_path, self.target_dir),
                ]

                # Create directories in a non-blocking way
                for directory in work_dirs:
                    if not os.path.exists(directory):
                        await asyncio.to_thread(os.makedirs, directory, exist_ok=True)
                        logger.info(f"Created working directory: {directory}")

                return True

            # If we don't need to clone, update existing repository
            # Update job status for pulling
            if hasattr(self, "_current_job_context"):
                job_id = self._current_job_context["job_id"]
                if job_id in self.active_jobs:
                    current_job = self.active_jobs[job_id]
                    # Create a dictionary of current values excluding the ones we want to update
                    current_values = current_job.model_dump()
                    current_values.update(
                        {
                            "status": JobState.PULLING,
                            "message": f"Updating repository (git pull from {self.github_branch})",
                        }
                    )
                    updated_job = PublishStatus(**current_values)
                    self.active_jobs[job_id] = updated_job

            logger.info(f"Repository exists, checking {self.github_branch} branch")

            # Function to update the repository
            def update_repo():
                try:
                    # Use GitHub token from environment for authentication
                    github_token = os.environ.get("GITHUB_TOKEN")
                    if not github_token:
                        logger.error("GitHub token not found in environment variables")
                        raise ValueError(
                            "GitHub token not found in environment variables"
                        )

                    logger.info("Using GitHub token from environment variables")

                    # Initialize the repository
                    repo = git.Repo(repo_path)

                    # Configure Git to use the token for this operation
                    with repo.git.custom_environment(
                        GIT_ASKPASS="echo",
                        GIT_USERNAME="oauth2",
                        GIT_PASSWORD=github_token,
                    ):
                        origin = repo.remotes.origin
                        # Fetch all branches first (required for proper reference handling)
                        logger.info("Fetching branches")
                        origin.fetch()

                    # Check if the configured branch exists in remote
                    remote_refs = [ref.name for ref in repo.refs]
                    remote_branch_exists = f"origin/{self.github_branch}" in remote_refs
                    logger.info(
                        f"Checking if branch '{self.github_branch}' exists on remote. Result: {remote_branch_exists}"
                    )

                    # If remote branch doesn't exist, try to create it from main/master
                    if not remote_branch_exists:
                        # Check if main or master exists in remote
                        if "origin/main" in remote_refs:
                            base_branch = "main"
                        elif "origin/master" in remote_refs:
                            base_branch = "master"
                        else:
                            logger.error(
                                f"Neither {self.github_branch}, main, nor master branch exists in remote"
                            )
                            raise ValueError("No valid base branch found in remote")

                        # Create and push the configured branch from base branch
                        logger.info(
                            f"Creating {self.github_branch} branch from {base_branch}"
                        )
                        repo.git.checkout(
                            "-b", self.github_branch, f"origin/{base_branch}"
                        )
                        repo.git.push("--set-upstream", "origin", self.github_branch)
                        remote_branch_exists = True

                    # Now handle local branch
                    if self.github_branch not in repo.heads:
                        # Create local branch tracking remote branch
                        logger.info(
                            f"Creating local {self.github_branch} branch tracking origin/{self.github_branch}"
                        )
                        branch = repo.create_head(
                            self.github_branch, f"origin/{self.github_branch}"
                        )
                        branch.set_tracking_branch(
                            getattr(origin.refs, self.github_branch)
                        )
                    else:
                        branch = repo.heads[self.github_branch]
                        # Ensure local branch is tracking remote branch
                        if (
                            not branch.tracking_branch()
                            or branch.tracking_branch().name
                            != f"origin/{self.github_branch}"
                        ):
                            branch.set_tracking_branch(
                                getattr(origin.refs, self.github_branch)
                            )

                    # Switch to branch if not already on it
                    if repo.active_branch.name != self.github_branch:
                        logger.info(f"Switching to {self.github_branch} branch")
                        branch.checkout()

                    # Log current branch for verification
                    logger.info(
                        f"Current branch after checkout: {repo.active_branch.name}"
                    )

                    # Reset local branch to match remote if they're out of sync
                    logger.info(
                        f"Synchronizing with remote {self.github_branch} branch"
                    )
                    repo.git.reset("--hard", f"origin/{self.github_branch}")

                    # Pull latest changes
                    logger.info(
                        f"Pulling latest changes from {self.github_branch} branch"
                    )
                    repo.git.pull("origin", self.github_branch)

                    return True
                except git.exc.GitCommandError as e:
                    logger.error(f"Git command failed: {str(e)}")
                    raise e

            # Run update_repo in a thread to avoid blocking
            try:
                return await asyncio.to_thread(update_repo)
            except Exception as e:
                logger.error(f"Repository operation failed: {str(e)}")
                if hasattr(self, "_current_job_context"):
                    job = self.active_jobs[self._current_job_context["job_id"]]
                    job.status = JobState.FAILED
                    job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                    job.message = f"Repository operation failed: {str(e)}"
                return False

        except Exception as e:
            logger.error(f"Repository operation failed: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.REPO_ACCESS
                job.message = f"Repository operation failed: {str(e)}"
            return False

    async def _commit_export_changes(self, message: str) -> bool:
        """Commit changes after export phase."""
        try:
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                # Store the current export_files count
                current_export_files = job.export_files
                # Update status while preserving export_files
                job.status = JobState.EXPORT_COMMIT
                job.message = (
                    f"Committing exported files (branch: {self.github_branch})"
                )
                # Restore the export_files count
                job.export_files = current_export_files

            # Define a function to perform all git operations in a thread
            def perform_git_operations():
                try:
                    repo = git.Repo(self.repo_path)

                    # Log current state for verification
                    logger.info(f"Current repository path: {self.repo_path}")
                    logger.info(
                        f"Current branch before commit: {repo.active_branch.name}"
                    )
                    logger.info(f"Target branch for commit: {self.github_branch}")

                    # Ensure we're on the configured branch
                    if repo.active_branch.name != self.github_branch:
                        logger.error(f"Not on {self.github_branch} branch")
                        # Try to checkout the branch if it exists
                        if self.github_branch in repo.heads:
                            logger.info(
                                f"Attempting to check out {self.github_branch} branch"
                            )
                            repo.heads[self.github_branch].checkout()
                            logger.info(
                                f"Successfully checked out {self.github_branch} branch"
                            )
                        else:
                            raise ValueError(
                                f"Branch {self.github_branch} does not exist locally"
                            )

                    # Double-check that we're on the correct branch
                    current_branch = repo.active_branch.name
                    if current_branch != self.github_branch:
                        logger.error(
                            f"Still not on {self.github_branch} branch after checkout attempt"
                        )
                        raise ValueError(
                            f"Could not switch to {self.github_branch} branch"
                        )
                    else:
                        logger.info(
                            f"Verified on {self.github_branch} branch for commit"
                        )

                    # Add both documentation and static files
                    logger.info(f"Adding documentation files in {self.source_dir}")
                    repo.git.add(os.path.join(self.source_dir, "*"))
                    logger.info("Adding static files")
                    repo.git.add("static")  # Add the entire static directory

                    # Check if there are any changes to commit
                    if repo.is_dirty(untracked_files=True):
                        commit = repo.index.commit(f"docs: {message}")
                        logger.info(
                            f"Committed changes to documentation and static files (hash: {commit.hexsha[:7]})"
                        )
                    else:
                        logger.info("No changes to commit in export phase")

                    return True
                except Exception as e:
                    logger.error(f"Error in git operations: {str(e)}")
                    return False

            # Run git operations in a thread pool
            return await asyncio.to_thread(perform_git_operations)

        except Exception as e:
            logger.error(f"Failed to commit export changes: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                job.message = f"Failed to commit export changes: {str(e)}"
            return False

    async def _commit_translation_changes(self, message: str) -> bool:
        """Commit changes after translation phase."""
        try:
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.TRANSLATION_COMMIT
                job.message = (
                    f"Committing translated files (branch: {self.github_branch})"
                )

            # Define a function to perform all git operations in a thread
            def perform_git_operations():
                try:
                    repo = git.Repo(self.repo_path)

                    # Log current state for verification
                    logger.info(f"Current repository path: {self.repo_path}")
                    logger.info(
                        f"Current branch before commit: {repo.active_branch.name}"
                    )
                    logger.info(f"Target branch for commit: {self.github_branch}")

                    # Ensure we're on the configured branch
                    if repo.active_branch.name != self.github_branch:
                        logger.error(f"Not on {self.github_branch} branch")
                        # Try to checkout the branch if it exists
                        if self.github_branch in repo.heads:
                            logger.info(
                                f"Attempting to check out {self.github_branch} branch"
                            )
                            repo.heads[self.github_branch].checkout()
                            logger.info(
                                f"Successfully checked out {self.github_branch} branch"
                            )
                        else:
                            raise ValueError(
                                f"Branch {self.github_branch} does not exist locally"
                            )

                    # Double-check that we're on the correct branch
                    current_branch = repo.active_branch.name
                    if current_branch != self.github_branch:
                        logger.error(
                            f"Still not on {self.github_branch} branch after checkout attempt"
                        )
                        raise ValueError(
                            f"Could not switch to {self.github_branch} branch"
                        )
                    else:
                        logger.info(
                            f"Verified on {self.github_branch} branch for commit"
                        )

                    # Add translation files
                    logger.info(f"Adding translation files in {self.target_dir}")
                    repo.git.add(os.path.join(self.target_dir, "*"))

                    # Check if there are any changes to commit
                    if repo.is_dirty(untracked_files=True):
                        commit = repo.index.commit(f"i18n: {message}")
                        logger.info(
                            f"Committed translation changes (hash: {commit.hexsha[:7]})"
                        )
                    else:
                        logger.info("No translation changes to commit")

                    return True
                except Exception as e:
                    logger.error(f"Error in git operations: {str(e)}")
                    return False

            # Run git operations in a thread pool
            return await asyncio.to_thread(perform_git_operations)

        except Exception as e:
            logger.error(f"Failed to commit translation changes: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                job.message = f"Failed to commit translation changes: {str(e)}"
            return False

    async def _push_changes(self) -> bool:
        """Push all changes to remote repository."""
        try:
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.PUSHING
                job.message = f"Pushing changes to remote repository (branch: {self.github_branch})"

            # Define a function to perform all git operations in a thread
            def perform_git_operations():
                try:
                    repo = git.Repo(self.repo_path)

                    # Log current state for debugging
                    logger.info(f"Current repo path: {self.repo_path}")
                    logger.info(f"Current branch: {repo.active_branch.name}")
                    logger.info(f"Target branch for push: {self.github_branch}")

                    # First, ensure we're on the configured branch
                    if repo.active_branch.name != self.github_branch:
                        logger.info(f"Switching to {self.github_branch} branch")
                        if self.github_branch in repo.heads:
                            repo.heads[self.github_branch].checkout()
                            logger.info(
                                f"Successfully switched to {self.github_branch} branch"
                            )
                        else:
                            logger.error(
                                f"Branch {self.github_branch} does not exist locally"
                            )
                            # Try to create the branch from origin
                            try:
                                logger.info(
                                    f"Attempting to create {self.github_branch} branch from origin"
                                )
                                # Fetch from origin to ensure we have the latest refs
                                origin = repo.remote(name="origin")
                                origin.fetch()
                                # Check if branch exists on remote
                                if f"origin/{self.github_branch}" in [
                                    ref.name for ref in repo.refs
                                ]:
                                    branch = repo.create_head(
                                        self.github_branch,
                                        f"origin/{self.github_branch}",
                                    )
                                    branch.set_tracking_branch(
                                        getattr(origin.refs, self.github_branch)
                                    )
                                    branch.checkout()
                                    logger.info(
                                        f"Created and checked out {self.github_branch} branch from origin"
                                    )
                                else:
                                    logger.error(
                                        f"Branch {self.github_branch} does not exist on origin"
                                    )
                                    return False
                            except Exception as e:
                                logger.error(
                                    f"Failed to create branch {self.github_branch}: {str(e)}"
                                )
                                return False

                    # Verify the current branch after checkout
                    current_branch = repo.active_branch.name
                    logger.info(
                        f"Verified current branch for operations: {current_branch}"
                    )

                    if current_branch != self.github_branch:
                        logger.error(
                            f"Branch mismatch! Expected to be on {self.github_branch} but found {current_branch}"
                        )
                        return False

                    # First, check for any untracked files
                    untracked_files = repo.untracked_files
                    if untracked_files:
                        logger.info(f"Found {len(untracked_files)} untracked files")
                        for file in untracked_files:
                            logger.info(f"Adding untracked file: {file}")
                            repo.git.add(file)

                    # Force add all relevant directories to ensure all changes are tracked
                    logger.info("Adding source directory files")
                    repo.git.add(os.path.join(self.source_dir, "*"), force=True)

                    logger.info("Adding target (i18n) directory files")
                    repo.git.add(os.path.join(self.target_dir, "*"), force=True)

                    logger.info("Adding static directory files")
                    # Use -A to add all files including untracked ones
                    repo.git.add("static", "-A", force=True)

                    # Check if there are changes to commit
                    diff_index = repo.index.diff(repo.head.commit)
                    unstaged = repo.index.diff(None)
                    untracked = repo.untracked_files

                    has_changes = (
                        len(diff_index) > 0 or len(unstaged) > 0 or len(untracked) > 0
                    )
                    logger.info(
                        f"Changes detected: staged={len(diff_index)}, unstaged={len(unstaged)}, untracked={len(untracked)}"
                    )

                    if has_changes:
                        # Commit all changes with a meaningful message
                        logger.info("Committing changes")
                        commit = repo.index.commit(
                            "docs: Update documentation and translations"
                        )
                        logger.info(f"Committed changes with hash: {commit.hexsha[:7]}")
                    else:
                        logger.info("No changes to commit")

                    # Always attempt to push - there might be commits that haven't been pushed yet
                    logger.info(
                        f"Pushing changes to remote repository ({current_branch} -> origin/{self.github_branch})"
                    )

                    # Set target branch
                    target_branch = self.github_branch

                    # First make sure we're up to date with remote
                    logger.info("Fetching latest changes from remote")
                    origin = repo.remote(name="origin")
                    fetch_info = origin.fetch()
                    logger.info(f"Fetch info: {fetch_info}")

                    # Try to push
                    try:
                        logger.info(
                            f"Pushing {current_branch} branch to origin/{target_branch}"
                        )
                        # Use force=True to override any conflicts
                        push_info = origin.push(
                            refspec=f"{current_branch}:{target_branch}", force=True
                        )

                        # Log push info for debugging
                        for info in push_info:
                            logger.info(f"Push result: {info.summary}")
                            if info.flags & info.ERROR:
                                logger.error(f"Push error: {info.summary}")
                                return False

                        logger.info(
                            f"Push from {current_branch} to origin/{target_branch} completed successfully"
                        )
                        return True
                    except git.exc.GitCommandError as e:
                        error_msg = str(e)
                        logger.error(f"Git command error during push: {error_msg}")

                        # Specific error handling
                        if (
                            "authentication failed" in error_msg.lower()
                            or "403" in error_msg
                        ):
                            logger.error(
                                "Git authentication failed. Please check Git credentials or SSH keys."
                            )
                            # Suggest creating a credential helper or using SSH
                            logger.info(
                                "Try using SSH keys or git credential helper for authentication"
                            )
                        elif (
                            "rejected" in error_msg.lower()
                            and "non-fast-forward" in error_msg.lower()
                        ):
                            logger.error(
                                "Remote rejected non-fast-forward push. Try pulling latest changes first."
                            )

                        return False
                except Exception as e:
                    logger.error(f"Unexpected error during git operations: {str(e)}")
                    return False

            # Run git operations in a thread pool
            return await asyncio.to_thread(perform_git_operations)

        except Exception as e:
            logger.error(f"Failed to push changes: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                job.message = f"Failed to push changes: {str(e)}"
            return False

    def _create_export_progress_callback(self, job_id: str):
        """Create a progress callback for the exporter.

        Args:
            job_id: ID of the job to track

        Returns:
            Function that can be passed to the exporter as progress_callback
        """
        # Ensure the job status exists
        if job_id not in self.active_jobs:
            logger.error(
                f"Job {job_id} not found when creating export progress callback"
            )
            return lambda current, total, message=None: None

        job_status = self.active_jobs[job_id]
        solution_value = job_status.solution  # Store the solution value

        def progress_callback(current: int, total: int, message: str = None):
            """Progress callback for the exporter.

            Args:
                current: Current progress value
                total: Total progress value
                message: Optional message
            """
            if job_id not in self.active_jobs:
                logger.warning(f"Job {job_id} not found during export progress update")
                return

            try:
                # Calculate progress percentage
                percentage = min(1.0, current / max(1, total)) if total > 0 else 0.0
                percentage_display = percentage * 100

                # Update job status with calculated values - round to 1 decimal place
                self.active_jobs[job_id].export_progress = round(percentage_display, 1)

                # Export is the first half of the process (0-50%)
                # Calculate total_progress as half of export_progress
                total_progress = percentage_display * 0.5
                self.active_jobs[job_id].total_progress = round(total_progress, 1)
                self.active_jobs[job_id].export_files = current

                # Make sure solution field is preserved
                if solution_value and not self.active_jobs[job_id].solution:
                    self.active_jobs[job_id].solution = solution_value

                # Format message with percentage and file count like "98.6%(69/70) - Exported page: application-logs-kibana"
                if message:
                    formatted_message = (
                        f"{percentage_display:.1f}%({current}/{total}) - {message}"
                    )
                    self.active_jobs[job_id].message = formatted_message

                # Log the progress at key intervals
                if current == total or current % 10 == 0 or percentage == 1.0:
                    status_snapshot = self.active_jobs[job_id]
                    logger.info(
                        f"Export progress for job {job_id}: {current}/{total} files, "
                        f"{percentage:.1%} complete, solution={status_snapshot.solution}"
                    )
            except Exception as e:
                logger.error(f"Error in export progress callback: {str(e)}")
                # Add traceback for better debugging
                import traceback

                logger.error(traceback.format_exc())

        return progress_callback

    async def translate_repository(
        self,
        source_path: str,
        target_dir: str | None,
        target_languages: list[str],
        selected_solution: str | None = None,
        job_id: str | None = None,
    ) -> bool:
        """Translate repository content to target languages.

        Args:
            source_path (str): Path to the source content (corresponds to selected Notion page)
            target_dir (str | None): Target directory for translations
            target_languages (list[str]): List of target languages to translate to
            selected_solution (str | None, optional): Selected solution type (ZCP, APIM, AMDP)
            job_id (str | None, optional): Current job ID for tracking progress

        Returns:
            bool: True if translation was successful, False otherwise
        """
        try:
            if not source_path or not target_languages:
                logger.error("Source path and target languages must be provided")
                return False

            # Get the solution type enum from string
            solution = (
                SolutionType(selected_solution.lower()) if selected_solution else None
            )
            if not solution:
                logger.error(f"Invalid solution type: {selected_solution}")
                return False

            # Log the actual paths we're working with for debugging
            logger.info(f"Starting translation from source path: {source_path}")
            logger.info(f"Selected solution: {solution.value}")

            # Set up the target directory
            if target_dir is None:
                target_dir = "i18n"

            # Create a job-specific translator instance with appropriate callback
            translation_progress_callback = None
            if job_id and job_id in self.active_jobs:
                translation_progress_callback = (
                    self._create_translation_progress_callback(job_id)
                )
                logger.info(f"Using progress tracking for job {job_id}")

            # Log the directories we're translating
            logger.info(f"Source directory: {source_path}")

            # Construct the base target path
            target_path = os.path.join(self.repo_path, target_dir)
            logger.info(f"Base target directory: {target_path}")

            # Get base source directory for the solution
            source_dir = os.path.join(
                self.repo_path, self.source_dir, solution.value.lower()
            )
            logger.info(f"Source base directory: {source_dir}")

            # # Determine if source is a file or directory
            # is_single_file = os.path.isfile(source_path)

            for lang in target_languages:
                lang_target_base = os.path.join(
                    target_path,
                    lang,
                    f"docusaurus-plugin-content-docs-{solution.value.lower()}",
                    "current",
                )
                os.makedirs(lang_target_base, exist_ok=True)
                logger.info(
                    f"Ensured translation base directory for {lang}: {lang_target_base}"
                )

            # Ensure images are available for translations
            # Copy images from static/img directory to ensure they're available for the translated content
            solution_img_dir = os.path.join(
                self.repo_path, "static", "img", solution.value.lower()
            )
            logger.info(f"Solution image directory: {solution_img_dir}")

            # Create a task translator
            task_translator = MarkdownTranslator(
                settings=Settings(
                    LANGUAGES=target_languages,
                    OPENAI_API_KEY=self.settings["openai_api_key"],
                    OPENAI_MODEL=self.settings["openai_model"],
                    MAX_CHUNK_SIZE=self.settings["max_chunk_size"],
                    MAX_CONCURRENT_REQUESTS=self.settings["max_concurrent_requests"],
                ),
                progress_callback=translation_progress_callback,
            )
            logger.info(
                f"Created Markdown translator with model: {self.settings['openai_model']}"
            )

            result = await task_translator.translate_repository(
                source_path=source_path,  # Use the provided source path directly
                target_dir=target_path,
                target_languages=target_languages,
                selected_solution=solution.value,
            )

            if not result:
                logger.error("Translation failed")
                return False

            # Commit translation changes
            if not await self._commit_translation_changes(
                f"Translate manual content for solution {solution.value}"
            ):
                logger.error("Failed to commit translation changes")
                return False

            return True

        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            return False

    def _find_node_by_path(
        self, nodes: list[Union[Manual, Folder]], target_path: str
    ) -> Union[Manual, Folder, None]:
        """Find a node (Manual or Folder) by its path in the manual structure.

        Args:
            nodes (list[Union[Manual, Folder]]): List of nodes to search
            target_path (str): Target path to find

        Returns:
            Union[Manual, Folder, None]: Found node or None if not found
        """
        for node in nodes:
            if isinstance(node, Manual):
                if node.path == target_path:
                    return node
            elif isinstance(node, Folder):
                # For folders, check children recursively
                if node.children:
                    found = self._find_node_by_path(node.children, target_path)
                    if found:
                        return found
        return None

    def _add_notification(
        self,
        status: NotificationStatus,
        title: str,
        message: str,
        solution: Optional[SolutionType] = None,
        user_id: Optional[str] = None,
        job_id: Optional[str] = None,
        notification_type: NotificationSourceType = NotificationSourceType.SYSTEM,
        node: Optional[Dict[str, Any]] = None,
    ):
        """Add a new notification."""
        notification = Notification(
            id=str(uuid.uuid4()),
            status=status,
            title=title,
            message=message,
            solution=solution,
            user_id=user_id,
            created_at=datetime.now(),
            job_id=job_id,
            notification_type=notification_type,
            node=node,
        )

        # Add document title if job_id exists and has title info
        if job_id and job_id in self.active_jobs:
            job_status = self.active_jobs[job_id]
            if job_status.title:
                notification.document_title = job_status.title

        self.notifications.append(notification)
        logger.info(
            f"Added notification: {notification.title} - {notification.message} for user: {user_id if user_id else 'all'}"
        )

        # Broadcast to all registered clients
        asyncio.create_task(self._broadcast_notification(notification))

        return notification

    async def add_notification(self, notification: Notification):
        """Add a pre-constructed notification to the notification system.

        Args:
            notification: The notification object to add

        Returns:
            The added notification
        """
        # Add document title if job_id exists and it's not already set
        if (
            notification.job_id
            and notification.job_id in self.active_jobs
            and not notification.document_title
        ):
            job_status = self.active_jobs[notification.job_id]
            if job_status.title:
                notification.document_title = job_status.title

        self.notifications.append(notification)
        logger.info(
            f"Added notification: {notification.title} - {notification.message} for user: {notification.user_id if notification.user_id else 'all'}"
        )

        # Broadcast to all registered clients
        await self._broadcast_notification(notification)

        return notification

    async def _broadcast_notification(self, notification: Notification):
        """Broadcast a notification to all registered clients.

        Args:
            notification: The notification to broadcast
        """
        # Create a copy of the clients to avoid modification during iteration
        clients = list(self.notification_clients.items())

        if not clients:
            logger.info("No notification clients registered, skipping broadcast")
            return

        logger.info(
            f"Broadcasting notification '{notification.title}' to {len(clients)} clients"
        )

        delivery_count = 0
        skip_count = 0
        for client_id, (queue, user_id) in clients:
            # Improved filtering logic for notification delivery
            should_deliver = False

            # Global notification stream client - deliver all notifications
            if user_id is None:
                should_deliver = True
                delivery_reason = "global notification stream"
            # Direct user match - notification is for this specific user
            elif notification.user_id is not None and notification.user_id == user_id:
                should_deliver = True
                delivery_reason = "direct user match"
            # System-wide notifications for admins
            elif notification.user_id is None and user_id in [
                "cloudzcp-admin",
                "admin",
            ]:
                should_deliver = True
                delivery_reason = "system notification to admin"
            # Job-initiated notifications - check if this user initiated the job
            elif notification.job_id and notification.job_id in self.active_jobs:
                job = self.active_jobs[notification.job_id]
                # If this job was initiated by this user, they can see related notifications
                if hasattr(job, "initiated_by") and job.initiated_by == user_id:
                    should_deliver = True
                    delivery_reason = "job initiator"

            if should_deliver:
                try:
                    logger.debug(
                        f"Delivering notification to client {client_id} ({delivery_reason})"
                    )
                    # Non-blocking put with a timeout
                    await asyncio.wait_for(queue.put(notification), timeout=2.0)
                    delivery_count += 1
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout broadcasting to client {client_id}")
                except asyncio.QueueFull:
                    logger.warning(
                        f"Queue full for client {client_id}, removing client"
                    )
                    await self.unregister_notification_client(client_id)
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client_id}: {str(e)}")
                    # Remove client on error
                    await self.unregister_notification_client(client_id)
            else:
                skip_count += 1
                logger.debug(
                    f"Skipping notification delivery to client {client_id} (user_id: {user_id})"
                )

        logger.info(
            f"Notification broadcast complete: {delivery_count} delivered, {skip_count} skipped"
        )

    async def register_notification_client(
        self, queue: asyncio.Queue, user_id: Optional[str] = None
    ) -> str:
        """Register a new client for notification streaming.

        Args:
            queue: An asyncio Queue where notifications will be sent
            user_id: Optional user ID to filter notifications

        Returns:
            A unique client ID that can be used to unregister
        """
        client_id = str(uuid.uuid4())
        self.notification_clients[client_id] = NotificationClient(queue, user_id)
        logger.info(f"Registered notification client {client_id} for user {user_id}")
        return client_id

    async def unregister_notification_client(self, client_id: str) -> bool:
        """Unregister a client from notification streaming.

        Args:
            client_id: The client ID to unregister

        Returns:
            True if the client was unregistered, False if not found
        """
        if client_id in self.notification_clients:
            queue, _ = self.notification_clients.pop(client_id)
            # Signal to the client that it should stop listening
            try:
                await queue.put(None)
            except Exception:
                pass  # Ignore errors when client is already gone

            logger.info(f"Unregistered notification client {client_id}")
            return True
        return False

    async def unregister_all_clients(self):
        """Unregister all notification clients."""
        client_ids = list(self.notification_clients.keys())
        logger.info(f"Unregistering all {len(client_ids)} notification clients")

        for client_id in client_ids:
            try:
                await self.unregister_notification_client(client_id)
            except Exception as e:
                logger.error(f"Error unregistering client {client_id}: {str(e)}")

        # Clear any remaining clients just to be safe
        self.notification_clients.clear()
        logger.info("All notification clients unregistered")

    async def get_notifications(
        self,
        limit: int = 50,
        include_read: bool = False,
        user_id: Optional[str] = None,
        latest_only: bool = False,
        job_id: Optional[str] = None,
    ) -> Union[List[Notification], Optional[Notification]]:
        """Get recent notifications.

        Args:
            limit: Maximum number of notifications to return
            include_read: Whether to include read notifications
            user_id: Filter notifications by user_id (if None, returns all notifications)
            latest_only: If True, return only the latest notification as a single object
            job_id: Optional job ID to filter notifications

        Returns:
            Either a list of notifications or a single latest notification (if latest_only=True)
        """
        # Determine which notifications the user is allowed to see
        # A user can see:
        # 1. Notifications explicitly addressed to them (user_id matches)
        # 2. System-wide notifications (user_id is None) IF they have admin privileges
        # 3. Job-specific notifications for jobs they initiated
        # 4. If user_id is None, return all notifications (used by global notification stream)

        # Check if the user has admin privileges
        is_admin = user_id in ["cloudzcp-admin", "admin"] if user_id else False

        # Filter notifications
        filtered = []
        for notification in self.notifications:
            # Skip read notifications unless explicitly included
            if not include_read and notification.is_read:
                continue

            # Filter by job_id if specified
            if job_id and notification.job_id != job_id:
                continue

            # If no user_id provided (global notification stream), include all notifications
            if user_id is None:
                filtered.append(notification)
            # User-specific filtering when user_id is provided
            elif notification.user_id == user_id:
                # User can always see their own notifications
                filtered.append(notification)
            elif notification.user_id is None and is_admin:
                # Admins can see system-wide notifications
                filtered.append(notification)
            # For job-related notifications, check if this user initiated the job
            elif notification.job_id and notification.job_id in self.active_jobs:
                job = self.active_jobs[notification.job_id]
                # If this job was initiated by this user, they can see related notifications
                if hasattr(job, "initiated_by") and job.initiated_by == user_id:
                    filtered.append(notification)

        # Sort by creation time (newest first)
        sorted_notifications = sorted(
            filtered, key=lambda x: x.created_at, reverse=True
        )

        # Return only the latest notification if requested
        if latest_only and sorted_notifications:
            return sorted_notifications[0]
        elif latest_only:
            return None

        # Otherwise return a list limited by the limit parameter
        return sorted_notifications[:limit]

    async def mark_notification_read(self, notification_id: str) -> bool:
        """Mark a notification as read."""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.is_read = True
                return True
        return False

    async def clear_notifications(self) -> None:
        """Clear all notifications."""
        self.notifications = []

    async def _ensure_exporter(self, solution_type: SolutionType) -> bool:
        """Ensure the exporter for the given solution type is initialized.

        Args:
            solution_type: The solution type to ensure exporter for

        Returns:
            bool: True if exporter was initialized or already exists, False otherwise
        """
        try:
            if self.exporters[solution_type].docs_node is None:
                root_page_id = self.root_page_ids.get(solution_type)
                if not root_page_id:
                    logger.error(f"No root page ID configured for {solution_type}")
                    return False

                # Initialize the exporter with the correct root_output_dir
                self.exporters[solution_type] = NotionPageExporter(
                    notion_token=self.notion_token,
                    root_page_id=root_page_id,
                    root_output_dir=str(self.repo_path),
                )
                logger.info(f"Initialized {solution_type} exporter")

            return True
        except Exception as e:
            logger.error(f"Failed to initialize {solution_type} exporter: {e}")
            return False

    async def export_repository(
        self,
        notion_page_id: str,
        output_dir: str,
        selected_solution: SolutionType,
        job_id: Optional[str] = None,
        is_directory: bool = False,
    ) -> Tuple[bool, Optional[str], Optional[int]]:
        """Export a repository from Notion.

        Args:
            notion_page_id: The Notion page ID to export
            output_dir: The output directory
            selected_solution: The selected solution type
            job_id: Optional job ID for progress tracking
            is_directory: Whether the page is a directory

        Returns:
            Tuple[bool, Optional[str], Optional[int]]: Success status, export path, and number of files exported
        """
        try:
            logger.info(
                f"Starting export for {selected_solution} from page {notion_page_id}"
            )

            exporter = self.exporters[selected_solution]
            if not exporter.initialized_node_tree:
                if not await self._ensure_exporter(selected_solution):
                    return (
                        False,
                        f"Failed to initialize node_tree for {selected_solution}",
                        None,
                    )

            # Set up progress callback if job_id is provided
            if job_id and job_id in self.active_jobs:
                exporter.progress_callback = self._create_export_progress_callback(
                    job_id
                )

            # self.exporters[selected_solution].root_output_dir = os.path.dirname(output_dir)

            # Format the Notion page ID
            formatted_page_id = self._format_page_id(notion_page_id)

            # Export the content
            export_path = await asyncio.to_thread(
                exporter.markdownx,
                page_id=formatted_page_id,
                include_subpages=is_directory,
            )

            if not export_path:
                return False, f"Failed to export content for {selected_solution}", None

            # Count exported files: if export_path is a single file, count as 1, otherwise count all files in the directory
            export_path_obj = Path(export_path)
            if export_path_obj.is_file():
                num_files = 1
            else:
                # count only files, not directories
                num_files = sum(1 for p in export_path_obj.rglob("*") if p.is_file())
            return True, export_path, num_files

        except Exception as e:
            logger.error(f"Error during export: {e}")
            logger.error(traceback.format_exc())
            return False, str(e), None

    async def _ensure_images_for_translations(
        self,
        selected_solution: SolutionType,
        target_languages: Optional[List[str]] = None,
    ) -> bool:
        """Ensure images are available for translations by copying them from the main repository."""
        try:
            solution_value = selected_solution.value.lower()

            # Source image directory in the main repository (where images should be copied from)
            main_repo_img_dir = os.path.join(
                self.original_repo_path, "static", "img", solution_value
            )
            # Target image directory in the job-specific repository
            job_repo_img_dir = os.path.join(
                self.repo_path, "static", "img", solution_value
            )
            logger.info(
                f"Copying images from main repo: {main_repo_img_dir} to job repo: {job_repo_img_dir}"
            )

            # Ensure target directory exists
            os.makedirs(job_repo_img_dir, exist_ok=True)

            # Copy all images from main repo to job repo, preserving structure
            if os.path.exists(main_repo_img_dir):
                # First, copy the entire solution directory
                shutil.copytree(main_repo_img_dir, job_repo_img_dir, dirs_exist_ok=True)
                logger.info(f"Copied all images for {solution_value} to job repo.")

                # # Then, for each target language, ensure the images are also available in the language-specific directory
                # for lang in target_languages:
                #     lang_img_dir = os.path.join(self.repo_path, "static", "img", lang, solution_value)
                #     os.makedirs(lang_img_dir, exist_ok=True)
                #     shutil.copytree(main_repo_img_dir, lang_img_dir, dirs_exist_ok=True)
                #     logger.info(f"Copied images for {solution_value} to {lang} directory")
            else:
                logger.warning(
                    f"Main repo image directory does not exist: {main_repo_img_dir}"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Error ensuring images for translations: {e}")
            logger.error(traceback.format_exc())
            return False

    async def initialize_cache(self):
        """Initialize all caches including node information and document content."""
        try:
            logger.info("Initializing all caches...")

            # Step 1: Initialize manuals cache (node information)
            logger.info("Initializing manuals cache for all solutions")
            for solution_type in self.root_page_ids.keys():
                try:
                    logger.info(f"Preloading manual cache for {solution_type.value}")

                    # Initialize exporter for this solution type
                    if not await self._ensure_exporter(solution_type):
                        logger.error(
                            f"Failed to initialize exporter for {solution_type.value}"
                        )
                        continue

                    exporter = self.exporters[solution_type]
                    if not exporter:
                        logger.error(f"No exporter found for {solution_type.value}")
                        continue

                    # First try to load from filesystem cache
                    cache_loaded = await self._load_tree_cache_from_file(solution_type)

                    if cache_loaded:
                        # Load nodes from filesystem cache
                        (
                            docs_node,
                            static_image_node,
                        ) = await self._load_node_cache_from_file(solution_type)

                        if docs_node and static_image_node:
                            self.exporters[solution_type].docs_node = docs_node
                            self.exporters[
                                solution_type
                            ].static_image_node = static_image_node
                            self.exporters[solution_type].initialized_node_tree = True
                            logger.info(
                                f"Loaded docs node from cache for {solution_type.value}"
                            )
                        else:
                            # If docs_node not in cache, initialize it
                            logger.info(
                                f"No docs node in cache for {solution_type.value}, initializing..."
                            )
                            if await self._export_node_cache(
                                solution_type, self.root_page_ids[solution_type]
                            ):
                                exporter.initialized_node_tree = True
                                logger.info(
                                    f"Initialized docs node for {solution_type.value}"
                                )

                        logger.info(
                            f"Successfully loaded {solution_type.value} manual cache from filesystem"
                        )
                    else:
                        # If filesystem cache doesn't exist or is invalid, fetch from Notion
                        logger.info(
                            f"No valid filesystem cache for {solution_type.value}, fetching from Notion"
                        )
                        # Make the tree node - this will properly initialize docs_node and static_image_node
                        try:
                            if await self._ensure_repository():

                                await self.get_manuals(selected_solution=solution_type)

                                logger.info(
                                    f"Successfully created node tree for {solution_type}"
                                )
                            else:
                                logger.error(
                                    f"Failed to create node tree for {solution_type}"
                                )
                                return False
                        except Exception as e:
                            logger.error(
                                f"Failed to create node tree for {solution_type}: {e}"
                            )
                            return False
                        # Initialize node tree
                        if await self._export_node_cache(
                            solution_type, self.root_page_ids[solution_type]
                        ):
                            exporter.initialized_node_tree = True
                            # Commit export changes
                            if not await self._commit_export_changes(
                                f"Export manual content for solution {solution_type}"
                            ):
                                logger.error(
                                    f"Failed to commit export changes for {solution_type}"
                                )
                                return False

                            # Push changes
                            if await self._push_changes():
                                logger.info(
                                    f"Successfully pushed changes for {solution_type.value}"
                                )
                            else:
                                logger.error(
                                    f"Failed to push changes for {solution_type.value}"
                                )
                                return False
                            logger.info(
                                f"Initialized node tree for {solution_type.value}"
                            )

                        # Cache the content
                        # await self._ensure_cached_content(solution_type, self.root_page_ids[solution_type])

                    # Verify initialization
                    if exporter.initialized_node_tree:
                        logger.info(
                            f"Exporter for {solution_type.value} is fully initialized"
                        )
                    else:
                        logger.warning(
                            f"Exporter for {solution_type.value} initialization incomplete"
                        )

                except Exception as e:
                    logger.error(
                        f"Error initializing caches for {solution_type.value}: {str(e)}"
                    )
                    continue

            logger.info(
                f"Cache initialization complete for {len(self.manuals_cache)} solutions"
            )
            return True

        except Exception as e:
            logger.error(f"Error in cache initialization: {str(e)}")
            return False

    async def update_manuals_cache(
        self, solution_type: SolutionType, notion_page_id: Optional[str] = None
    ) -> bool:
        """Update the manuals cache for a specific solution.

        Args:
            solution_type: The solution type to update
            notion_page_id: Optional specific page ID that was updated. If provided,
                            the method will optimize fetching only the necessary nodes.

        Returns:
            bool: True if the cache was successfully updated, False otherwise
        """
        try:
            logger.info(
                f"Updating manuals cache for {solution_type.value}"
                + (f", focusing on page {notion_page_id}" if notion_page_id else "")
            )

            # Get the root page ID for the selected solution
            root_page_id = self.root_page_ids.get(solution_type)
            if not root_page_id:
                error_msg = (
                    f"No root page ID configured for solution {solution_type.value}"
                )
                logger.error(error_msg)
                return False

            # Format and validate the root page ID
            try:
                formatted_root_id = self._format_page_id(root_page_id)
            except ValueError as e:
                error_msg = (
                    f"Invalid root page ID for solution {solution_type.value}: {str(e)}"
                )
                logger.error(error_msg)
                return False

            # # Create a separate exporter instance for this request
            # request_exporter = NotionPageExporter(
            #     notion_token=self.notion_token,
            #     root_page_id=formatted_root_id,  # Use the solution's root page ID
            #     root_output_dir="repo",
            # )

            # Get the exporter for the solution type
            request_exporter = self.exporters[solution_type]

            # Reset the initialized_node_tree flag
            request_exporter.initialized_node_tree = False

            # Determine which page ID to use for fetching nodes
            target_page_id = None
            if notion_page_id:
                # Check if the page exists in current cache
                current_cache = self.manuals_cache.get(solution_type, [])
                page_exists = False
                if current_cache:
                    all_nodes = self._flatten_nodes(current_cache)
                    for node in all_nodes:
                        if (
                            hasattr(node, "object_id")
                            and node.object_id == notion_page_id
                        ):
                            page_exists = True
                            target_page_id = notion_page_id
                            break

                if not page_exists:
                    # If page doesn't exist in cache, use root page to get full tree
                    logger.info(
                        f"Page {notion_page_id} not found in cache, fetching full tree"
                    )
                    target_page_id = formatted_root_id
            else:
                # If no specific page ID provided, use root page
                target_page_id = formatted_root_id

            # Get nodes from the exporter
            logger.info(f"Fetching nodes from page ID: {target_page_id}")
            nodes = await asyncio.to_thread(
                request_exporter.get_tree_nodes, page_id=target_page_id
            )

            if not nodes:
                error_msg = f"No nodes returned for {solution_type.value}"
                logger.error(error_msg)
                return False

            # If we fetched nodes for a specific page, merge them with existing cache
            if notion_page_id and target_page_id == notion_page_id:
                current_cache = self.manuals_cache.get(solution_type, [])
                if current_cache:
                    # Replace or add the updated nodes
                    updated_nodes = self._merge_nodes(current_cache, nodes)
                    nodes = updated_nodes
                    logger.info(
                        f"Merged {len(nodes)} updated nodes with existing cache"
                    )

            # Update the in-memory cache
            self.manuals_cache[solution_type] = nodes
            self.cache_last_updated[solution_type] = datetime.now()

            # Also update the filesystem cache
            await self._save_cache_to_file(solution_type)

            logger.info(
                f"Successfully updated manuals cache for {solution_type.value} with {len(nodes)} nodes"
            )

            # Find the specific node that was updated if notion_page_id was provided
            updated_node = None
            if notion_page_id:
                # Flatten all nodes to search for the specific node
                all_nodes = self._flatten_nodes(nodes)
                for node in all_nodes:
                    if hasattr(node, "object_id") and node.object_id == notion_page_id:
                        updated_node = node
                        break

            # Create node information dictionary for the notification
            node_info = None
            if updated_node:
                node_info = {
                    "object_id": updated_node.object_id,
                    "title": updated_node.name,
                    "is_directory": updated_node.is_directory,
                    "parent_id": updated_node.parent.object_id
                    if updated_node.parent
                    else None,
                    "notion_url": updated_node.notion_url,
                    "index": updated_node.index
                    if hasattr(updated_node, "index")
                    else None,
                    "last_edited_time": updated_node.last_edited_time.isoformat()
                    if hasattr(updated_node, "last_edited_time")
                    and updated_node.last_edited_time
                    else None,
                    "last_edited_by": updated_node.last_edited_by
                    if hasattr(updated_node, "last_edited_by")
                    else None,
                    "last_editor_avatar_url": updated_node.last_editor_avatar_url
                    if hasattr(updated_node, "last_editor_avatar_url")
                    else None,
                }

            # Create a notification about the cache update
            self._add_notification(
                status=NotificationStatus.INFO,
                title=f"{solution_type.value.upper()} Manuals Updated",
                message=f"The manuals for {solution_type.value.upper()} have been updated ({len(nodes)} documents)"
                + (" due to changes in a specific page" if notion_page_id else ""),
                solution=solution_type,
                notification_type=NotificationSourceType.DOCUMENT_UPDATE,
                node=node_info,
            )

            # Set the initialized_node_tree flag
            request_exporter.initialized_node_tree = True

            return True

        except Exception as e:
            logger.error(
                f"Error updating manuals cache for {solution_type.value}: {str(e)}"
            )
            return False

    def _merge_nodes(self, existing_nodes: list, updated_nodes: list) -> list:
        """Merge updated nodes into existing nodes list.

        Args:
            existing_nodes: Current list of nodes in cache
            updated_nodes: New nodes to merge in

        Returns:
            list: Merged list of nodes
        """
        # Convert existing nodes to dictionary for easy lookup
        nodes_dict = {}
        for node in self._flatten_nodes(existing_nodes):
            if hasattr(node, "object_id"):
                nodes_dict[node.object_id] = node

        # Update or add new nodes
        for node in self._flatten_nodes(updated_nodes):
            if hasattr(node, "object_id"):
                nodes_dict[node.object_id] = node

        # Convert back to list preserving hierarchy
        result = []
        for node in existing_nodes:
            if hasattr(node, "object_id") and node.object_id in nodes_dict:
                result.append(nodes_dict[node.object_id])

        return result

    async def _load_node_cache_from_file(
        self, solution_type: SolutionType
    ) -> tuple[Node, Node]:
        """Load cached nodes from files.

        Args:
            solution_type: The solution type to load cache for

        Returns:
            tuple[Node, Node]: A tuple containing (docs_node, static_image_node)
        """
        try:
            # Load docs node
            docs_node = None
            docs_node_file = (
                Path(self.cache_path)
                / "docs"
                / solution_type.value.lower()
                / "docs_node.pkl"
            )
            if docs_node_file.exists():
                try:
                    async with aiofiles.open(docs_node_file, "rb") as f:
                        content = await f.read()
                        docs_node = pickle.loads(content)
                        if not isinstance(docs_node, Node):
                            logger.error(
                                f"Invalid docs node type for {solution_type}: {type(docs_node)}"
                            )
                            docs_node = None
                except Exception as e:
                    logger.error(
                        f"Error loading docs node for {solution_type}: {str(e)}"
                    )

            # Load static image node
            static_image_node = None
            static_node_file = (
                Path(self.cache_path)
                / "static/img"
                / solution_type.value.lower()
                / "static_node.pkl"
            )
            if static_node_file.exists():
                try:
                    async with aiofiles.open(static_node_file, "rb") as f:
                        content = await f.read()
                        static_image_node = pickle.loads(content)
                        if not isinstance(static_image_node, Node):
                            logger.error(
                                f"Invalid static image node type for {solution_type}: {type(static_image_node)}"
                            )
                            static_image_node = None
                except Exception as e:
                    logger.error(
                        f"Error loading static image node for {solution_type}: {str(e)}"
                    )

            return docs_node, static_image_node

        except Exception as e:
            logger.error(f"Error loading node cache for {solution_type}: {str(e)}")
            return None, None

    async def _export_node_cache(
        self, solution_type: SolutionType, page_id: str
    ) -> bool:
        """Export the docs images for a solution type using markdownx to load cache.

        Args:
            solution_type: The solution type to initialize
            page_id: The Notion page ID to initialize from

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            task_exporter = self.exporters[solution_type]
            if not task_exporter:
                return False

            # Format the page ID
            formatted_page_id = self._format_page_id(page_id)

            # Log the directories we're exporting to
            logger.info(f"Output directory: {self.repo_path}")

            # Export the content
            export_path = await asyncio.to_thread(
                task_exporter.markdownx,  # Use markdownx for MDX file support
                page_id=formatted_page_id,
                include_subpages=True,
            )

            # Enhanced result checking with better logging
            logger.info(f"Export result path: {export_path}")

            if not export_path:
                logger.error(
                    f"Export failed: No path returned from exporter for page {formatted_page_id}"
                )
                return False, None, 0

            # Check if path exists - either as is or with .mdx extension
            actual_path = export_path
            export_dir = os.path.dirname(actual_path)
            logger.info(f"Actual export directory path: {export_dir}")

            # Function to count only newly exported MDX files
            def count_new_mdx_files(directory):
                mdx_count = 0
                exported_files = set()

                # Construct the target directory path by appending job_title
                target_dir = directory
                logger.info(f"Counting MDX files in directory: {target_dir}")

                if not os.path.exists(target_dir):
                    logger.warning(f"Export directory does not exist: {target_dir}")
                    return 0, set()

                # Get the solution name from the directory path
                source_basename = os.path.basename(target_dir).lower()
                logger.info(f"Source basename (solution): {source_basename}")

                # Walk through all subdirectories
                for root, _, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith(".mdx"):
                            file_abs = os.path.join(root, file)
                            # Get path relative to target directory
                            rel_path = os.path.relpath(file_abs, target_dir)
                            # If the first directory is the solution name, remove it from count
                            rel_parts = rel_path.split(os.sep)
                            if rel_parts and rel_parts[0].lower() == source_basename:
                                logger.info(
                                    f"Skipping file in solution directory: {rel_path}"
                                )
                                continue

                            mdx_count += 1
                            exported_files.add(file_abs)
                            logger.info(f"Found newly exported MDX file: {file_abs}")

                logger.info(f"Total MDX files found in {target_dir}: {mdx_count}")
                return mdx_count, exported_files

            # Count the number of MDX files exported
            mdx_files, exported_files = await asyncio.to_thread(
                count_new_mdx_files, export_dir
            )

            # Save the docs node and static image node to pickle files
            await self._save_pickle_to_file(solution_type)

            logger.info(
                f"Successfully exported {mdx_files} MDX files for {solution_type.value}"
            )
            return True, actual_path, mdx_files

        except Exception as e:
            logger.error(
                f"Error initializing node tree for {solution_type.value}: {str(e)}"
            )
            return False

    async def _ensure_cached_content(
        self, solution_type: SolutionType, notion_page_id: str
    ) -> bool:
        """Ensure cached content exists for the given solution type and page ID.

        Args:
            solution_type: The solution type to ensure cache for
            notion_page_id: The Notion page ID to ensure cache for

        Returns:
            bool: True if cache exists or was created successfully, False otherwise
        """
        try:
            # Initialize exporter for this solution type
            if not await self._ensure_exporter(solution_type):
                logger.error(f"Failed to initialize exporter for {solution_type.value}")
                return False

            # First try to load from filesystem cache
            cached_data = await self._load_tree_cache_from_file(solution_type)

            if cached_data:
                # Get the exporter for this solution type
                exporter = self.exporters[solution_type]

                # Create root node
                root_data = cached_data.get("root", {})
                if not root_data:
                    logger.error(
                        f"No root node found in cache for {solution_type.value}"
                    )
                    return False

                # Map the cached data to NodeModel structure
                root_node = NodeModel(
                    object_id=root_data.get("object_id", ""),
                    title=root_data.get("name", ""),  # Use name as title
                    parent_id=root_data.get("parent_id"),
                    children=[],  # Will be populated below
                    notion_url=root_data.get("notion_url"),
                    path=f"/{solution_type.value.lower()}",  # Set default path
                    last_edited_time=root_data.get("last_edited_time"),
                    last_edited_by=root_data.get("last_edited_by"),
                    last_editor_avatar_url=root_data.get("last_editor_avatar_url"),
                )

                # Process children recursively
                def process_children(
                    parent_node: NodeModel, children_data: list
                ) -> None:
                    for child_data in children_data:
                        # Create child node with proper path
                        child_path = f"{parent_node.path}/{child_data.get('name', '')}"
                        child_node = NodeModel(
                            object_id=child_data.get("object_id", ""),
                            title=child_data.get("name", ""),
                            parent_id=child_data.get("parent_id"),
                            children=[],
                            notion_url=child_data.get("notion_url"),
                            path=child_path,
                            last_edited_time=child_data.get("last_edited_time"),
                            last_edited_by=child_data.get("last_edited_by"),
                            last_editor_avatar_url=child_data.get(
                                "last_editor_avatar_url"
                            ),
                        )

                        # Process children recursively if they exist
                        child_children = child_data.get("children", [])
                        if child_children:
                            process_children(child_node, child_children)

                        parent_node.children.append(child_node)

                # Process root's children
                root_children = root_data.get("children", [])
                if root_children:
                    process_children(root_node, root_children)

                # Set the reconstructed tree
                exporter.docs_node = root_node
                exporter.initialized_node_tree = True
                logger.info(
                    f"Successfully loaded node tree from cache for {solution_type.value}"
                )
                return True

            # If no cache exists, create it
            logger.info(f"No cache found for {solution_type.value}, creating new cache")
            return await self._export_node_cache(solution_type, notion_page_id)

        except Exception as e:
            logger.error(f"Error ensuring cached content for {solution_type}: {str(e)}")
            return False

    def _get_cache_file_path(self, solution_type: SolutionType) -> Path:
        """Get the path to the cache file for a solution type."""
        return (
            Path(self.cache_path)
            / "manuals"
            / f"{solution_type.value.lower()}_cache.json"
        )

    def _flatten_nodes(self, nodes):
        """Flatten a tree of nodes into a list.

        Args:
            nodes: List of Node objects that form a tree structure

        Returns:
            List of all nodes in the tree, including all descendants
        """
        result = []
        if not nodes:
            return result

        for node in nodes:
            result.append(node)
            if node.is_directory and node.children:
                result.extend(self._flatten_nodes(node.children))

        return result

    async def _save_cache_to_file(self, solution_type: SolutionType) -> bool:
        """Save the cached manuals data for a solution to a file.

        Args:
            solution_type: The solution type whose cache to save

        Returns:
            bool: True if successful, False otherwise
        """
        if solution_type not in self.manuals_cache:
            logger.warning(f"No cache data to save for {solution_type.value}")
            return False

        try:
            cache_file = self._get_cache_file_path(solution_type)

            # Create a serializable structure
            serializable_data = {
                "last_updated": self.cache_last_updated.get(
                    solution_type, datetime.now()
                ).isoformat(),
                "nodes": [],
            }

            # Get all nodes, including children
            root_nodes = self.manuals_cache[solution_type]
            all_nodes = self._flatten_nodes(root_nodes)
            logger.info(
                f"Saving {len(all_nodes)} nodes to cache file for {solution_type.value}"
            )

            # Convert nodes to serializable dictionaries
            for node in all_nodes:
                node_dict = {
                    "object_id": node.object_id,
                    "name": node.name,
                    "is_directory": node.is_directory,
                    "parent_id": node.parent.object_id if node.parent else None,
                    "notion_url": node.notion_url,
                    "index": node.index,
                    "last_edited_time": node.last_edited_time.isoformat()
                    if hasattr(node, "last_edited_time") and node.last_edited_time
                    else None,
                    "last_edited_by": node.last_edited_by
                    if hasattr(node, "last_edited_by")
                    else None,
                    "last_editor_avatar_url": node.last_editor_avatar_url
                    if hasattr(node, "last_editor_avatar_url")
                    else None,
                }
                serializable_data["nodes"].append(node_dict)

            # Write to a temporary file first to avoid corruption if the process is interrupted
            temp_file = cache_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)

            # Rename the temporary file to the actual cache file (atomic operation)
            shutil.move(temp_file, cache_file)

            logger.info(
                f"Saved cache for {solution_type.value} to {cache_file} ({len(serializable_data['nodes'])} nodes)"
            )
            return True

        except Exception as e:
            logger.error(
                f"Error saving cache to file for {solution_type.value}: {str(e)}"
            )
            return False

    async def _save_pickle_to_file(self, solution_type: SolutionType) -> bool:
        """Save the docs node and static image node for a solution to a pickle file.
        Args:
            solution_type: The solution type to save cache for

        Returns:
            bool: True if cache was saved successfully, False otherwise
        """
        try:
            # Get the exporter for this solution type
            exporter = self.exporters[solution_type]
            if not exporter:
                logger.error(f"No exporter found for {solution_type.value}")
                return False

            # Create necessary directories
            docs_dir = Path(self.cache_path) / "docs" / solution_type.value.lower()
            static_dir = (
                Path(self.cache_path) / "static/img" / solution_type.value.lower()
            )

            docs_dir.mkdir(parents=True, exist_ok=True)
            static_dir.mkdir(parents=True, exist_ok=True)

            # Save docs node
            if exporter.docs_node:
                docs_node_file = docs_dir / "docs_node.pkl"
                try:
                    async with aiofiles.open(docs_node_file, "wb") as f:
                        await f.write(pickle.dumps(exporter.docs_node))
                    logger.info(f"Saved docs node for {solution_type.value}")
                except Exception as e:
                    logger.error(
                        f"Error saving docs node for {solution_type.value}: {str(e)}"
                    )
                    return False

            # Save static image node
            if exporter.static_image_node:
                static_node_file = static_dir / "static_node.pkl"
                try:
                    async with aiofiles.open(static_node_file, "wb") as f:
                        await f.write(pickle.dumps(exporter.static_image_node))
                    logger.info(f"Saved static image node for {solution_type.value}")
                except Exception as e:
                    logger.error(
                        f"Error saving static image node for {solution_type.value}: {str(e)}"
                    )
                    return False

            return True

        except Exception as e:
            logger.error(f"Error saving cache for {solution_type.value}: {str(e)}")
            return False

    async def _load_tree_cache_from_file(
        self, solution_type: SolutionType
    ) -> Optional[Dict[str, Any]]:
        """Load the cached node tree for a solution from a file.

        Args:
            solution_type: The solution type to load cache for

        Returns:
            bool: True if cache was loaded successfully, False otherwise
        """
        try:
            cache_file = self._get_cache_file_path(solution_type)
            if not cache_file.exists():
                logger.info(f"No cache file found for {solution_type.value}")
                return None

            try:
                async with aiofiles.open(cache_file, "r") as f:
                    content = await f.read()
                    if not content:
                        logger.error(f"Empty cache file for {solution_type.value}")
                        return None

                    try:
                        # Try JSON first
                        data = json.loads(content)
                    except json.JSONDecodeError:
                        # If JSON fails, try pickle
                        async with aiofiles.open(cache_file, "rb") as f:
                            content = await f.read()
                            try:
                                data = pickle.loads(content)
                            except pickle.UnpicklingError as e:
                                logger.error(
                                    f"Failed to load cache data for {solution_type.value}: {str(e)}"
                                )
                                return None

                if not isinstance(data, dict):
                    logger.error(
                        f"Invalid cache data format for {solution_type.value}: expected dict, got {type(data)}"
                    )
                    return False

                # First pass: create all nodes
                nodes_by_id = {}
                for node_data in data["nodes"]:
                    node = Node(
                        object_id=node_data["object_id"],
                        name=node_data["name"],
                        is_directory=node_data["is_directory"],
                        notion_url=node_data["notion_url"],
                    )
                    if "index" in node_data:
                        node.index = node_data["index"]
                    if (
                        "last_edited_time" in node_data
                        and node_data["last_edited_time"]
                    ):
                        node.last_edited_time = datetime.fromisoformat(
                            node_data["last_edited_time"]
                        )
                    if "last_edited_by" in node_data:
                        node.last_edited_by = node_data["last_edited_by"]
                    if "last_editor_avatar_url" in node_data:
                        node.last_editor_avatar_url = node_data[
                            "last_editor_avatar_url"
                        ]
                    nodes_by_id[node.object_id] = node

                # Second pass: establish parent-child relationships
                for node_data in data["nodes"]:
                    if node_data["parent_id"] and node_data["parent_id"] in nodes_by_id:
                        child_node = nodes_by_id[node_data["object_id"]]
                        parent_node = nodes_by_id[node_data["parent_id"]]

                        # Set parent reference
                        child_node.parent = parent_node

                        # Add child to parent's children list
                        if parent_node.is_directory:
                            if parent_node.children is None:
                                parent_node.children = []
                            parent_node.children.append(child_node)

                # Create a list of root nodes (nodes without parents)
                root_nodes = [
                    node for node in nodes_by_id.values() if node.parent is None
                ]

                # Store in the cache
                self.manuals_cache[solution_type] = root_nodes

                # Parse the last_updated timestamp
                if "last_updated" in data:
                    try:
                        self.cache_last_updated[solution_type] = datetime.fromisoformat(
                            data["last_updated"]
                        )
                    except (ValueError, TypeError):
                        self.cache_last_updated[solution_type] = datetime.now()

                logger.info(
                    f"Loaded cache for {solution_type.value} from {cache_file} ({len(nodes_by_id)} nodes)"
                )

                return True

            except Exception as e:
                logger.error(
                    f"Error reading cache file for {solution_type.value}: {str(e)}"
                )
                return False

        except Exception as e:
            logger.error(f"Error loading tree cache for {solution_type}: {str(e)}")
            return False
