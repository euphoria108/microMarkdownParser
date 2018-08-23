import re
import warnings
from collections import OrderedDict

#正規表現定義エリア
#ブロック要素
block_rules = OrderedDict()
block_rules['Table'] = re.compile(r'''
    ^(.*)           
    \|               #symbol that tells this block is a table           
    (.*)
''', re.VERBOSE)
block_rules['BlockQuote'] = re.compile(r"""
    (&gt;|\>)        #symbol that tells this line is a start of blockquote
    (.*)
""", re.VERBOSE)
block_rules['TaggedBlock'] = re.compile(r"""
    ^(\<p\>)         #start tag
    (.*)
""", re.VERBOSE)
block_rules['TaggedBlockEnd'] = re.compile(r"""
    (.*)
    (\< \s* \/ \s* p \s* \>)    #end tag
""", re.VERBOSE)
block_rules['Links'] = re.compile(r"""
    \[
        ([^\[]+)
    \]
    \(
        ([^\)]+)
    \)
""", re.VERBOSE)
block_rules['ulLists'] = re.compile(r"""
    \s*\*\s+(.*)
""", re.VERBOSE)
block_rules['olLists'] = re.compile(r"""
    \s*[0-9]+\.\s+(.*)
""", re.VERBOSE)
block_rules['HorizontalRule'] = re.compile(r"""
    ^((\-\s?){3,}|
    (\*\s?){3,}|
    (\_\s?){3,})
    \s*$
""", re.VERBOSE)
block_rules['CodeBlock'] = re.compile(r"""
    \s{4,}\w*
""", re.VERBOSE)
block_rules['DefinitionBlock'] = re.compile(r"""
    \[
    [^\[]*
    \]
    \:
    (.*)
""", re.VERBOSE)

#インライン要素
inline_rules = OrderedDict()
inline_rules['LineBreak'] = re.compile(r'\s{2,}\n')
inline_rules['BoldFont'] = re.compile(r"""
    (\*\*|__)(.*?)\1
""", re.VERBOSE)
inline_rules['EmphasizedFont'] = re.compile(r"""
    (\*|_)(.*?)\1
""", re.VERBOSE)
inline_rules['DeletedFont'] = re.compile(r"""
    \~\~(.*?)\~\~
""", re.VERBOSE)
inline_rules['InlineQuote'] = re.compile(r"""
    \:\"(.*?)\"\:
""", re.VERBOSE)
inline_rules['InlineCode'] = re.compile(r"""
    `(.*?)`
""", re.VERBOSE)

