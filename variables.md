# Variables In Webgoose Templating


- Site Info
- Page Info
- Macros
- Content


## Site
- .pages				-> List Of All Pages (with properties)
	+ .path
	+ .name
	+ .base_name
	+ .extension

- .static_files		-> All Static Files Present In Build Directory
	+ (same properties as ``.pages``)

- .url				-> URL of site as declared in .config/config.ini
- .config			-> All Configs Set In .config/config.ini as dict: str
- .version			-> Current Version Num As String 
- .time				-> Current Unix Time When Webgoose Launched


## Page
Provides Access To All Page Information and Metadata

- .meta 				-> Metadata in Frontmatter/Defaults
- .title				-> shortcut to title
- .desc 				-> shortcut to description
- .source_path		-> source markdown file path
- .build_path		-> build path for final HTML page
- .last_source_mod 	-> last mod time for source file
- .last_mod			-> last build time for page
- .raw_content		-> unprocessed content as string
- .raw_template		-> unprocessed template as string
 

## Content
Provides access to Page Content in Various Forms

- .content			-> returns all content as a string (ignores blocks)
- .content_dict		-> returns a dict {block_id:block_content}


## Macro
Provides Access To Helpful Methods N Stuff

- .time(format=<GNU-DATE-FORMAT>)
- .format_time(epoch)
- .toc()