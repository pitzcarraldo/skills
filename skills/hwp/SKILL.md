---
name: hwp
description: This skill should be used when the user wants to view contents of HWP/HWPX files (Korean word processor documents), mentions ".hwp" or ".hwpx" file paths, asks to "read hwp", "read hwpx", "open hwp", "open hwpx", or needs to extract text from Korean word processor documents.
argument-hint: [file-path]
metadata:
    short-description: Extract and display HWP/HWPX document contents
user-invocable: true
---

# HWP/HWPX Document Reader

This skill reads Korean Hangul Word Processor files (.hwp, .hwpx) and prepares to respond based on the content using [pyhwp2md](https://github.com/pitzcarraldo/pyhwp2md).

## Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| HWP | `.hwp` | Binary format (HWP 5.0+) |
| HWPX | `.hwpx` | XML-based format (Hangul 2014+) |

## Workflow

### 1. Verify File Exists

```bash
ls -la "[file-path]"
```

### 2. Extract Content

```bash
# Preferred (no installation needed)
uvx pyhwp2md "[file-path]"

# Alternatives if uvx is not available
pipx run pyhwp2md "[file-path]"
pip install pyhwp2md && pyhwp2md "[file-path]"
```

### 3. Handle Output Based on Size

**If content fits in context**: Use the stdout output directly to respond to user queries.

**If content is too large for context**: Save to a temporary file and reference it:

```bash
uvx pyhwp2md "[file-path]" -o /tmp/extracted_content.md
```

Then read the file in chunks as needed to answer user questions.

## Technical Requirements

| Requirement | Version | Note |
|-------------|---------|------|
| Python | 3.10+ | Required |
| uv/pipx/pip | Latest | Any one of these |

## Limitations

- **Images**: Not yet supported
- **Links**: Partial support
- **Formatting**: Styles, colors, and fonts are not preserved

## References

- [pyhwp2md GitHub](https://github.com/pitzcarraldo/pyhwp2md)
- [pyhwp2md PyPI](https://pypi.org/project/pyhwp2md/)
