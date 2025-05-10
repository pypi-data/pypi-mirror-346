"""
TrainLoop Evaluations SDK for automatic collection of LLM API calls.

This module provides the collect() function to instrument LLM API calls
by monkey-patching common LLM client libraries.
"""

import os
import json
import time
import inspect
import logging
import functools
import threading
from typing import Dict, Any, Callable, TypeVar
from pathlib import Path

# Setup logger
logger = logging.getLogger("trainloop_evals")

# Global variables for tracking state
_registry = {}
_registry_lock = threading.RLock()
_is_initialized = False

F = TypeVar("F", bound=Callable[..., Any])


# Type alias for the trainloop_tag parameter to suppress type errors
class TrainloopParam:
    """Type annotation for the trainloop_tag parameter."""

    def __new__(cls, *args, **kwargs):
        return str(*args, **kwargs) if args else None


def collect():
    """
    Initialize TrainLoop's data collection instrumentation.

    This function monkey-patches common LLM client libraries to intercept
    API calls with the trainloop_tag parameter. It should be called once
    at your application's startup.

    If the TRAINLOOP_DATA_FOLDER environment variable is not set,
    this function becomes a no-op.
    """
    global _is_initialized
    if _is_initialized:
        logger.debug("TrainLoop collect() already initialized")
        return

    evals_folder = os.environ.get("TRAINLOOP_DATA_FOLDER")
    if not evals_folder:
        logger.debug("TRAINLOOP_DATA_FOLDER not set, collect() is a no-op")
        return

    # Create the evals folder if it doesn't exist
    evals_path = Path(evals_folder)
    try:
        evals_path.mkdir(parents=True, exist_ok=True)
        logger.info(
            f"TrainLoop collect() initialized with evals folder: {evals_folder}"
        )
    except OSError as e:
        # More specific exception instead of catching Exception
        logger.error(f"Failed to create TrainLoop evals folder: {e}")
        return

    # Monkey-patch OpenAI
    _patch_openai()

    # Monkey-patch Anthropic
    _patch_anthropic()

    # Save the initial registry
    _save_registry(evals_path / "_registry.json")

    # Mark as initialized
    _is_initialized = True


def _get_caller_info() -> Dict[str, str]:
    """Get information about the calling file and line number."""
    frame = inspect.currentframe()
    try:
        # Walk up the stack to find the first frame outside this file
        while frame:
            frame_info = inspect.getframeinfo(frame)
            if __file__ not in frame_info.filename:
                return {
                    "file": frame_info.filename,
                    "line": str(frame_info.lineno),
                    "function": frame_info.function,
                }
            frame = frame.f_back
        return {"file": "unknown", "line": "0", "function": "unknown"}
    finally:
        del frame  # Avoid reference cycles


def _save_sample(
    tag: str, model: str, request: Any, response: Any, start_time: float
) -> None:
    """Save a sample to a file in the data folder."""
    if not tag:
        return  # Don't save untagged calls

    evals_folder = os.environ.get("TRAINLOOP_DATA_FOLDER")
    if not evals_folder:
        return

    try:
        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)

        # Create sample data
        current_time = time.time()
        sample = {
            "timestamp": int(current_time * 1000),  # Current time in ms
            "trainloop_tag": tag,
            "model": model,
            "request": request,
            "response": response,
            "latency_ms": latency_ms,
        }

        # Ensure tag directory exists
        tag_dir = Path(evals_folder) / "events"
        tag_dir.mkdir(parents=True, exist_ok=True)

        # Write to tag-specific file
        tag_file = tag_dir / f"{tag}.jsonl"
        with open(tag_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(sample) + "\n")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to save sample due to JSON decode error: {e}")
    except IOError as e:
        logger.error(f"Failed to save sample due to I/O error: {e}")
    except Exception as e:
        logger.error(f"Failed to save sample: {e}")


