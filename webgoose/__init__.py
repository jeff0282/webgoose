
"""
Webgoose Static Site Generator

---

MIT License

Copyright (c) 2022 Travis F. Campbell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# VERSION INFORMATION
from webgoose.version import version
from webgoose.version import version_info


# CONFIG
from webgoose.config import config


# FILE TRAVERSER
from webgoose.file_traverser import file_traverser


# GRABBERS
from webgoose.site_grabber import SiteGrabber 
from webgoose.page_grabber import PageGrabber 


# PAGE QUERIER
from webgoose.page_querier import PageQuerier


# BASE EXCEPTION CLASS
from webgoose.webgoose_exception import WebgooseException

