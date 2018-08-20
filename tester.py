import re
from parser import MarkdownParser

class Tester(MarkdownParser):
    def __init__(self, file):
        with open(file, 'rt') as f:
            self.rawdata = f.read()
            self.parsed_object = self.parse() 