import mmparser
import re



parser = mmparser.MarkdownParser()
# parser.parseText(text)
parser.parseFile('test_document.md')
parser.exportHTML()