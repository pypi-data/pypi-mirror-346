import sys

from bclearer_orchestration_services.log_environment_utility_service import (
    loggers,
)

sys.modules["loggers"] = loggers
