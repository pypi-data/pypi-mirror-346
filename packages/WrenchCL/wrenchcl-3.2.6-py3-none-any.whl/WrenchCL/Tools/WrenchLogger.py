import importlib
import inspect
import logging
import os
import re
import sys
import time
import json
import warnings
from datetime import datetime
from logging import Handler
from types import TracebackType
from typing import Any, Optional, Union, Literal, Type, IO, Dict, Callable
from difflib import get_close_matches
from contextlib import contextmanager
import threading

from .._Internal._MockPandas import _MockPandas
from ..Decorators.Deprecated import Deprecated
from ..Decorators.SingletonClass import SingletonClass

try:
    import pandas as pd
except ImportError:
    pd = _MockPandas()


class _ExceptionSuggestor:
    @staticmethod
    def suggest_similar(error: BaseException, frame_depth=20, n_suggestions=1, cutoff=0.6) -> Optional[str]:
        if not isinstance(error, BaseException):
            return None
        error_msg = error.args[0]
        if not error.__class__.__name__.lower() in error_msg.lower():
            error_msg = f"  {error.__class__.__name__}: {error_msg}"
        else:
            error_msg = f"  {error_msg}"

        obj_match = re.search(r"'(\w+)' object has no attribute", error_msg)
        key_match = re.search(r"has no attribute '(\w+)'", error_msg)

        if not key_match:
            return error_msg

        source_obj = obj_match.group(1) if obj_match else None
        missing_attr = key_match.group(1)

        for frame in reversed(inspect.stack()[:frame_depth]):
            for var in frame.frame.f_locals.values():
                if not hasattr(var, '__class__'):
                    continue
                if var.__class__.__name__ == source_obj:
                    keys = [k for k in dir(var) if not k.startswith('__')]
                    matches = get_close_matches(missing_attr, keys, n=n_suggestions, cutoff=cutoff)
                    if matches:
                        return f"{error_msg}\n    Did you mean: {', '.join(matches)}?\n"
        return error_msg


class _MockColorama:
    pass


class ColorPresets:
    """
    Provides color presets for common log use-cases.
    Falls back to mock colors if colorama isn't installed.
    """
    _color_class = _MockColorama
    _style_class = _MockColorama
    INFO = None
    DEBUG = None
    WARNING = None
    ERROR = None
    CRITICAL = None
    HEADER = None
    DATA = None
    BRIGHT = None
    NORMAL = None
    RESET = None
    COLOR_TRUE = None
    COLOR_FALSE = None
    COLOR_NONE = None
    COLOR_KEY = None
    COLOR_NUMBER = None

    COLOR_BRACE_OPEN = None
    COLOR_BRACE_CLOSE = None
    COLOR_BRACKET_OPEN = None
    COLOR_BRACKET_CLOSE = None
    COLOR_PAREN_OPEN = None
    COLOR_PAREN_CLOSE = None
    COLOR_COLON = None
    COLOR_COMMA = None

    _INTERNAL_DIM_COLOR = None
    _INTERNAL_DIM_STYLE = None

    def __init__(self, color, style):
        super().__setattr__('_color_class', color)
        super().__setattr__('_style_class', style)
        super().__setattr__('INFO', getattr(self._color_class, 'GREEN', ''))
        super().__setattr__('DEBUG', getattr(self._color_class, 'WHITE', ''))
        super().__setattr__('WARNING', getattr(self._color_class, 'YELLOW', ''))
        super().__setattr__('ERROR', getattr(self._color_class, 'RED', ''))
        super().__setattr__('CRITICAL', getattr(self._color_class, 'MAGENTA', ''))
        super().__setattr__('HEADER', getattr(self._color_class, 'CYAN', ''))
        super().__setattr__("DATA", getattr(self._color_class, 'BLUE', ''))

        super().__setattr__('BRIGHT', getattr(self._style_class, 'BRIGHT', ''))
        super().__setattr__('NORMAL', getattr(self._style_class, 'NORMAL', ''))
        super().__setattr__('RESET', getattr(self._style_class, 'RESET_ALL', ''))

        # Literal colors
        super().__setattr__('COLOR_TRUE', getattr(self._color_class, 'GREEN', ''))
        super().__setattr__('COLOR_FALSE', getattr(self._color_class, 'RED', ''))
        super().__setattr__('COLOR_NONE', getattr(self._color_class, 'WHITE', ''))
        super().__setattr__('COLOR_KEY', getattr(self._color_class, '', ''))
        super().__setattr__('COLOR_NUMBER', getattr(self._color_class, 'YELLOW', ''))

        # Syntax colors
        super().__setattr__('COLOR_BRACE_OPEN', getattr(self._color_class, 'CYAN', ''))     # {
        super().__setattr__('COLOR_BRACE_CLOSE', getattr(self._color_class, 'CYAN', ''))    # }
        super().__setattr__('COLOR_BRACKET_OPEN', getattr(self._color_class, 'BLUE', ''))      # [
        super().__setattr__('COLOR_BRACKET_CLOSE', getattr(self._color_class, 'BLUE', ''))     # ]
        super().__setattr__('COLOR_PAREN_OPEN', getattr(self._color_class, 'BLUE', ''))        # (
        super().__setattr__('COLOR_PAREN_CLOSE', getattr(self._color_class, 'BLUE', ''))       # )
        super().__setattr__('COLOR_COLON', getattr(self._color_class, 'MAGENTA', ''))           # :
        super().__setattr__('COLOR_COMMA', getattr(self._color_class, 'MAGENTA', ''))            # ,

        super().__setattr__('_INTERNAL_DIM_COLOR', getattr(self._color_class, 'WHITE', ''))
        super().__setattr__('_INTERNAL_DIM_STYLE', getattr(self._style_class, 'DIM', ''))

    def __setattr__(self, name, value):
        allowed_color_values = [val.lower() for val in self._color_class.__dict__.values() if val != 'RESET']
        allowed_style_values = [val.lower() for val in self._style_class.__dict__.values() if val != 'RESET_ALL']
        allowed_names = [val.lower() for val in self.__dict__.keys() if val != 'RESET']

        if not name.lower() in allowed_names:
            raise ValueError(f"Invalid name for '{name}': {name}. Allowed names: {allowed_names}")

        if name.lower() in allowed_color_values:
            value = getattr(self._color_class, value.upper())
        elif name.lower() in allowed_style_values:
            value = getattr(self._style_class, value.upper())
        else:
            raise ValueError(
                f"Invalid value for '{name}': {value}. Allowed values: {allowed_color_values + allowed_style_values}")

        name = name.upper()
        super().__setattr__(name, value)

    def get_color_by_level(self, level: Union[str, int]):
        if isinstance(level, int):
            str_name = logging.getLevelName(level)
        else:
            str_name = level.upper()
        if str_name == 'INTERNAL':
            return self._INTERNAL_DIM_COLOR
        return getattr(self, str_name, '')


    def get_level_style(self, level: Union[str, int]):
        if isinstance(level, int):
            str_name = logging.getLevelName(level)
        else:
            str_name = level.upper()
        if str_name in ['INFO', 'DEBUG']:
            return self.NORMAL
        elif str_name in ['WARNING', 'ERROR', 'CRITICAL', 'HEADER']:
            return self.BRIGHT
        elif str_name == 'INTERNAL':
            return self._INTERNAL_DIM_STYLE
        else:
            return self.NORMAL

    def get_message_color(self, level: Union[str, int]):
        if isinstance(level, int):
            str_name = logging.getLevelName(level)
        else:
            str_name = level.upper()
        if str_name in ['CRITICAL', 'ERROR']:
            return getattr(self, str_name, '')
        else:
            return ''


    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_demo_string(self):
        demo_string = "\n  • Log Level Color Preview:\n"
        demo_string += f"    {self.DEBUG}{self.get_level_style('DEBUG')}[DEBUG] Debug message preview{self.RESET}\n"
        demo_string += f"    {self.INFO}{self.get_level_style('INFO')}[INFO] Info message preview{self.RESET}\n"
        demo_string += f"    {self.WARNING}{self.get_level_style('WARNING')}[WARNING] Warning message preview{self.RESET}\n"
        demo_string += f"    {self.ERROR}{self.get_level_style('ERROR')}[ERROR] Error message preview{self.RESET}\n"
        demo_string += f"    {self.CRITICAL}{self.get_level_style('CRITICAL')}[CRITICAL] Critical message preview{self.RESET}\n"
        demo_string += f"    {self.HEADER}{self.get_level_style('HEADER')}[HEADER] Section header example{self.RESET}\n"
        demo_string += f"    {self.DATA}{self.get_level_style('DATA')}[DATA] Structured data printout{self.RESET}\n"

        demo_string += "  • Literal/Syntax Highlight Preview:\n"
        demo_string += f"    - true → {self.COLOR_TRUE}{self.BRIGHT}true{self.RESET}\n"
        demo_string += f"    - false → {self.COLOR_FALSE}{self.BRIGHT}false{self.RESET}\n"
        demo_string += f"    - none → {self.COLOR_NONE}{self.BRIGHT}None{self.RESET}\n"
        demo_string += f"    - \"key\": → {self.COLOR_KEY}{self.BRIGHT}\"key\"{self.RESET}{self.COLOR_COLON}:{self.RESET}\n"
        demo_string += f"    - 123 → {self.COLOR_NUMBER}123{self.RESET}\n"
        demo_string += f"    - {{ }} → {self.COLOR_BRACE_OPEN}{{{self.RESET} content {self.COLOR_BRACE_CLOSE}}}{self.RESET}\n"
        demo_string += f"    - [ ] → {self.COLOR_BRACKET_OPEN}[{self.RESET} content {self.COLOR_BRACKET_CLOSE}]{self.RESET}\n"
        demo_string += f"    - ( ) → {self.COLOR_PAREN_OPEN}({self.RESET} content {self.COLOR_PAREN_CLOSE}){self.RESET}\n"
        demo_string += f"    - {self.COLOR_KEY}{self.BRIGHT}key{self.RESET}{self.COLOR_COLON}:{self.RESET}value{self.COLOR_COMMA},{self.RESET}\n"

        return demo_string


