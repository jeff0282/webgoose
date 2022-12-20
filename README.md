# Webgoose - Web 1.0 Style Static Page Generator

**(IN DEVELOPMENT)** 

![Version Badge](https://raster.shields.io/badge/Version-0.3.4-green)

Webgoose is a Static Page Generator written in Python, using the Jinja2 Templating Engine and CMARK-GFM for Markdown Conversion.

More Information will be Added to this README as Development Progresses.

---

# Basic Information

### Installation:

Webgoose can be installed simply by running the following commands:
```
git clone https://github.com/jeff0282/webgoose
cd webgoose
pip3 install .
```

### Usage:

(webgoose does NOT yet spit out HTML files, please await the release of 1.0.0)

Webgoose only supports a single command ``webgoose``; no arguments are currently supported.

This command looks for a config file, located at the relative path ``./config/config.yaml``, an example file is shown below:

```
# Webgoose Standard Config

# Buid Options:
source_dir: ".source"
build_dir: "."
template_dir: ".template"
default_template: "default.j2"
```

Using the config, webgoose loads in all the information about the site, builds the pages in the source-dir specified in the config file, and outputs the resulting string to STDOUT. 



# Todo:

A hell of a lot!!

- Output resulting html files to their corresponding build file
- Move static files to build location
- Restructure SiteQuerier To Load In Info About All Pages To Allow For Smart Things (e.g. scanning all page's metadata for certain attributes) !!!
- Allow for reading of Data Files and allow access in template and source files
- Allow for page tags
- Add support for special filenames that expand to multiple pages (e.g. {tag}.md should make a page for every tag)
