"""ReportBot - scrape data, build Excel reports, and email them automatically."""

from .cli import main
from .mailer import send_report
from .pipeline import ReportConfig, run_pipeline
from .report import build_report

__version__ = "0.1.0"
__all__ = [
    "ReportConfig",
    "build_report",
    "main",
    "run_pipeline",
    "send_report",
    "__version__",
]