def _patch_function(obj: Any, attr_name: str) -> None:
    """Patch a function or method to intercept trainloop_tag."""
    if not hasattr(obj, attr_name):
        return

    orig_func = getattr(obj, attr_name)

    @functools.wraps(orig_func)
    def wrapper(*args, **kwargs):
        tag = kwargs.pop("trainloop_tag", None)
        caller_info = _get_caller_info()
        start_time = time.time()
        model = None

        # Extract model information if available
        if len(args) > 0 and isinstance(args[0], dict) and "model" in args[0]:
            model = args[0]["model"]
        elif "model" in kwargs:
            model = kwargs["model"]

        if tag:
            # Log the call in the registry
            location = f"{caller_info['file']}:{caller_info['line']}"
            _update_registry(location, tag)

            # Log the usage
            logger.debug(f"TrainLoop tagged call: {tag} at {location}")
        else:
            # Log untagged call
            location = f"{caller_info['file']}:{caller_info['line']}"
            _update_registry(location, "untagged")

        # Call the original function
        try:
            response = orig_func(*args, **kwargs)

            # Save the sample if tag is provided
            if tag:
                # Format request for saving
                if len(args) > 0 and isinstance(args[0], dict):
                    request = args[0]
                else:
                    request = kwargs

                _save_sample(tag, model or "unknown", request, response, start_time)

            return response
        except (ValueError, TypeError, KeyError) as e:
            # More specific exceptions for better error handling
            logger.error(f"Error in patched function: {e}")
            raise  # Re-raise the exception

    setattr(obj, attr_name, wrapper)


def _update_registry(location: str, tag: str) -> None:
    """Update the registry with a new tag usage."""
    with _registry_lock:
        if location not in _registry:
            _registry[location] = {}

        if tag not in _registry[location]:
            _registry[location][tag] = 0

        _registry[location][tag] += 1

        # Save the registry periodically
        evals_folder = os.environ.get("TRAINLOOP_DATA_FOLDER")
        if evals_folder:
            registry_path = Path(evals_folder) / "_registry.json"
            _save_registry(registry_path)


def _save_registry(path: Path) -> None:
    """Save the current registry to a JSON file."""
    with _registry_lock:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(_registry, f, indent=2)
        except (IOError, OSError) as e:
            logger.error(f"Failed to save TrainLoop registry: {e}")


def _patch_openai() -> None:
    """Patch the OpenAI client library."""
    try:
        import openai

        # Check if we have the new v1 client
        if hasattr(openai, "ChatCompletion") or hasattr(openai, "chat"):
            # New v1 API with namespaces
            if hasattr(openai, "chat") and hasattr(openai.chat, "completions"):
                _patch_function(openai.chat.completions, "create")

            # Legacy v0 API
            if hasattr(openai, "ChatCompletion"):
                _patch_function(openai.ChatCompletion, "create")
                _patch_function(openai.Completion, "create")

        logger.info("TrainLoop: OpenAI SDK patched successfully")
    except ImportError:
        logger.debug("OpenAI SDK not found, skipping patch")
    except Exception as e:
        logger.error(f"Failed to patch OpenAI SDK: {e}")


def _patch_anthropic() -> None:
    """Patch the Anthropic client library."""
    try:
        import anthropic

        # Check if we have the client class
        if hasattr(anthropic, "Anthropic"):
            # We can't easily monkey patch the instance methods
            # Instead, we'll patch the constructor to instrument new instances
            original_init = anthropic.Anthropic.__init__

            @functools.wraps(original_init)
            def patched_init(self, *args, **kwargs):
                result = original_init(self, *args, **kwargs)

                # Patch the instance methods
                _patch_function(self, "create_completion")
                _patch_function(self, "completions")
                _patch_function(self, "messages")

                return result

            anthropic.Anthropic.__init__ = patched_init

        logger.info("TrainLoop: Anthropic SDK patched successfully")
    except ImportError:
        logger.debug("Anthropic SDK not found, skipping patch")
    except Exception as e:
        logger.error(f"Failed to patch Anthropic SDK: {e}")


# Export type helper
traininloop_tag = TrainloopParam
