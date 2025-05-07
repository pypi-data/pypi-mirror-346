"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

"""
"""
Command-line interface for VAssureAI framework.

Provides command-line tools for running tests, managing PDFs,
and interacting with the framework.
"""

import os
import sys
import asyncio
import argparse
import subprocess
from typing import List, Optional

from ..core.base.config import BaseConfig
from ..core.base.llm import BaseLLMFactory
from ..core.base.runner import BaseTestRunner
from ..core.base.plugin import BasePluginManager


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="VAssureAI Test Automation Framework"
    )
    
    # Main command groups
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run tests")
    run_parser.add_argument(
        "test_path",
        nargs="?",
        default="tests",
        help="Path to test file or directory"
    )
    run_parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    run_parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers"
    )
    
    # Watch command
    watch_parser = subparsers.add_parser(
        "watch",
        help="Watch PDF directory for changes"
    )
    watch_parser.add_argument(
        "pdf_path",
        nargs="?",
        default="input_pdfs",
        help="Path to PDF file or directory"
    )
    watch_parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run in daemon mode"
    )
    
    # Init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize framework in current directory"
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Force initialization even if directory is not empty"
    )
    
    return parser.parse_args()


async def run_tests(
    test_path: str,
    parallel: bool = False,
    workers: int = 4
) -> bool:
    """Run tests from specified path using pytest."""
    pytest_args = ["pytest", test_path]
    if parallel:
        pytest_args += ["-n", str(workers)]
    # Run pytest as a subprocess for reliability
    result = subprocess.run(pytest_args)
    return result.returncode == 0


async def watch_pdfs(pdf_path: str, daemon: bool = False) -> None:
    """Watch PDF directory for changes."""
    # TODO: Implement PDF watching functionality
    pass


def init_framework(force: bool = False) -> bool:
    """Initialize framework in current directory."""
    directories = [
        "tests",
        "input_pdfs",
        "reports",
        "logs",
        "metrics",
        "custom"
    ]
    
    try:
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Copy sample PDF and test if not already present
        import shutil
        framework_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sample_pdf_src = os.path.join(framework_dir, 'input_pdfs', 'amazon.pdf')
        sample_pdf_dst = os.path.join('input_pdfs', 'amazon.pdf')
        if os.path.exists(sample_pdf_src) and not os.path.exists(sample_pdf_dst):
            shutil.copy2(sample_pdf_src, sample_pdf_dst)
        
        sample_test_src = os.path.join(framework_dir, 'tests', 'test_amazon.py')
        sample_test_dst = os.path.join('tests', 'test_amazon.py')
        if os.path.exists(sample_test_src) and not os.path.exists(sample_test_dst):
            shutil.copy2(sample_test_src, sample_test_dst)
        
        # Copy README.html (user-facing) into the new project if not already present
        readme_html_src = os.path.join(framework_dir, 'README.html')
        readme_html_dst = os.path.join('README.html')
        if os.path.exists(readme_html_src) and not os.path.exists(readme_html_dst):
            shutil.copy2(readme_html_src, readme_html_dst)
        
        # Create example configuration
        config = BaseConfig()
        config.save(".env.example")
        
        return True
    except Exception as e:
        print(f"Initialization failed: {str(e)}")
        return False


def main() -> int:
    """Main entry point for the CLI."""
    args = parse_args()
    
    if args.command == "run":
        success = asyncio.run(run_tests(
            args.test_path,
            args.parallel,
            args.workers
        ))
        return 0 if success else 1
        
    elif args.command == "watch":
        asyncio.run(watch_pdfs(args.pdf_path, args.daemon))
        return 0
        
    elif args.command == "init":
        success = init_framework(args.force)
        return 0 if success else 1
        
    else:
        print("No command specified. Use --help for usage information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())