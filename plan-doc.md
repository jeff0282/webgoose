# Planning Document - WebGoose 2
bog je srbin


## Project Structure:

```
webgoose
    - config    -> for config file, env variable stuffs, etc :3
    - pages     -> for site pages stored as partial html/markdown with YAML frontmatter
    - template  -> for storing templates used by WebGoose
    - static    -> for storing static files (images, css, etc, etc, and etc)
    - src       -> source code
```


## Routes: 

- /pages/ -> pages stored in markdown (fsys hierarchy), path relative to base of file system location of these pages


## Page Frontmatter

Stored in YAML at top of page files.
```
---

# Basic Metadata (Mandatory)
title: str -> "What To Show As Tab Title"

# Custom Headers
extra-css: list or str -> path(s) to extra css files to include
custom-template: str -> path to non-standard template to use for this page

# OpenGraph Metadata (Used For Page Embeds)
description: <description of page>
embed-img: <link-to-image>

# Twitter OpenGraph Extra
tw-site: str -> Twitter Handle For Website
tw-creator: str -> Twitter Handle For "Content Creator"

---
```

