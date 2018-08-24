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
block_rules['ulLists'] = re.compile(r"""
    \s*\*\s+(.*)
""", re.VERBOSE)
block_rules['olLists'] = re.compile(r"""
    \s*[0-9]+\.\s+(.*)
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
inline_rules['InlineCode'] = re.compile(r"""
    (`{1,})(.*?)\1
""", re.VERBOSE)
inline_rules['Links'] = re.compile(r"""
    \[
        ([^\[]+)
    \]
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
horizontal_rule = re.compile(r"""
    ^((\-\s?){3,}|
    (\*\s?){3,}|
    (\_\s?){3,})
    \s*$
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
    # def __init__(self, listed_data):
    #     self.rawdata = listed_data
    #     self.parsed_data = []
    #     self.block_reg = []
    #     self.inline_reg = []
    #     reset()

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

            #ブロック要素として処理ができないとき、通常文として処理する。
            elif previous_line_type == -1
                previous_line_type = self.parseNormalBlock(self.rawdata[i])
                i += 1
                continue

    #####################################################
    # 以下、ブロック要素のparse関数。                      #
    # 返り値としてparseした行の種類を返します。（例外あり）  #
    # 関数内でオブジェクトを生成したらparse()を実行すること。#
    #####################################################

    def parseFirstTime(self, text):
        #block要素のルールに合致するかを判断する。
        for rule in self.block_rules.keys():
            if rule.match(text):
                self.text_buffer.append(text)
                #次の行の処理のために、現在の行の種類を保存する
                return rule
        if header_block.match(text):
            self.parsed_data.append(headers(text))
            return 'Blank'
        if horizontal_rule.match(text):
            self.parsed_data.append(horizontalRule())
            return 'Blank'
        #block要素のいずれにも合致しなかった場合
        if not blank_line.match(text):
            self.text_buffer.append(text)
            return 'Normal'

    def parseInlineElements(self, text):
        parsed_text = []
        for dictitem in self.inline_reg:
            if dictitem['rule'].search(text):
                element = dictitem['rule'].search(text).group()
                instance = dictitem['class'](element)
                instance.shapeData()
                #（elementsを整形する処理は個別のクラスで実装）
                devided_text = re.sub(dictitem['rule'], '_splitter_', text, 1).split('_splitter_')
                #before_element and after_element should be list.
                before_element = self.parseInlineElements(devided_text[0])
                after_element = self.parseInlineElements(devided_text[1])
                for item in before_element:
                    if item != '':
                        parsed_text.append(item)
                parsed_text.append(instance)
                for item in after_element:
                    if item != '':
                        parsed_text.append(item)
                return parsed_text
        #if any inline rules didn't match with text
        return [text]

    def parseNormalBlock(self, text):
        #次の文が---等だった場合、前の要素がh1ヘッダになる
        if header_line.match(text):
            self.parsed_data.append(headers(self.text_buffer))
            #次の文の処理は振り出しに戻したいので'Blank'を返す
            return 'Blank'
        if blank_line.match(text):
            for line in self.text_buffer:
                parsed_line = parseInlineElements(line)
                for item in parsed_line:
                    self.parsed_data.append(item)
            return 'Blank'
        else:
            self.text_buffer.append(text)
            return 'Normal'

    def parseTableBlock(self, text):
        if block_rules['Table'].match(text):
            self.text_buffer.append(text)
            return 'Table'
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
        #this method will be overrided at each subclasses.
        raise NotImplementedError

    @staticmethod
    def countIndent(text):
        blank = re.compile(r'\W')
        count = 0
        while blank.match(text):
            count += 1
            text = text.replace(' ', '', 1)
        return count

class root(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()
        
class table(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

class blockQuote(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

class headers(baseObject):
    def __init__(self, data, level=None):
        if level:
            self.level = level
            self.parsed_data = [data]
        else:
            self.rawdata = rawdata
            self.parsed_data = []
            reset()

class taggedBlock(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

    def parse(self):
        #We don't parse any words in tagged block.
        return

class ulLists(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

class olLists(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

class horizontalRule(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

class codeBlock(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

class normalBlock(baseObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.block_reg = []
        self.inline_reg = []
        reset()

class lineBreak(baseObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        self.rawdata = []

    def parse(self):
        pass

class links(baseObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []

class boldFont(baseObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        shaped_text = self.rawdata.lstrip('*', 2).rstrip('*', 2)
        self.parsed_data = shaped_text

    def parse(self):
        pass

class emphasizedFont(baseObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        rule = re.compile(r'(\*\*)(?P<content> .*?)\1')
        shaped_text = rule.search(self.rawdata).group('content').strip()
        self.parsed_data = shaped_text

    def parse(self):
        pass

class deletedFont(baseObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        rule = re.compile(r'(\~\~)(?P<content> .*?)\1')
        shaped_text = rule.search(self.rawdata).group('content').strip()
        self.parsed_data = shaped_text

    def parse(self):
        pass

class inlineCode(baseObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        rule = re.compile(r'(`{1,})(?P<content> .*?)\1')
        shaped_text = rule.search(self.rawdata).group('content').strip()
        self.parsed_data = shaped_text

    def parse(self):
        pass
    

class definitionBlock:


