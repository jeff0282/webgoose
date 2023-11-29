# Webgoose - A Static-Site Generator Framework

**[Roughly Mid-Way In-Development]**

## Le Petit Preface
Over 12 months of development. 12 complete restarts. This project has become something of a Sisyphus of Software, never going anywhere.

Starting life as a imageboard-style personal website engine (which worked scarily well), it went through a minimalism phase, a tree-centric phase, multiple identity crises, and has now developed into a static site generator framework

Who knows, maybe this idea will fall through as well. Though I have hope that this revision will become something!


## Provisional API
This is the proposed API for Webgoose. It's not exactly polished, but it's getting there :)
```python
from    pathlib     import      Path

from    webgoose    import      Component
from    webgoose    import      Page
from    webgoose    import      Site


site = Site()


@site.attach()
def root(component):
    """
    The root of the site 
    """
    component.add("index.html", Page(".src/index.md"))


@root.attach("blog/")
def blog(component):
    """
    Blog section of the site
    """

    tags = component.posts.group("tags", include_missing=True)
    tag_page = Page(template=".template/tags.jinja2", tags=tags)
    
    
@blog.attach("posts/")
def posts(component):
    """
    Posts within the blog section of the site
    """

    for path in Path.glob(".src/posts/*.md")
        component.add(path.stem + ".html", Page(path))


if __file__ == __main__:
    site.render("./build")

```


## Credits & Notes

Webgoose has been heavily inspired by a variety of projects and websites:

- ['Lightweight'](https://github.com/mdrachuk/lightweight) - A Nice & Simple Static-Site Generator Framework; Inspiration for quite a lot of the Webgoose API.
- ['Kagami'](https://github.com/microsounds/kagami) and ['microsounds.github.io'](https://microsounds.github.io) - A 'Web-1.0 Static Microblog Processor' written in Shell, and the author's website built with it. I cannot tell you how much I love these two projects..!!
