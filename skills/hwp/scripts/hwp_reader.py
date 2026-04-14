#!/usr/bin/env python3
"""
HWP/HWPX Document Reader

Extracts text content from Korean Hangul Word Processor files.
Supports both legacy HWP (5.x) and modern HWPX (2014+) formats.

Usage:
    python hwp_reader.py <file_path>

Requirements:
    - python-hwpx: For HWPX files (pip install python-hwpx)
    - pyhwp: For HWP files (pip install pyhwp)
"""

import sys
import os
import subprocess
import re
from pathlib import Path

# Import HTML extractor for fallback processing
from html_extractor import HwpHtmlExtractor


def print_header(file_path: str) -> None:
    """Print formatted header."""
    print("=" * 60)
    print(f"File: {file_path}")
    print("=" * 60)
    print()


def print_footer(message: str = "Processing complete") -> None:
    """Print formatted footer."""
    print()
    print("=" * 60)
    print(message)
    print("=" * 60)


def check_hwpx_installation() -> bool:
    """Check if python-hwpx is installed."""
    try:
        import hwpx
        return True
    except ImportError:
        return False


def check_pyhwp_installation() -> bool:
    """Check if pyhwp is installed."""
    try:
        import hwp5
        return True
    except ImportError:
        return False


def install_package(package: str) -> bool:
    """Attempt to install a Python package."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--break-system-packages", package],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False


def read_hwpx(file_path: str) -> None:
    """Read and extract text from HWPX file."""
    if not check_hwpx_installation():
        print("python-hwpx library is not installed. Installing now...", file=sys.stderr)
        if not install_package("python-hwpx"):
            print("Error: Failed to install python-hwpx", file=sys.stderr)
            sys.exit(1)
        print("python-hwpx installation complete.", file=sys.stderr)

    from hwpx.document import HwpxDocument

    try:
        document = HwpxDocument.open(file_path)
        print_header(file_path)

        paragraph_count = 0
        for paragraph in document.paragraphs:
            text = paragraph.text.strip() if hasattr(paragraph, 'text') else str(paragraph).strip()
            if text:
                print(text)
                print()
                paragraph_count += 1

        print_footer(f"Total {paragraph_count} paragraphs")

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def run_hwp5txt(file_path: str) -> str:
    """Run hwp5txt command and return output."""
    proc = subprocess.run(
        ["hwp5txt", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return proc.stdout


def should_fallback_to_html(text: str) -> bool:
    """Determine if HTML extraction is needed based on hwp5txt output."""
    normalized = re.sub(r"\s+", "", text)
    if not normalized:
        return True
    if normalized in {"<표>", "<표></표>"}:
        return True
    if len(normalized) < 40:
        return True
    return False


def extract_from_html(file_path: str) -> None:
    """Extract text using HTML conversion fallback."""
    output_dir = "/tmp/hwp_output"
    subprocess.run(
        ["hwp5html", file_path, "--output", output_dir],
        check=False,
        capture_output=True
    )

    html_file = os.path.join(output_dir, "index.xhtml")
    if not os.path.exists(html_file):
        print("Error: HTML conversion failed", file=sys.stderr)
        sys.exit(1)

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    parser = HwpHtmlExtractor()
    parser.feed(html_content)

    for line in parser.output:
        if line and line not in ['.', '{', '}', ';']:
            print(line)


def read_hwp(file_path: str) -> None:
    """Read and extract text from HWP file."""
    if not check_pyhwp_installation():
        print("pyhwp library is not installed. Installing now...", file=sys.stderr)
        if not install_package("six"):
            print("Error: Failed to install six dependency", file=sys.stderr)
            sys.exit(1)
        if not install_package("pyhwp"):
            print("Error: Failed to install pyhwp", file=sys.stderr)
            sys.exit(1)
        print("pyhwp installation complete.", file=sys.stderr)

    print_header(file_path)

    # Try hwp5txt first
    txt_output = run_hwp5txt(file_path)

    if not should_fallback_to_html(txt_output):
        print(txt_output.rstrip())
        print_footer("HWP file processing complete")
        return

    # Fallback to HTML extraction for table-heavy documents
    extract_from_html(file_path)
    print_footer("HWP file processing complete")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python hwp_reader.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}", file=sys.stderr)
        sys.exit(1)

    ext = Path(file_path).suffix.lower()

    if ext == ".hwpx":
        read_hwpx(file_path)
    elif ext == ".hwp":
        read_hwp(file_path)
    else:
        print(f"Error: Unsupported file extension '{ext}'. Use .hwp or .hwpx", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