#その他個別ルール
blank_line = re.compile(r"""
    \s*\n$
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

    def preprocessData(self):
        #ファイルを行ごとに分割してlist形式にする

    def title_handler(self):
        pass

    def block_handler(self):
        pass

class baseObject:
    # this class doesn't have __init__ function.
    # __init__ will be defined at each subclasses like this:
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        
        reset()

    def reset(self):
        self.start_index = 0
        self.text_buffer = []

    def parse(self):
        if len(self.rawdata) == 0:
            return

        i = self.start_index
        
        while i < len(self.rawdata):
            if previous_line_type == 'Blank':
                self.text_buffer = []
                previous_line_type = self.parseFirstTime(self.rawdata[i])
                i += 1
                continue

            elif previous_line_type == 'Normal':
                previous_line_type = self.parseNormalBlock(self.rawdata[i])
                i += 1
                continue

            elif previous_line_type == 'Table':
                previous_line_type = self.parseTableBlock(self.rawdata[i])
                i += 1
                continue

            elif previous_line_type == 'BlockQuote':
                previous_line_type = parseBlockQuote(self.rawdata[i])
                i += 1
                continue

            elif previous_line_type == 'TaggedBlock':
                previous_line_type = self.parseTaggedBlock(self.rawdata[i])
                i += 1
                continue

            elif previous_line_type == 'CodeBlock':
                previous_line_type = self.parseCodeBlock(self.rawdata[i])
                i += 1
                continue

            elif previous_line_type == 'ulLists':
                previous_line_type = self.parseUlLists(self.rawdata[i])
                i += 1
                continue

            elif previous_line_type == 'olLists':
                previous_line_type = self.parseOlLists(self.rawdata[i])
                i += 1
                continue


    ###################################################
    # 以下、ブロック要素のparse関数。                    #
    # 返り値としてparseした行の種類を返します。（例外あり）#
    ###################################################

    def parseFirstTime(self, text):
        #block要素のルールに合致するかを判断する。
        for rule in self.block_rules.keys():
            if rule.match(text):
                self.text_buffer.append(text)
                #次の行の処理のために、現在の行の種類を保存する
                return rule
        #header要素に合致するかを判断する。
        if header_block.match(text):
            self.parsed_data.append(headers(text))
            return 'Blank'
        #block要素のいずれにも合致しなかった場合
        if not blank_line.match(text):
            self.text_buffer.append(text)
            return 'Normal'

    def parseNormalBlock(self, text):
        #次の文が---等だった場合、前の要素がh1ヘッダになる
        if header_line.match(text):
            self.parsed_data.append(headers(self.text_buffer))
            #次の文の処理は振り出しに戻したいので'Blank'を返す
            return 'Blank'
        if blank_line.match(text):
            for line in self.text_buffer:
                self.parsed_data.append(line)
            return 'Blank'
        else:
            self.text_buffer.append(text)
            return 'Normal'

    def parseTableBlock(self, text):
        if block_rules['Table'].match(text):
            self.text_buffer.append(text)
            return table
        elif blank_line.match(text):
            self.parsed_data.append(table(self.text_buffer))
            return 'Blank'
        else:
            return -1

    def parseBlockQuote(self, text):
        if block_rules['BlockQuote'].match(text):
            #一番左の'>'を空白と置き換え、さらに左端の空白を切り詰める。
            stripped_text = text.replace('>', '', 1).strip()
            self.text_buffer.append(stripped_text)
            return 'BlockQuote'
        if blank_line.match(rawdata, i):
            #空行でブロックの終わりを検知する
            self.parsed_data.append(blockQuote(self.text_buffer))
            return 'Blank'
        else:
            self.text_buffer.append(text)
            return 'BlockQuote'

    def parseTaggedBlock(self, text):
        if block_rules['TaggedBlockEnd'].match(text):
            self.parsed_data.append(taggedBlock(self.text_buffer))
            return 'Blank'
        else:
            self.text_buffer.append(text)
            return 'TaggedBlock'

    def parseCodeBlock(self, text):
        #まず、parseFirstTime()で処理されていない、text_bufferの1要素目の先頭の空白を取り除く。
        self.text_buffer[0] = self.text_buffer[0].lstrip()

        if block_rules['CodeBlock'].match(text):
            stripped_text = text.lstrip()
            self.text_buffer.append(stripped_text)
            return 'CodeBlock'
        elif blank_line.match(text):
            self.parsed_data.append(codeBlock(self.text_buffer))
            return 'Blank'
        else:
            self.text_buffer.append(text)
            return 'CodeBlock'

    def parseUlLists(self, text):
        base_indent = self.countIndent(self.text_buffer[0])
        current_line_indent = self.countIndent(text)
        if block_rules['ulLists'].match(text):
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する
            if current_line_indent >= base_indent + 2 and current_line_indent <= base_indent + 5:
                # 左端をbase_indent分だけトリミングする
                stripped_text = text.replace(' ', '', base_indent)
                self.text_buffer.append(stripped_text)
                return 'ulLists'
            else:
                # 左端の'*'マークまでトリミングする
                stripped_text = re.sub(r'\W*[\-\+\*]\s', '', text, 1)
                self.text_buffer.append(stripped_text)
                return 'ulLists'
        elif block_rules['olLists'].match(text):
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する
            if current_line_indent >= base_indent + 2 and current_line_indent <= base_indent + 5:
                # 左端をbase_indent分だけトリミングする
                stripped_text = text.replace(' ', '', base_indent)
                self.text_buffer.append(stripped_text)
                return 'ulLists'
            else:
                # 左端の空白をトリミングする
                stripped_text = text.lstrip()
                self.text_buffer[-1] = self.text_buffer[-1] + ' ' + stripped_text
                return 'ulLists'
        elif blank_line.match(text):
            self.parsed_data.append(ulLists(self.text_buffer))
            return 'Blank'
        else:
            # 左端の空白をトリミングする
            stripped_text = text.lstrip()
            self.text_buffer[-1] = self.text_buffer[-1] + ' ' + stripped_text
            return 'ulLists'

    def parseOlLists(self, text):
        base_indent = self.countIndent(self.text_buffer[0])
        current_line_indent = self.countIndent(text)
        if block_rules['olLists'].match(text):
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する
            if current_line_indent >= base_indent + 2 and current_line_indent <= base_indent + 5:
                # 左端をbase_indent分だけトリミングする
                stripped_text = text.replace(' ', '', base_indent)
                self.text_buffer.append(stripped_text)
                return 'olLists'
            else:
                # 左端の'*'マークまでトリミングする
                stripped_text = re.sub(r'\W*[0-9]\.\s', '', text, 1)
                self.text_buffer.append(stripped_text)
                return 'olLists'
        elif block_rules['ulLists'].match(text):
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する
            if current_line_indent >= base_indent + 2 and current_line_indent <= base_indent + 5:
                # 左端をbase_indent分だけトリミングする
                stripped_text = text.replace(' ', '', base_indent)
                self.text_buffer.append(stripped_text)
                return 'olLists'
            else:
                # 左端の空白をトリミングする
                stripped_text = text.lstrip()
                self.text_buffer[-1] = self.text_buffer[-1] + ' ' + stripped_text
                return 'olLists'
        elif blank_line.match(text):
            self.parsed_data.append(ulLists(self.text_buffer))
            return 'Blank'
        else:
            # 左端の空白をトリミングする
            stripped_text = text.lstrip()
            self.text_buffer[-1] = self.text_buffer[-1] + ' ' + stripped_text
            return 'olLists'

    def expandToHTML(self):
        #expand parced objects to HTML recursively        
        pass

    @staticmethod
    def countIndent(text):
        blank = re.compile(r'\W')
        count = 0
        while blank.match(text):
            count += 1
            text = text.replace(' ', '', 1)
        return count

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


