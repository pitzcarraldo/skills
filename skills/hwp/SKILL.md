---
name: hwp
description: This skill should be used when the user wants to view contents of HWP/HWPX files (한글 문서), mentions ".hwp" or ".hwpx" file paths, asks to "read hwp", "read hwpx", "open hwp", "open hwpx", "hwp 파일 열기", "hwpx 파일 열기", "한글 문서 읽기", or needs to extract text from Korean word processor documents.
argument-hint: [file-path]
metadata:
    short-description: Extract and display HWP/HWPX document contents
user-invocable: true
---

# HWP/HWPX Skill

## Overview

This skill enables Claude to read and extract text content from Korean Hangul Word Processor (HWP/HWPX) files. It automatically detects file formats and uses the appropriate library for extraction.

## Supported Formats

- **HWPX** (Hangul 2014+): XML-based format, ZIP container
- **HWP** (Hangul 5.x): Legacy binary format, OLE2 container

## Tool Selection Guide

Choose the appropriate tool based on file extension:

| File Type | Extension | Library | Use Case |
|-----------|-----------|---------|----------|
| Modern Hangul | `.hwpx` | python-hwpx | Documents from Hangul 2014+ |
| Legacy Hangul | `.hwp` | pyhwp | Documents from Hangul 5.x and earlier |

## Workflow

### 1. File Detection and Validation

**Check file existence and extension:**

```bash
ls -la "[file-path]"
```

**Expected output:**
- File exists: Proceed to step 2
- File not found: Display error message

**Error message format:**
```
Error: File not found - [file-path]
Please verify the file path and try again.
```

### 2. Process HWPX Files (Modern Format)

**2.1 Check Installation**

```bash
python3 -c "import hwpx; print('OK')" 2>&1
```

**If not installed:**

```
python-hwpx library is not installed.
Installing now...
```

**Install command:**
```bash
pip install python-hwpx || pip install --break-system-packages python-hwpx
```

**On success:**
```
python-hwpx installation complete. Processing HWPX file...
```

**2.2 Extract Text Content**

```bash
python3 << 'PYTHON_SCRIPT'
import sys
from hwpx.document import HwpxDocument

try:
    file_path = "[file-path]"
    document = HwpxDocument.open(file_path)

    print("=" * 60)
    print(f"File: {file_path}")
    print("=" * 60)
    print()

    paragraph_count = 0
    for paragraph in document.paragraphs:
        text = paragraph.text.strip() if hasattr(paragraph, 'text') else str(paragraph).strip()
        if text:
            print(text)
            print()
            paragraph_count += 1

    print("=" * 60)
    print(f"Total {paragraph_count} paragraphs")
    print("=" * 60)

except FileNotFoundError:
    print(f"Error: File not found - {file_path}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
```

### 3. Process HWP Files (Legacy Format)

**3.1 Check Installation**

```bash
python3 -c "import hwp5; print('OK')" 2>&1
```

**If not installed:**

```
pyhwp library is not installed.
Installing now...
```

**Install commands:**
```bash
pip install --break-system-packages six pyhwp || pip install six pyhwp
```

**On success:**
```
pyhwp installation complete. Processing HWP file...
```

**3.2 Extract Text Content (Single-pass with fallback)**

Use `hwp5txt` first, then automatically fall back to table-aware HTML extraction if the output is too small or table-only (e.g., just `<표>`). This makes it possible to see content in one run while preserving table rows.

```bash
python3 << 'PYTHON_SCRIPT'
import subprocess
import sys
import re

file_path = "[file-path]"

def run_hwp5txt(path: str) -> str:
    proc = subprocess.run(["hwp5txt", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.stdout

def should_fallback(text: str) -> bool:
    # If only table markers or too little text, HTML extraction is more reliable.
    normalized = re.sub(r"\s+", "", text)
    if not normalized:
        return True
    if normalized in {"<표>", "<표></표>"}:
        return True
    if len(normalized) < 40:
        return True
    return False

print("=" * 60)
print(f"File: {file_path}")
print("=" * 60)
print()

txt_output = run_hwp5txt(file_path)
if not should_fallback(txt_output):
    print(txt_output.rstrip())
    print()
    print("=" * 60)
    print("HWP file processing complete")
    print("=" * 60)
    sys.exit(0)

# Fallback: convert to HTML and extract text
subprocess.run(["hwp5html", file_path, "--output", "/tmp/hwp_output"], check=False)

from html.parser import HTMLParser

class HwpHtmlExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_style = False
        self.in_table = False
        self.in_tr = False
        self.in_td = False
        self.current_cell = []
        self.current_row = []
        self.current_table = []
        self.output = []

    def handle_starttag(self, tag, attrs):
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

    def handle_endtag(self, tag):
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

    def handle_data(self, data):
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

with open('/tmp/hwp_output/index.xhtml', 'r', encoding='utf-8') as f:
    html_content = f.read()

parser = HwpHtmlExtractor()
parser.feed(html_content)

for line in parser.output:
    if line and line not in ['.', '{', '}', ';']:
        print(line)

print()
print("=" * 60)
print("HWP file processing complete")
print("=" * 60)
PYTHON_SCRIPT
```

**Alternative method (Manual HTML extraction):**

If you want to skip the fallback check and always extract from HTML with table-aware output:

```bash
# Convert to HTML
hwp5html "[file-path]" --output /tmp/hwp_output 2>&1

# Extract text from HTML
python3 << 'PYTHON_SCRIPT'
from html.parser import HTMLParser

class HwpHtmlExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_style = False
        self.in_table = False
        self.in_tr = False
        self.in_td = False
        self.current_cell = []
        self.current_row = []
        self.current_table = []
        self.output = []

    def handle_starttag(self, tag, attrs):
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

    def handle_endtag(self, tag):
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

    def handle_data(self, data):
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

with open('/tmp/hwp_output/index.xhtml', 'r', encoding='utf-8') as f:
    html_content = f.read()

parser = HwpHtmlExtractor()
parser.feed(html_content)

print("=" * 60)
print("File: [file-path]")
print("=" * 60)
print()

for line in parser.output:
    if line and line not in ['.', '{', '}', ';']:
        print(line)

print()
print("=" * 60)
print("HWP file processing complete")
print("=" * 60)
PYTHON_SCRIPT
```

## Output Format

All text extraction follows this consistent format:

```
============================================================
File: /path/to/document.hwp
============================================================

[Extracted text content organized by paragraphs]

============================================================
Total N paragraphs / Processing complete
============================================================
```

## Examples

### Example 1: HWPX File Extraction

```bash
User: /hwp ~/Documents/report.hwpx
```

**Claude's action:**
1. Checks file exists
2. Detects `.hwpx` extension
3. Verifies python-hwpx is installed
4. Extracts text using HwpxDocument
5. Displays formatted output

### Example 2: HWP File Extraction

```bash
User: /hwp ~/Documents/minutes.hwp
```

**Claude's action:**
1. Checks file exists
2. Detects `.hwp` extension
3. Verifies pyhwp is installed
4. Extracts text using hwp5txt
5. Displays formatted output

### Example 3: Auto-Trigger

```bash
User: Show me the contents of contract.hwp
```

**Claude automatically:**
1. Detects HWP file mention
2. Locates file in current directory
3. Applies appropriate extraction method
4. Displays results

## Technical Requirements

### Required Libraries

| Library | Purpose | Installation |
|---------|---------|--------------|
| python-hwpx | HWPX file parsing | `pip install python-hwpx` |
| pyhwp | HWP file parsing | `pip install pyhwp` |
| six | pyhwp dependency | `pip install six` |

### Command-Line Tools

| Tool | Purpose | Availability |
|------|---------|--------------|
| hwp5txt | Text extraction from HWP | Installed with pyhwp |
| hwp5html | HTML conversion from HWP | Installed with pyhwp |

### System Requirements

- **Python**: 3.7 or higher
- **pip**: Package installer for Python
- **System permissions**: May require `--break-system-packages` flag on managed environments

## Limitations

1. **Text-only extraction**: Images, shapes, and embedded objects are not extracted
2. **Formatting loss**: Complex formatting, colors, and styles are simplified
3. **Table rendering**: Tables are converted to plain text or HTML structure
4. **Font information**: Font details and sizes are not preserved
5. **Comments and tracked changes**: May not be fully extracted depending on method

## Error Handling

### Common Errors and Solutions

**Error: File is not a zip file**
- **Cause**: Trying to open HWP 5.x file with python-hwpx
- **Solution**: File is legacy format, use pyhwp instead

**Error: No module named 'hwp5'**
- **Cause**: pyhwp not installed
- **Solution**: Install pyhwp and six dependencies

**Error: No module named 'six'**
- **Cause**: Missing pyhwp dependency
- **Solution**: Install six before pyhwp

**Error: externally-managed-environment**
- **Cause**: System-managed Python environment
- **Solution**: Use `--break-system-packages` flag

## Best Practices

1. **Always verify file path** before attempting extraction
2. **Check file extension** to determine correct tool
3. **Handle installation errors gracefully** with clear user messages
4. **Use HTML conversion** for documents with complex tables
5. **Preserve document structure** in output formatting
6. **Clean up temporary files** after HTML conversion

## References

- **pyhwp GitHub**: https://github.com/mete0r/pyhwp
- **python-hwpx PyPI**: https://pypi.org/project/python-hwpx/
- **HWP Format Specification**: Korean standard word processor format

## Notes

- HWP/HWPX files are primarily used in South Korea for government and business documents
- The skill prioritizes text extraction over formatting preservation
- For editing capabilities, consider using the Hangul Word Processor application directly
- Both libraries are community-maintained projects
