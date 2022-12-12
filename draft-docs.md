# Webgoose - Static Site Generator
For Web 1.0 Style Personal Websites/Blogs


## Variables

### Site

The Object Containing All Site-Wide Information

``site.all_files``
- A List Containing WGFile Objects, with .basename, .ext, .path, .last_mod, attributes

``site.pages``
- A Subset of `site.all_files` Containing Only `.md` Files

``site.static_files``
- A Subset of `site.all_files` Containing Everything That Isn't A `.md` File.

``site.timestamp``
- The Time of Site Generation As An Epoch Timestamp

``site.config``
- A Dictionary Containing All Configuration Options Set In Site `config.ini`



### Page

The Object Containing All Information About A Single Page

``page.source_path``
- The Relative Path of the Source Markdown File Used

``page.build_path``
- The Relative Path of the Destination File

``page.template_path``
- The Relative Path of the Template File Used

``page.title``
- A Shortened Version of `page.meta['title']`

``page.description``
- A Shortened Version of `page.meta['description']`

``page.meta``
- A Dictionary Containing All Values Set in the Pages YAML Frontmatter (may include default values)

``page.raw_template``
- The Raw Template as a String Used by the Page

``page.raw_content``
- The Raw, Unprocessed Markdown From the Source File

``page.file``
- The Corresponding WGFile Object From `site.all_files` (and `site.pages` by extension)



### Content

The Object Containing The Page Content and Content_Dict (awaiting GooseDown support)

``content.string`` (also available as str(content))
- The String containing All Page Content, Disregarding Blocks

``content.dict`` (awaiting GooseDown support)
- A Dictionary Containing Block-ID : Block-Content Pairs





 
