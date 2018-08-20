import re
import warnings
from collections import OrderedDict

#正規表現定義エリア
block_rules = OrderedDict()
block_rules[table] = re.compile(r'''
    ^(.*)           
    \|               #symbol that distinguishes this block is a table           
    (.*)
''', re.VERBOSE)
block_rules[blockQuote] = re. compile(r"""
    (&gt;|\>)        #symbol that distinguishes this line is a start of blockquote
    (.*)
""", re.VERBOSE)
block_rules[taggedBlock] = re.compile(r"""
    ^(\<p\>)         #start tag
    (.*)
    (\<\/p\>)$       #end tag
""", re.VERBOSE)
block_rules[normalBlock] = re.compile(r"""
    (.*?)\n\s*\n
""", flags=(re.VERBOSE|re.MULTILINE|re.ADDDOT))
rules[lineBreak] = re.compile(r'\s{2,}\n')
rules[headers] = re.compile(r"""
    (\#+)            #header symbol
    (.*)
""", re.VERBOSE)
rules[links] = re.compile(r"""
    \[([^\[]+)\]\(([^\)]+)\)
""", re.VERBOSE)
rules[boldFont] = re.compile(r"""
    (\*\*|__)(.*?)\1
""", re.VERBOSE)
rules[emphasizedFont] = re.compile(r"""
    (\*|_)(.*?)\1
""", re.VERBOSE)
rules[deletedFont] = re.compile(r"""
    \~\~(.*?)\~\~
""", re.VERBOSE)
rules[inlineQuote] = re.compile(r"""
    \:\"(.*?)\"\:
""", re.VERBOSE)
rules[inlineCode] = re.compile(r"""
    `(.*?)`
""", re.VERBOSE)
rules[ulLists] = re.compile(r"""
    \s*\*\s+(.*)
""", re.VERBOSE)
rules[olLists] = re.compile(r"""
    \s*[0-9]+\.\s+(.*)
""", re.VERBOSE)
rules[horizontalRule] = re.compile(r"""
    ^((\-\s?){3,}|
    (\*\s?){3,}|
    (\_\s?){3,})$
""", re.VERBOSE)
rules[codeBlock] = re.compile(r"""
    \s{4,}\w*
""", re.VERBOSE)
rules[definitionBlock] = re.compile(r"""
    \[
    [^\[]*
    \]
    \:
    (.*)
""", re.VERBOSE)


class MarkdownParser:
    def __init__(self):
        pass

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

    def reset(self):
        self.start_pos = 0

    def parse(self, parse=True):
        if not parse:
            return
        
        i = self.start_pos
        rawdata = self.rawdata
        while i < len(rawdata):
            for rule in rules:
                if rule.match(rawdata,i):
                    start_matched = rule.match(rawdata,i).start()
                    end_matched = rule.match(rawdata,i).end()
                    if start_matched > i:
                        self.parsed_data.append(rawdata[i:start_matched])
                    self.parsed_data.append(rule[0](rawdata[start_matched:end_matched]))
                    i = end_matched

    def expandToHTML(self):
        #expand parced objects to HTML recursively        
        pass

class root(baseObject):
        
class table(baseObject):

class blockQuote(baseObject):

class lineBreak(baseObject):

class headers(baseObject):

class links(baseObject):

class taggedBlock(baseObject):
    def parse(self):
        #We don't parse any words in tagged block.
        return

class normalBlock(baseObject):

class boldFont(baseObject):

class emphasizedFont(baseObject):

class deletedFont(baseObject):

class inlineQuote(baseObject):

class inlineCode(baseObject):

class ulLists(baseObject):

class olLists(baseObject):

class horizontalRule(baseObject):
    
class codeBlock(baseObject):

class definitionBlock:


