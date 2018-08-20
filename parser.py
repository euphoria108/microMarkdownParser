import re
import warnings

#正規表現定義エリア
rules = {}
rules['table block'] = re.compile(r'''
    ^(.*)           
    \|               #symbol that distinguishes this block is a table           
    (.*)
''', re.VERBOSE)
rules['blockquote'] = re. compile(r"""
    (&gt;|\>)        #symbol that distinguishes this line is a start of blockquote
    (.*)
""", re.VERBOSE)
rules['linebreak'] = re.compile(r'\s{2,}\n')
rules['headers'] = re.compile(r"""
    (\#+)            #header symbol
    (.*)
""", re.VERBOSE)
rules['tag_block'] = re.compile(r"""
    ^(\<p\>)         #start tag
    (.*)
    (\<\/p\>)$       #end tag
""", re.VERBOSE)
rules['links'] = re.compile(r"""
    \[([^\[]+)\]\(([^\)]+)\)
""", re.VERBOSE)
rules['bold'] = re.compile(r"""
    (\*\*|__)(.*?)\1
""", re.VERBOSE)
rules['emphasis'] = re.compile(r"""
    (\*|_)(.*?)\1
""", re.VERBOSE)
rules['delete'] = re.compile(r"""
    \~\~(.*?)\~\~
""", re.VERBOSE)
rules['quote'] = re.compile(r"""
    \:\"(.*?)\"\:
""", re.VERBOSE)
rules['inline code'] = re.compile(r"""
    `(.*?)`
""", re.VERBOSE)
rules['ul lists'] = re.compile(r"""
    \s*\*\s+(.*)
""", re.VERBOSE)
rules['ol lists'] = re.compile(r"""
    \s*[0-9]+\.\s+(.*)
""", re.VERBOSE)
rules['horizontal rule'] = re.compile(r"""
    ^((\-\s?){3,}|
    (\*\s?){3,}|
    (\_\s?){3,})$
""", re.VERBOSE)
rules['code block'] = re.compile(r"""
    \s{4,}\w*
""", re.VERBOSE)
rules['definition area'] = re.compile(r"""
    \[
    [^\[]*
    \]
    \:
    (.*)
""", re.VERBOSE)


class MarkdownParser:
    def __init__(self):

    def title_handler(self):
        pass

    def block_handler(self):
        pass

class baseObject:
    def __init__(self, rawdata):
        #コンストラクタを呼ぶと同時にparse関数を呼びます。
        #このことにより、インスタンスが生成されると、その中身を再帰的にparseします。
        self.rawdata = rawdata
        self.parsed_data = []
        parse()

    def parse(self, parse=True):
        if not parse:
            return
        

