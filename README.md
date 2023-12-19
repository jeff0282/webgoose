# Webgoose - A Static-Site Generator Framework

**[Roughly Mid-Way In-Development]:** For an idea of how Webgoose development has been, please see ['webgoose.net'](https://www.webgoose.net)

## Le Petit Preface
Over 12 months of development. 12 complete restarts. This project has become something of a Sisyphus of Software, never going anywhere.

Starting life as a imageboard-style personal website engine (which worked scarily well), it went through a minimalism phase, a tree-centric phase, multiple identity crises, and has now developed into a static site generator framework

Who knows, maybe this idea will fall through as well. Though I have hope that this revision will become something!


## Provisional API
Below is a basic example using Webgoose to contruct a static website, demonstrating some of the core functionality of Webgoose.
```python
from    collections import      defaultdict
from    typing      import      Type
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

    # make a dedicated page for every tag
    for tag, posts in component.posts["tags"].values():
        component.add(f"tags/{tag.lower()}", Page(".src/blog/tags.md"))

    
@blog.attach("posts/")
def posts(component):
    """
    Posts within the blog section of the site
    """

    component["tags"] = defaultdict(list)
    for path in Path.glob(".src/posts/*.md")
        post = Page(path)

        # add post to tags dict
        for tag_name in post.meta.get("tag", []):
            component["tags"][tag_name].append(post)

        component.add(path.stem + ".html", Page(path))


if __file__ == __main__:
    site.render("./build")

```


## Credits & Notes

Webgoose has been heavily inspired by a variety of projects and websites:

- ['Astro'](https://astro.build) and ['Nyabla.net V2'](https://https://github.com/nyabla/nyabla.net-v2) - An incredibly extensible site generation framework, and an older version of ['Nela's'](https://nyabla.net) personal website made using it.
- ['Lightweight'](https://github.com/mdrachuk/lightweight) - A Nice & Simple Static-Site Generator Framework; Inspiration for quite a lot of the Webgoose API.
- ['Kagami'](https://github.com/microsounds/kagami) and ['microsounds.github.io'](https://microsounds.github.io) - A 'Web-1.0 Static Microblog Processor' written in Shell, and the author's website built with it. I cannot tell you how much I love these two projects..!!
