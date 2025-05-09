# corelab-blockkit

A library for building and managing content blocks.

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/corelab-blockkit.svg)](https://pypi.org/project/corelab-blockkit/)

## Overview

`corelab-blockkit` is a CoreLab project that provides a standardized representation of course content as discrete "blocks" that can be serialized, rendered, and extended. It's designed to be lightweight, type-safe, and easily extensible.

## Features

- **Core Block Types**: TextBlock, ImageBlock, VideoBlock, AudioBlock, DownloadBlock, GlossaryBlock, QuoteBlock, SupplementBlock
- **Serialization**: JSON and YAML support
- **Type Registry**: Extensible registry for block types
- **Block Operations**: Add, remove, move, and find blocks
- **Metadata**: Track creation/update times, favorites, tags, and custom metadata
- **Extensibility**: Add custom block types without modifying the core library

## Installation

```bash
pip install corelab-blockkit
```

## Quick Start

```python
from corelab_blockkit import BlockList, TextBlock, ImageBlock

# Create a block list
blocks = BlockList()

# Add a text block
text_block = TextBlock(
    text="Hello **world**! This is a *markdown* formatted text block.",
    format="markdown",
)
blocks = blocks.add(text_block)

# Add an image block
image_block = ImageBlock(
    url="https://example.com/image.jpg",
    alt_text="An example image",
    caption="Figure 1: Example image",
)
blocks = blocks.add(image_block)

# Serialize to JSON
json_str = blocks.to_json(indent=2)
print(json_str)

# Serialize to YAML
yaml_str = blocks.to_yaml()
print(yaml_str)

# Deserialize from JSON
deserialized = BlockList.from_json(json_str)
```

## Plugin Guide

You can extend `blockkit` with custom block types by creating a plugin. Here's how:

1. Create a new package with a class that inherits from `BaseBlock`
2. Define an entry point in your `pyproject.toml`:

```toml
[project.entry-points."blockkit.blocks"]
my_block = "my_package:MyBlock"
```

3. Install your package, and `blockkit` will automatically discover and register your block type

See the [examples/plugin_example](examples/plugin_example) directory for a complete example.

## JSON Specification

Each block is serialized to JSON with the following structure:

```json
{
  "id": "uuid-string",
  "kind": "block-type",
  "meta": {
    "created_at": "iso-datetime",
    "updated_at": "iso-datetime",
    "is_favorite": false,
    "tags": [],
    "extra": {}
  },
  "payload": {
    // Block-specific content
  }
}
```

A block list is serialized as:

```json
{
  "blocks": [
    // Array of block objects
  ]
}
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
