#!/usr/bin/env python3
"""
HWP HTML Extractor

Extracts text content from HWP-converted HTML files with table-aware parsing.
Handles tables by preserving row structure with pipe-separated columns.

Usage:
    from html_extractor import HwpHtmlExtractor

    parser = HwpHtmlExtractor()
    parser.feed(html_content)
    for line in parser.output:
        print(line)
"""

from html.parser import HTMLParser
from typing import List


class HwpHtmlExtractor(HTMLParser):
    """
    HTML parser that extracts text from HWP-converted HTML.

    Features:
    - Ignores style tags and CSS content
    - Preserves table structure with pipe-separated columns
    - Filters out noise characters like standalone punctuation
    """

    def __init__(self):
        super().__init__()
        self.in_style: bool = False
        self.in_table: bool = False
        self.in_tr: bool = False
        self.in_td: bool = False
        self.current_cell: List[str] = []
        self.current_row: List[str] = []
        self.current_table: List[List[str]] = []
        self.output: List[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        """Handle opening HTML tags."""
        if tag == 'style':
            self.in_style = True
        elif tag == 'table':
            self.in_table = True
            self.current_table = []
        elif tag == 'tr' and self.in_table:
            self.in_tr = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_table:
            self.in_td = True
            self.current_cell = []

    def handle_endtag(self, tag: str) -> None:
        """Handle closing HTML tags."""
        if tag == 'style':
            self.in_style = False
        elif tag in ('td', 'th') and self.in_table and self.in_td:
            cell = ''.join(self.current_cell).strip()
            self.current_row.append(cell)
            self.current_cell = []
            self.in_td = False
        elif tag == 'tr' and self.in_table and self.in_tr:
            if self.current_row:
                self.current_table.append(self.current_row)
            self.current_row = []
            self.in_tr = False
        elif tag == 'table' and self.in_table:
            if self.current_table:
                self.output.append("TABLE:")
                for row in self.current_table:
                    self.output.append(" | ".join(row))
            self.current_table = []
            self.in_table = False

    def handle_data(self, data: str) -> None:
        """Handle text content."""
        if self.in_style:
            return

        text = data.strip().replace('&#13;', '')
        if not text:
            return

        if self.in_table:
            if self.in_td:
                self.current_cell.append(text)
        else:
            self.output.append(text)

    def get_text(self) -> str:
        """Return all extracted text as a single string."""
        return '\n'.join(
            line for line in self.output
            if line and line not in ['.', '{', '}', ';']
        )


def extract_text_from_html(html_content: str) -> str:
    """
    Extract text from HWP-converted HTML content.

    Args:
        html_content: HTML string from hwp5html conversion

    Returns:
        Extracted text with preserved table structure
    """
    parser = HwpHtmlExtractor()
    parser.feed(html_content)
    return parser.get_text()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python html_extractor.py <html_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        html_content = f.read()

    print(extract_text_from_html(html_content))
