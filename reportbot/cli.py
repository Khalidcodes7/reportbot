"""Command line interface: `reportbot run config.yaml`."""
from __future__ import annotations

import argparse
import logging
import sys
import time

from .pipeline import ReportConfig, run_pipeline

logger = logging.getLogger("reportbot")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reportbot",
        description="Scrape data, build an Excel report, and email it — automatically.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="run a full report job from a YAML/JSON config")
    run.add_argument("config", help="path to config file")
    run.add_argument("--email-to", help="override the recipient email")
    run.add_argument("--no-email", action="store_true", help="skip sending the email")
    run.add_argument("--output", help="override the report output path")
    run.add_argument("--max-pages", type=int, help="override max_pages")

    return parser


def cmd_run(args) -> int:
    config = ReportConfig.from_file(args.config)

    if args.email_to is not None:
        config.email_to = args.email_to
    if args.no_email:
        config.email_to = ""
    if args.output:
        config.output_path = args.output
    if args.max_pages is not None:
        config.max_pages = args.max_pages

    started = time.time()
    result = run_pipeline(config)
    elapsed = time.time() - started

    logger.info(
        "Done: %d rows -> %s (%.1fs)",
        result["rows"],
        result["report"],
        elapsed,
    )
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )
    try:
        return cmd_run(args)
    except KeyboardInterrupt:
        logger.warning("Interrupted")
        return 130
    except Exception as exc:  # noqa: BLE001 - top-level CLI handler
        logger.error("%s: %s", type(exc).__name__, exc)
        if args.verbose:
            raise
        return 1


if __name__ == "__main__":
    sys.exit(main())