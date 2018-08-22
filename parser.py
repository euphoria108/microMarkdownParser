import re
import warnings
from collections import OrderedDict

#正規表現定義エリア
#ブロック要素
block_rules = OrderedDict()
block_rules[table] = re.compile(r'''
    ^(.*)           
    \|               #symbol that tells this block is a table           
    (.*)
''', re.VERBOSE)
block_rules[blockQuote] = re.compile(r"""
    (&gt;|\>)        #symbol that tells this line is a start of blockquote
    (.*)
""", re.VERBOSE)
block_rules[taggedBlock] = re.compile(r"""
    ^(\<p\>)         #start tag
    (.*)
    (\<\/p\>)$       #end tag
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

#インライン要素
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

#その他個別ルール
blank_line = re.compile(r"""
    \s*\n
""",　re.VERBOSE)
header_line = re.compile(r"""
    ^((\-){3,}|
    (\*){3,}|
    (\=){3,})
    /s*$
""",　re.VERBOSE)
header_block = re.compile(r"""
    (\#+)            #header symbol
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
    # def __init__(self, listed_data):
    #     self.rawdata = listed_data
    #     self.parsed_data = []
    #     self.text_buffer = []
    #     reset()

    def reset(self):
        self.start_index = 0

    def parse(self):
        if len(self.rawdata) == 0:
            return

        i = self.start_index
        text_buffer = []
        # if previous_line_type = 'Blank'
            if previous_line_type == "blank":
                
            elif previous_line_type == 'Normal':
                #次の文が---等だった場合、前の要素がh1ヘッダになる
                if header_line.match(rawdata, i):
                    instance = headers(text_buffer,1)
                    previous_line_type = 'Blank'
                    return
                if blank_line.match(rawdata, i):
                    self.appendParsedText(text_buffer)
                    i = re.compile(r'.*').search(rawdata).end()
                    previous_line_type = 'Blank'
                    return
                else:
                    #行末のインデックスをjに代入
                    j = re.compile(r'.*').search(rawdata).end()
                    text_buffer += rawdata[i:j]
                    i = j
                    return

            elif previous_line_type == table:
                if block_rules[table].match(rawdata, i):
                    start_matched = block_rules[table].match(rawdata, i).start()
                    end_matched = block_rules[table].match(rawdata, i).end()
                    instance.appendRawData(rawdata[start_matched:end_matched])
                    i = end_matched
                    return
                if blank_line.match(rawdata, i):
                    self.appendParsedObj(instance)
                    #行末にインデックスを移動
                    i = re.compile(r'.*').search(rawdata).end()
                    previous_line_type = 'Blank'
                    return

            elif previous_line_type == blockQuote:
                if block_rules[blockQuote].match(rawdata, i):
                    #行頭の>を取り除く動作は個別クラスで実装する
                    start_matched = block_rules[blockQuote].match(rawdata, i).start()
                    end_matched = block_rules[blockQuote].match(rawdata, i).end()
                    instance.appendRawData(rawdata[start_matched:end_matched])
                    i = end_matched
                    return
                if blank_line.match(rawdata, i):
                    #空行でブロックの終わりを検知する
                    self.appendParsedObj(instance)
                    #行末にインデックスを移動
                    i = re.compile(r'.*').search(rawdata).end()
                    previous_line_type = 'Blank'
                    return
                else:
                    j = re.compile(r'.*').search(rawdata).end()
                    instance.appendRawData(rawdata[i:j])
                    i = j
                    return

        while i < len(rawdata):
            ##ブロック要素についての処理
            #前の行の要素が空行の場合、または文頭の場合:
            if previous_line_type = 'Blank':
                matchBlockElements('Blank')

            #前の行の要素が通常文だった場合
            if previous_line_type == 'Normal':
                matchBlockElements('Normal')

            #以下、前の行がそれぞれのブロック要素のときについて実装する。
            if previous_line_type == table:
                matchBlockElements(table)

            if previous_line_type == blockQuote:
                matchBlockElements(blockQuote)

    def parseFirstTime(self, listed_data, start_index):
        #block要素のルールに合致するかを判断する。
        for rule in self.block_rules.keys():
            if rule.match(rawdata, i):
                start_matched = rule.match(rawdata,i).start()
                end_matched = rule.match(rawdata,i).end()
                instance = rule(rawdata[start_matched:end_matched])
                #次の行の処理のために、現在の行の種類を保存する
                previous_line_type = rule
                i = end_matched
                return 
        #header要素に合致するかを判断する。
        if header_block.match(rawdata, i):
            start_matched = header_block.match(rawdata,i).start()
            end_matched = header_block.match(rawdata,i).end()
            instance = headers(rawdata[start_matched:end_matched])
            self.appendParsedObj(instance)
            i = end_matched
            previous_line_type = "Blank"
            return
        #block要素のいずれにも合致しなかった場合
        if not blank_line.match(rawdata, i):
            #行末のインデックスをjに代入
            j = re.compile(r'.*').search(rawdata).end()
            text_buffer += rawdata[i:j]
            previous_line_type = "Normal"
            i = j
            return

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