class _CustomFormatter(logging.Formatter):
    def __init__(self, fmt: str, datefmt: Optional[str], presets: ColorPresets):
        super().__init__(fmt, datefmt)
        self.presets = presets

    def formatStack(self, exc_info: str) -> str:
        dim_color = self.presets._INTERNAL_DIM_COLOR or ''
        dim_style = self.presets._INTERNAL_DIM_STYLE or ''
        reset = self.presets.RESET or ''
        return f"{dim_color}{dim_style}{exc_info}{reset}"

    def formatException(self, ei) -> str:
        original = super().formatException(ei)
        dim_color = self.presets._INTERNAL_DIM_COLOR or ''
        dim_style = self.presets._INTERNAL_DIM_STYLE or ''
        reset = self.presets.RESET or ''
        return f"{dim_color}{dim_style}{original}{reset}"


class _JSONLogFormatter(logging.Formatter):
    def __init__(self, env_metadata: dict, forced_color: bool, highlight_func: Callable):
        super().__init__()
        self.env_metadata = env_metadata
        self.color_mode = forced_color
        self.highlight_func = highlight_func


    def _extract_generic_context(self) -> dict:
        """
        Scan all active ContextVars for common keys like user_id, client_id, or organization_id.
        Supports deeply nested dicts and custom objects.
        """


        context_data = {}
        user_keys = {'user_id', 'usr_id', 'entity_id', 'user_entity_id'}
        org_keys = {'client_id', 'org_id', 'organization_id'}

        def scan_dict(d: dict):
            found = {}
            try:
                for k, v in d.items():
                    key_lower = k.lower()
                    if key_lower in user_keys:
                        found['user_id'] = v
                    elif key_lower in org_keys:
                        found['organization_id'] = v
                    elif isinstance(v, dict):
                        found.update(scan_dict(v))
                    elif hasattr(v, '__dict__'):
                        found.update(scan_dict(vars(v)))
            finally:
                return found

        try:
            import contextvars
            ctx = contextvars.copy_context()
            for var in ctx:
                val = var.get()
                if isinstance(val, dict):
                    context_data.update(scan_dict(val))
                elif hasattr(val, '__dict__'):
                    context_data.update(scan_dict(vars(val)))
        finally:
            return context_data



    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "level": record.levelname,
            "logger": record.name,
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),

            # Required for Datadog log correlation
            "dd.env": self.env_metadata.get("env"),
            "dd.service": self.env_metadata.get("project"),
            "dd.version": self.env_metadata.get("project_version"),
            "dd.trace_id": str(getattr(record, "dd.trace_id", "")),
            "dd.span_id": str(getattr(record, "dd.span_id", "")),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        ctx = self._extract_generic_context()
        if len(ctx) > 0:
            log_record.update(ctx)

        dumped_json = json.dumps(log_record, default=str, ensure_ascii=False)

        if self.color_mode:
            dumped_json = self.highlight_func(dumped_json, True)

        return dumped_json

_exc_info_type = None | bool | tuple[Type[BaseException], BaseException, TracebackType | None] | tuple[
    None, None, None] | BaseException


