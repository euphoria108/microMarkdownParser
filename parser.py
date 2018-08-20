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
block_rules[headers] = re.compile(r"""
    (\#+)            #header symbol
    (.*)
""", re.VERBOSE)
block_rules[links] = re.compile(r"""
    \[
        ([^\[]+)
    \]
    \(
        ([^\)]+)
    \)
""", re.VERBOSE)
block_rules[ulLists] = re.compile(r"""
    \s*\*\s+(.*)
""", re.VERBOSE)
block_rules[olLists] = re.compile(r"""
    \s*[0-9]+\.\s+(.*)
""", re.VERBOSE)
block_rules[horizontalRule] = re.compile(r"""
    ^((\-\s?){3,}|
    (\*\s?){3,}|
    (\_\s?){3,})
    \s*$
""", re.VERBOSE)
block_rules[codeBlock] = re.compile(r"""
    \s{4,}\w*
""", re.VERBOSE)
block_rules[definitionBlock] = re.compile(r"""
    \[
    [^\[]*
    \]
    \:
    (.*)
""", re.VERBOSE)

blank_line = re.compile(r"""
    \s*\n$
""",　re.VERBOSE)
header_line = re.compile(r"""
    ^((\-){3,}|
    (\*){3,}|
    (\=){3,})
    /s*$
""",　re.VERBOSE)

inline_rules = OrderedDict()
inline_rules[lineBreak] = re.compile(r'\s{2,}\n')
inline_rules[boldFont] = re.compile(r"""
    (\*\*|__)(.*?)\1
""", re.VERBOSE)
inline_rules[emphasizedFont] = re.compile(r"""
    (\*|_)(.*?)\1
""", re.VERBOSE)
inline_rules[deletedFont] = re.compile(r"""
    \~\~(.*?)\~\~
""", re.VERBOSE)
inline_rules[inlineQuote] = re.compile(r"""
    \:\"(.*?)\"\:
""", re.VERBOSE)
inline_rules[inlineCode] = re.compile(r"""
    `(.*?)`
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
        self.rawdata = rawdata
        self.parsed_data = []
        reset()

    def reset(self):
        self.start_pos = 0

    def appendRawData(self, data):
        self.rawdata += data

    def appendParsedObj(self, obj):
        'parse済のデータを格納すると同時にparse関数を呼びます。'
        obj.parse()
        self.parsed_data.append(obj)
        

    def parse(self, parse=True):
        if not parse:
            return
        
        i = self.start_pos
        rawdata = self.rawdata
        text_buffer = ""
        previous_line_type = 'Blank'
        while i < len(rawdata):
            #前の行の要素が空行の場合、または文頭の場合:
            if previous_line_type = 'Blank':
                #block要素のルールに合致するかを判断する。
                for rule in block_rules.keys():
                    if rule.match(rawdata, i):
                        start_matched = rule.match(rawdata,i).start()
                        end_matched = rule.match(rawdata,i).end()
                        instance = rule(rawdata[start_matched:end_matched])
                        #次の行の処理のために、現在の行の種類を保存する
                        previous_line_type = rule
                        i = end_matched
                        break 
                #block要素のいずれにも合致しなかった場合
                if not blank_line.match(rawdata, i):
                    #行末のインデックスをjに代入
                    j = re.compile(r'.*').search(rawdata).end()
                    text_buffer += rawdata[i:j]
                    previous_line_type = "Normal"
                    i = j

            if previous_line_type == 'Normal':
                if header_line.match(rawdata, i):
                    instance = header(text_buffer)

            if previous_line_type == table:
                if block_rules[table].match(rawdata, i):
                    start_matched = block_rules[table].match(rawdata, i).start()
                    end_matched = block_rules[table].match(rawdata, i).end()
                    instance.appendRawData(rawdata[start_matched:end_matched])
                    i = end_matched
                if blank_line.match(rawdata, i):
                    self.appendParsedObj(instance)
                    #行末にインデックスを移動
                    i = re.compile(r'.*').search(rawdata).end()

            

    def expandToHTML(self):
        #expand parced objects to HTML recursively        
        pass

class root(baseObject):
        
class table(baseObject):

class blockQuote(baseObject):

class lineBreak(baseObject):

class headers(baseObject):
    def __init__(self, data, level=None):
        if level:
            self.level = level
            self.parsed_data = [data]
        else:
            self.rawdata = rawdata
            self.parsed_data = []
            reset()

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


