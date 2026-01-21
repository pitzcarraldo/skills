---
name: hwp
description: This skill should be used when the user wants to view contents of HWP/HWPX files (Korean word processor documents), mentions ".hwp" or ".hwpx" file paths, asks to "read hwp", "read hwpx", "open hwp", "open hwpx", or needs to extract text from Korean word processor documents.
argument-hint: [file-path]
metadata:
    short-description: Extract and display HWP/HWPX document contents
user-invocable: true
---

# HWP/HWPX Document Reader

This skill extracts text content from Korean Hangul Word Processor files (.hwp, .hwpx).

## Supported Formats

| Format | Extension | Library | Description |
|--------|-----------|---------|-------------|
| Modern | `.hwpx` | python-hwpx | XML-based format (Hangul 2014+) |
| Legacy | `.hwp` | pyhwp | Binary OLE2 format (Hangul 5.x) |

## Quick Start

To read an HWP/HWPX file, run the reader script:

```bash
python3 scripts/hwp_reader.py "[file-path]"
```

The script automatically:
1. Detects file format by extension
2. Installs required libraries if missing
3. Extracts text with table-aware formatting
4. Falls back to HTML extraction for complex documents

## Scripts

### hwp_reader.py

Main entry point for reading HWP/HWPX files. Read the complete script before using:

```bash
cat scripts/hwp_reader.py
```

**Key functions:**
- `read_hwpx()`: Extract text from modern HWPX files
- `read_hwp()`: Extract text from legacy HWP files with automatic fallback
- `install_package()`: Auto-install missing dependencies

### html_extractor.py

Utility for extracting text from HWP-converted HTML. Provides table-aware parsing:

```bash
cat scripts/html_extractor.py
```

**Key class:**
- `HwpHtmlExtractor`: HTMLParser subclass that preserves table structure

## Workflow

### 1. Verify File Exists

```bash
ls -la "[file-path]"
```

### 2. Run Reader Script

```bash
cd [skill-directory]
python3 scripts/hwp_reader.py "[file-path]"
```

### 3. Handle Missing Dependencies

If libraries are not installed, the script will attempt automatic installation:

```bash
# For HWPX files
pip install python-hwpx

# For HWP files
pip install six pyhwp
```

On managed environments, use:
```bash
pip install --break-system-packages [package]
```

## Output Format

```
============================================================
File: /path/to/document.hwp
============================================================

[Extracted text content]

TABLE:
Column 1 | Column 2 | Column 3
Value 1 | Value 2 | Value 3

[More text...]

============================================================
HWP file processing complete
============================================================
```

## Technical Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.7+ |
| python-hwpx | Latest (for .hwpx) |
| pyhwp | Latest (for .hwp) |

## Limitations

- **Text-only**: Images and embedded objects are not extracted
- **Formatting loss**: Styles, colors, and fonts are not preserved
- **Tables**: Converted to pipe-separated text format
- **Comments**: May not be fully extracted

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| File not found | Invalid path | Verify file path |
| Not a zip file | Using python-hwpx on .hwp | Script auto-detects format |
| No module named 'hwp5' | pyhwp not installed | Script auto-installs |
| externally-managed-environment | System Python | Use --break-system-packages |

## References

- [pyhwp GitHub](https://github.com/mete0r/pyhwp)
- [python-hwpx PyPI](https://pypi.org/project/python-hwpx/)
