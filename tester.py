import mmparser_test

text = """
# this is a test document.

this is a content.
"""
parser = mmparser_test.MarkdownParser()
# parser.parseText(text)
parser.parseFile('test_document.md')