class _BaseLogger:
    """
    WrenchCL's structured, colorized, and extensible logger.

    Features:
    ---------
    • Structured formatting with optional syntax highlighting for Python/JSON-style literals.
    • Multiple output modes: 'terminal' (colored), 'json' (infra-readable), 'compact' (minimal).
    • Datadog APM correlation (trace_id, span_id) via ddtrace integration.
    • Colorized output with environment-aware fallback (e.g., AWS Lambda disables color).
    • Smart exception suggestion engine for attribute errors.
    • Thread-safe across logging, handler updates, and reconfiguration.
    • Singleton-safe with `_logger_()` for consistent usage across modules.

    Initialization:
    ---------------
    - On instantiation, the logger performs:
        1. Stream handler setup (`__setup`)
        2. Environment-aware configuration refresh (`reinitialize`)
    - All runtime changes to env vars (COLOR_MODE, LOG_DD_TRACE, etc.) should be followed by `reinitialize()`.

    Environment Variables:
    ----------------------
    - COLOR_MODE: "true" or "false" (defaults to true unless on Lambda)
    - LOG_DD_TRACE: "true" or "false" to enable Datadog trace injection
    - ENV, PROJECT_NAME, PROJECT_VERSION: Used in prefix metadata (optional)

    Usage Example:
    --------------
    ```python
    from WrenchCL.Tools import logger

    logger.info("Starting job...")
    logger.error("Something failed", exc_info=True)

    # Runtime config switch
    logger.configure(mode="json", trace_enabled=True)
    ```

    To force colors and JSON highlighting in CI:
    ```python
    logger.force_markup()
    ```
    """


    def __init__(self, level: str = 'INFO') -> None:
        # Thread safety lock

        self.__lock = threading.RLock()
        self.__logger_instance = logging.getLogger('WrenchCL')
        # Basic logger state
        self.__global_stream_configured = False
        self.__force_markup = False
        self.__initialized = False
        self.run_id = self.__generate_run_id()
        self.__base_level = 'DEBUG'

        # Mode flags (simplified to a single dictionary)
        self.__config = {
            'mode': 'terminal',      # 'terminal', 'json', or 'compact'
            'highlight_syntax': True,
            'verbose': False,
            'deployed': False,
            'dd_trace_enabled': False,
            'color_enabled': True
        }

        # Initialize objects
        self.__start_time = None
        self.__dd_log_flag = False
        self.presets = ColorPresets(None, None)
        self.__env_metadata = self.__fetch_env_metadata()

        # Read environment variables
        self.__config['dd_trace_enabled'] = os.environ.get("LOG_DD_TRACE", "false").lower() == "true"
        self.__config['color_enabled'] = os.environ.get("COLOR_MODE", "true").lower() == "true"

        # Set up logger instance
        self.__setup()
        self.reinitialize()
        self._internal_log(f"Logger -> Color:{self.__config['color_enabled']} | Mode:{self.presets.COLOR_BRACE_OPEN}{self.__config['mode'].capitalize()}{self.presets.RESET} | Deployment:{self.__config['deployed']}")

    # ---------------- Public Configuration API ----------------

    def configure(self,
                  mode: Optional[Literal['terminal', 'json', 'compact']] = None,
                  level: Optional[str] = None,
                  color_enabled: Optional[bool] = None,
                  highlight_syntax: Optional[bool] = None,
                  verbose: Optional[bool] = None,
                  trace_enabled: Optional[bool] = None,
                  deployment_mode: Optional[bool] = None,
                  suppress_autoconfig: bool = False) -> None:
        """
        Centralized configuration method to set multiple options at once.

        :param mode: Output mode - 'terminal' (human readable), 'json' (for infrastructure), 'compact' (for scripts)
        :param level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        :param color_enabled: Whether to use ANSI colors
        :param verbose: Enable detailed context information
        :param trace_enabled: Enable Datadog trace ID injection
        :param deployment_mode: Whether to use deployment mode (e.g., Lambda) disable color and enable json output
        :param highlight_syntax: Whether to highlight syntax, set to true when enabling color, set to false when disabling color initially set to true if color is enabled
        """

        with self.__lock:
            if not suppress_autoconfig:
                self.__check_deployment()
            if mode is not None:
                self.__config['mode'] = mode
            if highlight_syntax is not None:
                self.__config['highlight_syntax'] = highlight_syntax
            if level is not None:
                self.setLevel(level)
            if color_enabled is not None:
                self.__config['color_enabled'] = color_enabled
            if verbose is not None:
                self.__config['verbose'] = verbose
            if deployment_mode is not None:
                self.__config['deployed'] = deployment_mode
            if trace_enabled is not None:
                self.__config['dd_trace_enabled'] = trace_enabled
                try:
                    import ddtrace
                    ddtrace.patch(logging=True)
                    self._internal_log("Datadog trace injection enabled via ddtrace.patch(logging=True)")
                    os.environ["DD_TRACE_ENABLED"] = "true"
                except ImportError:
                    self.__config['dd_trace_enabled'] = False
                    self._internal_log("   Datadog trace injection disabled: `ddtrace` module not available.")
            if self.__config.get('dd_trace_enabled') and self.__config['mode'] != 'json':
                self._internal_log("   Trace injection requested, but trace_id/span_id only appear in JSON mode.")
            self.__check_color()
            self.__env_metadata = self.__fetch_env_metadata()

    def reinitialize(self, verbose = False):
        """
        Re-applies all environment-variable-driven settings (e.g., COLOR_MODE, LOG_DD_TRACE, ENV).

        This method refreshes internal flags such as deployment mode, color mode, and metadata
        without reinitializing logger handlers. Call this if env vars are updated at runtime.
        """
        with self.__lock:
            self.__check_deployment(verbose)
            self.__check_color()
            self.__env_metadata = self.__fetch_env_metadata()
            if verbose:
                self._internal_log(json.dumps(self.logger_state, indent=2, default=lambda x: str(x), ensure_ascii=False))

    def update_color_presets(self, **kwargs) -> None:
        """Update color presets for log levels and syntax highlighting."""
        with self.__lock:
            self.presets.update(**kwargs)

    def setLevel(self, level: Literal["DEBUG", "INFO", 'WARNING', 'ERROR', 'CRITICAL']) -> None:
        """Set the logging level for this logger."""
        with self.__lock:
            self.flush_handlers()
            self.__logger_instance.setLevel(self.__get_level(level))

    def initiate_new_run(self):
        """Generate a new run ID for this logger instance."""
        with self.__lock:
            self.run_id = self.__generate_run_id()

    # ---------------- Core Logging Methods ----------------

    def info(self, *args, exc_info: _exc_info_type = None, **kwargs) -> None:
        """
        Logs an INFO-level message.

        :param args: Strings or objects to log
        :param exc_info: Optional exception info
        :param no_format: If True, disables structured formatting
        """
        self.__log(logging.INFO, *args, exc_info=exc_info, **kwargs)

    def warning(self, *args, exc_info: _exc_info_type = None, **kwargs) -> None:
        """
        Logs a WARNING-level message.

        :param args: Strings or objects to log
        :param exc_info: Optional exception info
        :param no_format: If True, disables structured formatting
        """
        self.__log(logging.WARNING, *args, exc_info=exc_info, **kwargs)

    def error(self, *args, exc_info: _exc_info_type = True, **kwargs) -> None:
        """
        Logs an ERROR-level message.

        :param args: Strings or objects to log
        :param exc_info: Exception info (defaults to True)
        :param no_format: If True, disables structured formatting
        """
        self.__log(logging.ERROR, *args, exc_info=exc_info, **kwargs)

    def critical(self, *args, exc_info: _exc_info_type = None, **kwargs) -> None:
        """
        Logs a CRITICAL-level message.

        :param args: Strings or objects to log
        :param exc_info: Optional exception info
        :param no_format: If True, disables structured formatting
        """
        self.__log(logging.CRITICAL, *args, exc_info=exc_info, **kwargs)

    def debug(self, *args, exc_info: _exc_info_type = None, **kwargs) -> None:
        """
        Logs a DEBUG-level message.

        :param args: Strings or objects to log
        :param exc_info: Optional exception info
        :param no_format: If True, disables structured formatting
        """
        self.__log(logging.DEBUG, *args, exc_info=exc_info, **kwargs)

    def exception(self, *args, exc_info: _exc_info_type = True, **kwargs) -> None:
        """
        Logs an ERROR-level message with exception info.

        :param args: Strings or objects to log
        :param exc_info: Exception info (defaults to True)
        :param no_format: If True, disables structured formatting
        """
        self.__log(logging.ERROR, *args, exc_info=exc_info, **kwargs)

    def _internal_log(self, *args) -> None:
        """Internal logging method for logger infrastructure messages."""
        self.__log(logging.WARNING, *args, color_flag="INTERNAL")

    # ---------------- Additional Logging Features ----------------

    def start_time(self) -> None:
        """
        Starts or resets the internal timer for measuring elapsed time.
        """
        self.__start_time = time.time()

    def log_time(self, message="Elapsed time") -> None:
        """
        Logs the time elapsed since the last `start_time()` checkpoint.

        :param message: Prefix message to display alongside elapsed duration.
        """
        if self.__start_time:
            elapsed = time.time() - self.__start_time
            self.info(f"{message}: {elapsed:.2f}s")

    def header(self, text: str, size:int =None, compact=False) -> None:
        """
        Logs a stylized section header.

        :param text: The header text
        :param size: Width of the line used to center the header
        :param compact: If True, uses a single-line compact format
        """
        text = text.replace('_', ' ').replace('-', ' ').strip().capitalize()
        if compact or self.__config['mode'] == 'compact':
            size = size or 40
            formatted = self.__apply_color(text, self.presets.HEADER).center(size, "-")
        else:
            size = size or 80
            formatted = "\n" + self.__apply_color(text, self.presets.HEADER).center(size, "-")
        self.__log("INFO", formatted, no_format=True, no_color=True)

    def pretty_log(self, obj: Any, indent=4, **kwargs) -> None:
        """
        Logs a prettified version of an object (dict, model, DataFrame, etc).

        :param obj: Any printable object
        :param indent: Indentation level for structured formats
        :param kwargs: Passed through to serialization methods
        """
        try:
            if isinstance(obj, pd.DataFrame):
                prefix_str = f"DataType: {type(obj).__name__} | Shape: {obj.shape[0]} rows | {obj.shape[1]} columns"
                pd.set_option(
                    'display.max_rows', 500,
                    'display.max_columns', None,
                    'display.width', None,
                    'display.max_colwidth', 50,
                    'display.colheader_justify', 'center'
                )
                output = str(obj)
            elif hasattr(obj, 'pretty_print'):
                output = obj.pretty_print(**kwargs)
            elif hasattr(obj, 'model_dump_json'):
                output = obj.model_dump_json(indent=indent, **kwargs)
            elif hasattr(obj, 'dump_json_schema'):
                output = obj.dump_json_schema(indent=indent, **kwargs)
            elif hasattr(obj, 'json'):
                output = json.dumps(obj.json(), indent=indent, ensure_ascii=False, **kwargs)
            elif isinstance(obj, dict):
                output = json.dumps(obj, indent=indent, ensure_ascii=False, **kwargs)
            elif isinstance(obj, str):
                try:
                    output = json.dumps(json.loads(obj), indent=indent, ensure_ascii=False, **kwargs, default=str)
                except Exception:
                    output = str(obj)
            else:
                output = str(obj)
        except Exception:
            output = str(obj)
        self.__log(logging.INFO, output, exc_info=False, color_flag="DATA")

    # ---------------- Resource Management ----------------

    def flush_handlers(self):
        """
        Thread-safe method to flush all handlers associated with the logger instance.
        """
        with self.__lock:
            for h in self.__logger_instance.handlers:
                try:
                    h.flush()
                except Exception:
                    pass

    def close(self):
        """
        Properly closes all handlers and releases resources.
        Should be called during application shutdown.
        """
        with self.__lock:
            self.flush_handlers()
            for handler in list(self.__logger_instance.handlers):
                try:
                    handler.close()
                    self.__logger_instance.removeHandler(handler)
                except Exception as e:
                    # Log failure but continue with remaining handlers
                    sys.stderr.write(f"Error closing handler: {str(e)}\n")

            # If we've configured global logging, clean that up too
            if self.__global_stream_configured:
                root_logger = logging.getLogger()
                for handler in list(root_logger.handlers):
                    try:
                        handler.close()
                        root_logger.removeHandler(handler)
                    except Exception:
                        pass

    # ---------------- Handler Management ----------------

    def add_new_handler(
        self,
        handler_cls: Type[logging.Handler] = logging.StreamHandler,
        stream: Optional[IO[str]] = None,
        level: Union[str, int] = None,
        formatter: Optional[logging.Formatter] = None,
        force_replace: bool = False,
    ) -> logging.Handler:
        """
        Adds a new logging handler to the WrenchCL logger.

        :param handler_cls: Handler class (StreamHandler, FileHandler, etc.)
        :param stream: Required for StreamHandler
        :param level: Log level for this handler
        :param formatter: Optional custom formatter
        :param force_replace: If True, removes existing handlers
        :return: The newly added handler
        """
        with self.__lock:
            if not level:
                level = self.__base_level

            level = self.__get_level(level)

            if issubclass(handler_cls, logging.StreamHandler):
                if stream is None:
                    raise ValueError("StreamHandler requires a valid `stream` argument.")
                handler = handler_cls(stream)
            else:
                handler = handler_cls()

            handler.setLevel(level)

            if not formatter:
                formatter = self.__get_formatter(level)
            handler.setFormatter(formatter)

            if force_replace:
                self.__logger_instance.handlers = []

            self.__logger_instance.addHandler(handler)
            return handler

    def add_rotating_file_handler(
        self,
        filename: str,
        max_bytes: int = 10485760,  # 10MB default
        backup_count: int = 5,
        level: Union[str, int] = None,
        formatter: Optional[logging.Formatter] = None,
    ) -> logging.Handler:
        """
        Adds a rotating file handler with the specified parameters.

        :param filename: Path to the log file
        :param max_bytes: Maximum size in bytes before rollover (default 10MB)
        :param backup_count: Number of backup files to keep (default 5)
        :param level: Logging level for this handler
        :param formatter: Optional custom formatter
        :return: The configured RotatingFileHandler
        """
        try:
            from logging.handlers import RotatingFileHandler
        except ImportError:
            self.error("Rotating file handler requires Python's logging.handlers module")
            return None

        with self.__lock:
            handler = RotatingFileHandler(
                filename=filename,
                maxBytes=max_bytes,
                backupCount=backup_count,
                delay=True  # Only create file when first log written
            )

            if not level:
                level = self.__base_level
            handler.setLevel(self.__get_level(level))

            if not formatter:
                formatter = self.__get_formatter(level)
            handler.setFormatter(formatter)

            self.__logger_instance.addHandler(handler)
            return handler

    # ---------------- Global Configuration ----------------

    def configure_global_stream(self, level: str = "INFO", silence_others: bool = False, stream = sys.stdout) -> None:
        """
        Configures the root logger to use WrenchCL formatting.

        :param level: Log level for the global handler
        :param silence_others: If True, silences all other loggers
        :param stream: Output stream (defaults to stdout)
        """
        with self.__lock:
            self.flush_handlers()
            root_logger = logging.getLogger()
            root_logger.setLevel(self.__base_level)

            handler = self.add_new_handler(
                logging.StreamHandler,
                stream=stream,
                level=level,
                force_replace=True
            )
            root_logger.handlers = [handler]
            root_logger.propagate = False

            if silence_others:
                self.silence_other_loggers()

            self.__global_stream_configured = True

        # Log outside the lock
        self.info(" Global stream configured successfully.")

    def silence_logger(self, logger_name: str, level: Optional[int] = None) -> None:
        """
        Silences a specific logger by attaching a NullHandler.

        :param logger_name: Name of the logger to silence
        :param level: Optional override level
        """
        with self.__lock:
            logger = logging.getLogger(logger_name)
            for h in logger.handlers:
                h.flush()
            logger.handlers = [logging.NullHandler()]
            if not level:
                logger.setLevel(logging.CRITICAL + 1)
            else:
                logger.setLevel(level)
            logger.propagate = False

    def silence_other_loggers(self, level: Optional[int] = None) -> None:
        """
        Silences all non-WrenchCL loggers.

        :param level: Optional override level
        """
        for name in logging.root.manager.loggerDict:
            if name != 'WrenchCL':
                self.silence_logger(name, level)

    def force_markup(self) -> None:
        """
        Enables ANSI styling and literal highlighting even in non-TTY environments (e.g., CI, Docker) and JSON output mode.
        """
        try:
            with self.__lock:
                import colorama
                self.__force_markup = True
                self.enable_color()
                colorama.deinit()
                colorama.init(strip=False, convert=False)
                sys.stdout = colorama.AnsiToWin32(sys.stdout).stream
                sys.stderr = colorama.AnsiToWin32(sys.stderr).stream
                if self.__force_markup and self.__config['deployed']:
                    warnings.warn("Forcing Markup in deployment mode is not recommended and will cause issues in external parsers like cloudwatch and Datadog", category=RuntimeWarning, stacklevel=5)
                # Update color presets and reconfigure formatters
                self.presets = ColorPresets(self._Color, self._Style)
                self.flush_handlers()
                if self.__config['mode'] == 'json':
                    self.__use_json_logging()
                else:
                    for handler in self.__logger_instance.handlers:
                        handler.setFormatter(self.__get_formatter(self.__logger_instance.level))

                if self.__global_stream_configured:
                    root_logger = logging.getLogger()
                    for handler in root_logger.handlers:
                        handler.setFormatter(self.__get_formatter(root_logger.level))

            self.info("Forced color output enabled.")
        except ImportError:
            self.warning("Colorama is not installed; cannot force color output.")

    def enable_color(self):
        """Enable ANSI color output if colorama is available."""
        try:
            with self.__lock:
                colorama = importlib.import_module("colorama")
                self.__config['color_enabled'] = True
                self.__config['highlight_syntax'] = True if self.__config['highlight_syntax'] is not False else False
                self._Color = colorama.Fore
                self._Style = colorama.Style
                self.presets = ColorPresets(self._Color, self._Style)
                colorama.deinit()
                colorama.init(strip=False, autoreset=False)
        except ImportError:
            self._internal_log("Colorama not installed. Cannot enable color output.")
            self.disable_color()

    def disable_color(self):
        """Disable ANSI color output."""
        with self.__lock:
            self._Color = _MockColorama
            self._Style = _MockColorama
            self.__config['color_enabled'] = False
            self.__config['highlight_syntax'] = False
            try:
                colorama = importlib.import_module("colorama")
                colorama.deinit()
            except ImportError:
                pass
            self.presets = ColorPresets(self._Color, self._Style)

    def display_logger_state(self) -> None:
        """
        Logs the current logger configuration and formatting settings.
        """
        self.__log_setup_summary()

    # ---------------- Context Manager ----------------

    @contextmanager
    def config_context(self, **kwargs):
        """
        Context manager for temporarily changing logger configuration.

        Example:
            with logger.config_context(mode='compact', level="DEBUG"):
                logger.debug("This will be logged in compact mode at DEBUG level")

        :param kwargs: Configuration parameters to change
        """
        with self.__lock:
            # Save original values
            original_values = {}

            # Special handling for 'level'
            if 'level' in kwargs:
                original_values['level'] = self.level
                self.setLevel(kwargs.pop('level'))

            # Handle all other attributes via the configure method
            if kwargs:
                attrs_map = {
                    'mode': 'mode',
                    'color_enabled': 'color_enabled',
                    'verbose': 'verbose',
                    'trace_enabled': 'dd_trace_enabled',
                    'highlight_syntax': 'highlight_syntax',
                    'deployed': 'deployed',
                }

                config_args = {}
                for key, value in kwargs.items():
                    if key in attrs_map:
                        mapped_key = attrs_map[key]
                        original_values[mapped_key] = self.__config.get(mapped_key)
                        config_args[key] = value

                # Apply the temporary configuration
                if config_args:
                    self.configure(**config_args)

        try:
            # Yield control back to the with block
            yield
        finally:
            # Restore original values
            with self.__lock:
                # Restore level if it was changed
                if 'level' in original_values:
                    self.setLevel(original_values.pop('level'))

                # Restore other configs that were changed
                restore_args = {}
                for attr, value in original_values.items():
                    if attr == 'mode':
                        restore_args['mode'] = value
                    elif attr == 'color_enabled':
                        restore_args['color_enabled'] = value
                    elif attr == 'verbose':
                        restore_args['verbose'] = value
                    elif attr == 'dd_trace_enabled':
                        restore_args['trace_enabled'] = value

                if restore_args:
                    self.configure(**restore_args)

    # ---------------- Properties (SIMPLIFIED) ----------------

    @property
    def mode(self) -> str:
        """
        Get the current logging mode.

        Returns one of:
        - 'terminal': Human-readable colored output
        - 'json': Machine-readable structured output
        - 'compact': Minimal single-line output
        """
        return self.__config.get('mode', 'terminal')

    @property
    def level(self) -> str:
        """Get the current logging level."""
        return logging.getLevelName(self.__logger_instance.level)

    @property
    def logger_instance(self) -> logging.Logger:
        """Get the underlying logger instance."""
        return self.__logger_instance

    @property
    def handlers(self) -> list[Handler]:
        """Get the current handlers."""
        return self.__logger_instance.handlers

    @property
    def logger_state(self) -> dict:
        """
        Get a complete summary of the logger's current state.
        """
        return {
            "Logging Level": self.level,
            "Run Id": self.run_id,
            "Mode": self.__config['mode'],
            "Environment Metadata": self.__env_metadata,
            "Configuration": {
                "Color Enabled": self.__config['color_enabled'],
                "Highlight Syntax": self.__config['highlight_syntax'],
                "Verbose": self.__config['verbose'],
                "Deployment Mode": self.__config['deployed'],
                "DD Trace Enabled": self.__config['dd_trace_enabled'],
                "Global Stream Configured": self.__global_stream_configured
            },
            "Handlers": [type(h).__name__ for h in self.__logger_instance.handlers],
        }

    @property
    def color_presets(self) -> ColorPresets:
        """Returns the active ColorPresets object used for ANSI styling."""
        return self.presets

    @property
    def highlight_syntax(self) -> bool:
        """Whether syntax highlighting for literals is enabled."""
        return self.__config['highlight_syntax']

    # ---------------- Internals ----------------

    def __log(self, level: Union[int, str], *args: str, exc_info: _exc_info_type = None,
              color_flag: Optional[Literal['INTERNAL', 'DATA']] = None, **kwargs) -> None:
        """Thread-safe logging implementation."""
        args = list(args)
        for idx, a in enumerate(args):
            if isinstance(a, Exception) or isinstance(a, BaseException):
                exc_info = args.pop(idx)

        if self.__config['mode'] == 'terminal':
            suggestion = self.__suggest_exception(exc_info)
            if suggestion:
                suggestion = f"{self.presets.ERROR}{suggestion}{self.presets.RESET}"
                args.append(suggestion)

        args = tuple(args)
        msg = '\n'.join(str(arg) for arg in args)

        if self.__config['highlight_syntax'] and self.__config['color_enabled'] and not self.__config['mode'] == 'json':
            msg = self.__highlight_literals(msg, data=color_flag == 'DATA')

        # Format based on mode
        if self.__config['mode'] == 'compact' or self.__config['deployed'] or self.__config['mode'] == 'json':
            lines = msg.splitlines()
            msg = ' '.join([line.strip() for line in lines if len(line.strip()) > 0])
            msg = msg.replace('\n', ' ').replace('\r', '').strip()

        if color_flag == 'INTERNAL':
            level = "INTERNAL"
        elif color_flag == 'DATA':
            level = "DATA"

        # Use lock for handler configuration
        with self.__lock:
            self.flush_handlers()
            for handler in self.__logger_instance.handlers:
                if not isinstance(handler, logging.NullHandler):
                    handler.setFormatter(self.__get_formatter(
                        level,
                        no_format=kwargs.get('no_format', False)
                    ))

            # Process multi-line messages
            lines = msg.splitlines()
            if len(lines) > 1:
                msg = "    " + "\n    ".join(lines)
            if exc_info:
                msg = "\n".join(lines)

            if isinstance(level, str):
                level = self.__get_level(level)
        # Actual logging outside the lock to prevent deadlocks
        self.__logger_instance.log(
            level,
            msg,
            exc_info=exc_info,
            stack_info=kwargs.get('stack_info', False),
            stacklevel=self.__get_depth(internal = color_flag == 'INTERNAL')
        )

    def __highlight_literals(self, msg: str, data: bool = False) -> str:
        """Add syntax highlighting to literals in log messages."""
        if self.__force_markup:
            pass
        elif not self.__config['color_enabled'] or not self.__config['highlight_syntax'] or self.__config['deployed']:
            return msg

        c = self.presets

        # Boolean/None literals — match as full words
        msg = re.sub(r'\btrue\b', lambda m: f"{c.COLOR_TRUE}{c.BRIGHT}{m.group(0)}{c.RESET}", msg, flags=re.IGNORECASE)
        msg = re.sub(r'\bfalse\b', lambda m: f"{c.COLOR_FALSE}{c.BRIGHT}{m.group(0)}{c.RESET}", msg, flags=re.IGNORECASE)
        msg = re.sub(r'\bnone\b', lambda m: f"{c.COLOR_NONE}{c.BRIGHT}{m.group(0)}{c.RESET}", msg, flags=re.IGNORECASE)
        msg = re.sub(r'\bnull\b', lambda m: f"{c.COLOR_NONE}{c.BRIGHT}{m.group(0)}{c.RESET}", msg, flags=re.IGNORECASE)
        msg = re.sub(r'\bnan\b', lambda m: f"{c.COLOR_NONE}{c.BRIGHT}{m.group(0)}{c.RESET}", msg, flags=re.IGNORECASE)
        if data and not self.__config['mode'] == 'json':
            msg = self.__highlight_data(msg)
        if self.__config['mode'] == 'json' and self.__force_markup:
            msg = self.__highlight_literals_json(msg)

        return msg

    def __highlight_literals_json(self, msg: str) -> str:
        c = self.presets

        # Highlight log level terms
        level_keywords = {
            "DEBUG": c.DEBUG,
            "INFO": c.INFO,
            "WARNING": c.WARNING,
            "WARN": c.WARNING,
            "ERROR": c.ERROR,
            "CRITICAL": c.CRITICAL
        }
        for keyword, color in level_keywords.items():
            msg = re.sub(
                rf'\b{keyword}\b',
                lambda m: f"{color}{c.BRIGHT}{m.group(0)}{c.RESET}",
                msg,
                flags=re.IGNORECASE
            )

        # Highlight JSON-style keys (with optional whitespace before colon)
        msg = re.sub(
            r'(?P<key>"[^"]+?")(?P<colon>\s*:)',
            lambda m: f"{c.COLOR_NUMBER}{c.BRIGHT}{m.group('key')}{c.RESET}{c.COLOR_COLON}{m.group('colon')}{c.RESET}",
            msg
        )

        # Highlight numbers
        msg = re.sub(
            r'(?<=\s)(-?\d+(\.\d+)?)(?=\s|[,|\]])',
            lambda m: f"{c.COLOR_KEY}{m.group(1)}{c.RESET}",
            msg
        )

        # Highlight brackets, braces, commas, colons
        msg = msg.replace('{', f"{c.COLOR_BRACE_OPEN}{{{c.RESET}")
        msg = msg.replace('}', f"{c.COLOR_BRACE_CLOSE}}}{c.RESET}")
        msg = msg.replace('(', f"{c.COLOR_PAREN_OPEN}({c.RESET}")
        msg = msg.replace(')', f"{c.COLOR_PAREN_CLOSE}){c.RESET}")
        msg = msg.replace(':', f"{c.COLOR_COLON}:{c.RESET}")
        msg = msg.replace(',', f"{c.COLOR_COMMA},{c.RESET}")

        # Brackets: only color when at line-start or line-end to avoid nested breakage
        msg = re.sub(r'(?<=\n)(\s*)\[', lambda m: f"{m.group(1)}{c.COLOR_BRACKET_OPEN}[{c.RESET}", msg)
        msg = re.sub(r'\](?=\n)', lambda m: f"{c.COLOR_BRACKET_CLOSE}]{c.RESET}", msg)

        return msg


    def __highlight_data(self, msg):
        # Match string keys (only if followed by colon)
        c = self.presets
        msg = re.sub(
            r'(?P<key>"[^"]+?")(?P<colon>\s*:)',  # `"key":` only
            lambda m: f"{c.INFO}{c.BRIGHT}{m.group('key')}{c.RESET}{c.COLOR_COLON}{m.group('colon')}{c.RESET}",
            msg
        )

        # Match standalone integers (not quoted, surrounded by whitespace or symbols)
        msg = re.sub(
            r'(?<=\s)(\d+)(?=\s|[,|\]])',  # match int if followed by space, comma, or ]
            lambda m: f"{c.COLOR_NUMBER}{m.group(1)}{c.RESET}",
            msg
        )

        # Brackets, braces, parens
        msg = msg.replace('{', f"{c.COLOR_BRACE_OPEN}{{{c.RESET}")
        msg = msg.replace('}', f"{c.COLOR_BRACE_CLOSE}}}{c.RESET}")
        msg = msg.replace('(', f"{c.COLOR_PAREN_OPEN}({c.RESET}")
        msg = msg.replace(')', f"{c.COLOR_PAREN_CLOSE}){c.RESET}")
        msg = msg.replace(':', f"{c.COLOR_COLON}:{c.RESET}")
        msg = msg.replace(',', f"{c.COLOR_COMMA},{c.RESET}")

        # Brackets: only color when at line-start or line-end to avoid nested breakage
        msg = re.sub(r'(?<=\n)(\s*)\[', lambda m: f"{m.group(1)}{c.COLOR_BRACKET_OPEN}[{c.RESET}", msg)
        msg = re.sub(r'\](?=\n)', lambda m: f"{c.COLOR_BRACKET_CLOSE}]{c.RESET}", msg)
        return msg

    def __get_env_prefix(self, dimmed_color, dimmed_style, color, style) -> str:
        """Generate environment prefix for log messages."""
        meta = self.__env_metadata
        if not self.__config['color_enabled'] or self.__config['deployed'] or self.__config['mode'] == 'json':
            dimmed_color = ''
            dimmed_style = ''
            color = ''
            style = ''

        prefix = []
        verbose = self.__config['verbose']
        first_color_flag = False
        if meta.get('project', None) is not None and (self.__config['deployed'] or verbose):
            prefix.append(f"{color}{style}{meta['project'].upper()}{self.presets.RESET}")
            first_color_flag = True
        if meta.get('env', None) is not None and (self.__config['deployed'] or verbose):
            if first_color_flag:
                prefix.append(f"{dimmed_color}{dimmed_style}{meta['env'].upper()}{self.presets.RESET}")
            else:
                prefix.append(f"{color}{style}{meta['env'].upper()}{self.presets.RESET}")
        if meta.get('project_version', None) is not None and (self.__config['deployed'] or verbose):
            if first_color_flag:
                prefix.append(f"{dimmed_color}{dimmed_style}{meta['project_version']}{self.presets.RESET}")
            else:
                prefix.append(f"{color}{style}{meta['project_version']}{self.presets.RESET}")
        if meta.get('run_id', None) is not None and (self.__config['deployed'] or verbose):
            if first_color_flag:
                prefix.append(f"{dimmed_color}{dimmed_style}{meta['run_id'].upper()}{self.presets.RESET}")
            else:
                prefix.append(f"{color}{style}{meta['run_id'].upper()}{self.presets.RESET}")

        if len(prefix) > 0:
            return f' {color}{style}:{self.presets.RESET} '.join(prefix) + f" {color}{style}|{self.presets.RESET} "
        else:
            return ''

    def __get_depth(self, internal = False) -> int:
        """Get stack depth to determine log source."""
        for i, frame in enumerate(inspect.stack()):
            if frame.filename.endswith("WrenchLogger.py") or 'WrenchCL' in frame.filename or frame.filename == '<string>':
                if internal:
                    return i + 2
                else:
                    continue
            return i

    def __suggest_exception(self, args) -> Optional[str]:
        """Generate improvement suggestions for certain exceptions."""
        suggestion = None
        if not hasattr(args, '__iter__') and args is not None:
            args = [args]
        else:
            return suggestion

        for a in args:
            if isinstance(a, Exception) or isinstance(a, BaseException):
                ex = a
                if hasattr(ex, 'args') and ex.args and isinstance(ex.args[0], str):
                    suggestion = _ExceptionSuggestor.suggest_similar(ex)
                break
        return suggestion

    def __apply_color(self, text: str, color: Optional[str]) -> str:
        """Apply ANSI colors to text if color mode is enabled."""
        return f"{color}{self.presets.BRIGHT}{text}{self.presets.RESET}" if color else text

    def __check_deployment(self, log = True):
        """Detect deployment environment and adjust settings accordingly."""
        if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None:
            self.__config['color_enabled'] = False
            self.__config['deployed'] = True
            self.disable_color()
            if log:
                self._internal_log("Detected Lambda deployment. Set color mode to False.")
            self.__config['mode'] = 'json'

        if os.environ.get("AWS_EXECUTION_ENV") is not None:
            self.__config['color_enabled'] = False
            self.__config['deployed'] = True
            self.disable_color()
            if log:
                self._internal_log("Detected AWS deployment. Set color mode to False.")
            self.__config['mode'] = 'json'

        if os.environ.get("COLOR_MODE") is not None:
            if os.environ.get("COLOR_MODE").lower() == "false":
                self.__config['color_enabled'] = False
            else:
                self.__config['color_enabled'] = True

        if os.environ.get("LOG_DD_TRACE") is not None:
            val = os.environ.get("LOG_DD_TRACE", "false").lower()
            self.__config['dd_trace_enabled'] = val == "true"
            state = "enabled" if self.__config['dd_trace_enabled'] else "disabled"
            if log:
                self._internal_log(f"LOG_DD_TRACE detected — Datadog tracing {state}. | Mode Json")
            if self.__config['dd_trace_enabled']:
                self.__config['mode'] = 'json'

    def __fetch_env_metadata(self) -> dict:
        """
        Extract environment metadata from system environment variables.
        """
        env_vars = {
            "env": os.getenv("ENV") or os.getenv('DD_ENV') or os.getenv("AWS_EXECUTION_ENV") or None,
            "project": os.getenv("PROJECT_NAME") or os.getenv('COMPOSE_PROJECT_NAME') or os.getenv("AWS_LAMBDA_FUNCTION_NAME") or None,
            "project_version": os.getenv("PROJECT_VERSION") or os.getenv("LAMBDA_TASK_ROOT") or os.getenv('REPO_VERSION') or None,
            "run_id": self.run_id
        }
        return env_vars

    def __setup(self) -> None:
        """Initialize the logger with basic configuration."""
        with self.__lock:
            if self.__initialized:
                self._internal_log("Logger already initialized. Skipping setup.")
                return

            self.flush_handlers()
            self.__logger_instance.setLevel(self.__base_level)
            self.add_new_handler(logging.StreamHandler, stream=sys.stdout, force_replace=True)
            self.__logger_instance.propagate = False
            self.__initialized = True

    def __check_color(self) -> None:
        """
        Check if color output is available and configure accordingly.
        """
        if self.__config['color_enabled']:
            try:
                self.enable_color()
                return
            except ImportError:
                self._internal_log("Color mode not available. Disabling.")
                pass
        self.disable_color()

    def __use_json_logging(self):
        """
        Configure the logger for JSON-structured output.
        """
        formatter = _JSONLogFormatter(self.__env_metadata, self.__force_markup, self.__highlight_literals)

        if not self.__logger_instance.handlers:
            self.add_new_handler(logging.StreamHandler, stream=sys.stdout, formatter=formatter, force_replace=True)
        else:
            self.flush_handlers()
            for i, handler in enumerate(self.__logger_instance.handlers):
                if not hasattr(getattr(handler, "stream", None), "write"):
                    self.__logger_instance.handlers[i] = self.add_new_handler(
                        logging.StreamHandler,
                        stream=sys.stdout,
                        formatter=formatter,
                        force_replace=False,
                    )
                else:
                    handler.setFormatter(formatter)

    def __log_setup_summary(self) -> None:
        """Log a summary of the current logger configuration."""
        if self.__config["mode"] == "json":
            self._internal_log(json.dumps(self.__config, indent=2, default=str))
            return

        settings = self.logger_state
        msg = '⚙️  Logger Configuration:\n'

        msg += f"  • Logging Level: {self.__apply_color(settings['Logging Level'], self.presets.get_color_by_level(settings['Logging Level']))}\n"
        msg += f"  • Mode: {settings['Mode']}\n"
        msg += f"  • Run ID: {settings['Run Id']}\n"

        msg += "  • Configuration:\n"
        for mode, enabled in settings["Configuration"].items():
            state = "✓ Enabled" if enabled else "✗ Disabled"
            color = self.presets.INFO if enabled else self.presets.ERROR
            msg += f"      - {mode:20s}: {self.__apply_color(state, color)}\n"

        if self.__config['color_enabled']:
            msg += self.presets.get_demo_string()

        self._internal_log(msg)


    @staticmethod
    def __generate_run_id() -> str:
        """Generate a unique run ID for this logger instance."""
        now = datetime.now()
        return f"R-{os.urandom(1).hex().upper()}{now.strftime('%m%d')}{os.urandom(1).hex().upper()}"

    def __get_level(self, level: Union[str, int]) -> int:
        """Convert a level name to its numeric value."""
        if isinstance(level, str) and hasattr(logging, level.upper()):
            return getattr(logging, level.upper())
        elif isinstance(level, int):
            return level
        elif level == 'INTERNAL':
            return logging.DEBUG
        return logging.INFO

    def __get_formatter(self, level: Union[str, int], no_format=False) -> logging.Formatter:
        """Get the appropriate formatter based on log level and mode."""

        if self.__config['mode'] == 'json' and level != 'INTERNAL':
            return _JSONLogFormatter(self.__env_metadata, self.__force_markup, self.__highlight_literals)

        color = self.presets.get_color_by_level(level)
        style = self.presets.get_level_style(level)
        message_color = self.presets.get_message_color(level)

        if isinstance(level, int):
            str_name = logging.getLevelName(level)
        else:
            str_name = level.upper()

        if str_name in ['ERROR', 'CRITICAL', 'WARNING']:
            dimmed_color = self.presets.get_color_by_level(level)
        else:
            dimmed_color = self.presets.get_color_by_level('INTERNAL')

        dimmed_style = self.presets.get_level_style('INTERNAL')

        if level == 'INTERNAL':
            color = self.presets.CRITICAL
            style = self.presets.get_level_style('INTERNAL')


        file_section = f"{dimmed_color}{dimmed_style}%(filename)s:%(funcName)s:%(lineno)d]{self.presets.RESET}"
        verbose_section = f"{dimmed_color}{dimmed_style}[%(asctime)s|{file_section}{self.presets.RESET}"
        app_env_section = self.__get_env_prefix(dimmed_color, dimmed_style, color, style)
        level_name_section = f"{color}{style}%(levelname)-8s{self.presets.RESET}"
        colored_arrow_section = f"{color}{style} -> {self.presets.RESET}"
        message_section = f"{style}{message_color}%(message)s{self.presets.RESET}"

        if level == "INTERNAL":
            level_name_section = f"{color}{style}  WrenchCLInternal{self.presets.RESET}"
        elif level == "DATA":
            level_name_section = f"{color}{style}DATA    {self.presets.RESET}"

        if self.__config['mode'] == 'compact':
            fmt = f"{level_name_section}{file_section}{colored_arrow_section}{message_section}"
        elif no_format:
            fmt = "%(message)s"
        if level == 'INTERNAL':
            fmt = f"{level_name_section}{colored_arrow_section}{message_section}"
        else:
            fmt = f"{app_env_section}{level_name_section}{verbose_section}{colored_arrow_section}{message_section}"

        fmt = f"{self.presets.RESET}{fmt}{self.presets.RESET}"

        return _CustomFormatter(fmt, datefmt='%H:%M:%S', presets=self.presets)

    # ---------------- Aliases/Shortcuts ----------------

    def data(self, data, **kwargs):
        """
        Alias for `pretty_log()` for structured or semantic logging.

        :param data: JSON-serializable object or printable value
        :param kwargs: Optional formatting or indentation parameters
        """
        return self.pretty_log(data, **kwargs)


@SingletonClass
class _logger_(_BaseLogger):
    __doc__ = """Singleton thread-safe instance of BaseLogger.""" + _BaseLogger.__doc__

    def __init__(self):
        super().__init__()

    @property
    def baseClass(self) -> Type[_BaseLogger]:
        "Returns the base class of this instance."
        return _BaseLogger
