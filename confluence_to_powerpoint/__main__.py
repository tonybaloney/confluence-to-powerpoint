from __future__ import absolute_import
import yaml

from .scrape import scrape
from .scrape import parse

settings = None
with open('settings.cfg', 'r') as settings:
    settings = yaml.load(settings)

scrape(settings['url'], settings['page'], settings['user'], settings['password'])

parsed_table = None
with open('table_dump.html', 'r') as table_dump:
    contents = table_dump.read()
    parsed_table = parse(contents)

print ("Parsed table")

print(parsed_table)