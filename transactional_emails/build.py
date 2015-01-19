#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import fnmatch

from premailer import transform
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('transactional_emails', 'templates'))


def gen_find(filepat, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield name


def gen_jinja(filenames):
    for filename in filenames:
        template = env.get_template(filename)
        yield filename, template.render()


def gen_premailer(htmls):
    for html in htmls:
        yield html[0], transform(html[1])


def write_output(emails, output):
    for email in emails:
        f = open(output + '/' + email[0], 'w')
        f.write(email[1].encode("utf-8"))

files = gen_find("*.html", "templates")
htmls = gen_jinja(files)
emails = gen_premailer(htmls)
write_output(emails, "output")
