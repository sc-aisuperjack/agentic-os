import os
import sys
import structlog
from typing import Any

def setup_logger(service_name: str):
    """
    CEO-Grade Structured Logging.
    JSON in Production (Render), Colorful in Local.
    """
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    # If on Render, use JSON for better log aggregation
    if os.getenv("RENDER", "false").lower() == "true":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(20), # INFO level
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger(service_name=service_name)

# Global usage: logger = setup_logger("orchestrator")