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
    (\[)
        ([^\[]+)
    (\])
    ([\[\(])
        (.*?)
    ([\]\)])
""", re.VERBOSE)
inline_rules['Images'] = re.compile(r"""
    (!\[)
        ([^\[]+)
    (\])
    ([\[\(])
        (.*?)
    ([\]\)])
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
definition_block = re.compile(r"""
    (\[)
    ([^\[]+)
    (\])
    \:
    (.*)
""", re.VERBOSE)


class MarkdownParser:
    def __init__(self):
        self.rootobject = root()
        return

    def parseFile(self, filepath):
        """
        This function will read markdown file and parse it.
        Only a file encoded with UTF-8 is appliable.
        """
        #ファイルを行ごとに分割してlist形式にする
        with open(filepath, 'rt', encoding='utf-8') as f:
            data = f.read()
            splitted_data = []
            for line in data.split('\n'):
                splitted_data.append(line)
            #parse関数の処理の都合上、末尾に空行を挿入する。
            splitted_data.append('')
            self.rootobject.rawdata = splitted_data
        self.rootobject.parse()

    def parseText(self, textdata):
        data = textdata
        splitted_data = []
        for line in data.split('\n'):
            splitted_data.append(line)
        #parse関数の処理の都合上、末尾に空行を挿入する。
        splitted_data.append('')
        self.rootobject.rawdata = splitted_data
        self.rootobject.parse()
    
    def title_handler(self):
        pass

    def block_handler(self):
        pass

#URLリンクのid情報を保存する辞書オブジェクト
link_id_info = {}

class blockObject:
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.parsed_data = []
        self.inline_reg = [
            {'rule':'LineBreak'      , 'class':lineBreak      },
            {'rule':'BoldFont'       , 'class':boldFont       },
            {'rule':'EmphasizedFont' , 'class':emphasizedFont },
            {'rule':'DeletedFont'    , 'class':deletedFont    },
            {'rule':'InlineCode'     , 'class':inlineCode     },
            {'rule':'Links'          , 'class':links          },
            {'rule':'Images'         , 'class':images         },
        ]
        reset()

    def reset(self):
        self.start_index = 0
        self.text_buffer = []

    def parse(self):
        if len(self.rawdata) == 0:
            return

        i = self.start_index
        previous_line_type = 'Blank'
        
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
        del self.rawdata
        return

    #####################################################
    # 以下、ブロック要素のparse関数。                      #
    # 返り値としてparseした行の種類を返します。（例外あり）  #
    # 関数内でオブジェクトを生成したらparse()を実行すること。#
    #####################################################

    def parseFirstTime(self, text):
        #block要素のルールに合致するかを判断する。
        for rule in block_rules.keys():
            if block_rules[rule].match(text):
                self.text_buffer.append(text)
                #次の行の処理のために、現在の行の種類を保存する
                return rule
        if header_block.match(text):
            instance = headers(text)
            instance.parse()
            self.parsed_data.append(instance)
            return 'Blank'
        if horizontal_rule.match(text):
            self.parsed_data.append(horizontalRule())
            return 'Blank'
        if definition_block.match(text):
            self.parseDefinitionBlock(text)
            return 'Blank'
        #block要素のいずれにも合致しなかった場合
        if not blank_line.match(text):
            self.text_buffer.append(text)
            return 'Normal'

    def parseInlineElements(self, text):
        parsed_text = []
        for dit in self.inline_reg:
            if dit['rule'].search(text):
                element = dit['rule'].search(text).group()
                instance = dit['class'](element)
                instance.shapeData()
                #（elementsを整形する処理は個別のクラスで実装）
                devided_text = re.sub(dit['rule'], '_splitter_', text, 1).split('_splitter_')
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
        #if all inline rules didn't match with text
        return [text]

    def parseNormalBlock(self, text):
        #次の文が---等だった場合、前の要素がh1ヘッダになる
        if header_line.match(text):
            instance = headers(self.text_buffer)
            instance.parse()
            self.parsed_data.append(instance)
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
            instance = table(self.text_buffer)
            instance.parse()
            self.parsed_data.append(instance)
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
            instance = blockQuote(self.text_buffer)
            instance.parse()
            self.parsed_data.append(instance)
            return 'Blank'
        else:
            self.text_buffer.append(text)
            return 'BlockQuote'

    def parseTaggedBlock(self, text):
        if block_rules['TaggedBlockEnd'].match(text):
            instance = taggedBlock(self.text_buffer)
            instance.parse()
            self.parsed_data.append(instance)
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
            instance = codeBlock(self.text_buffer)
            instance.parse()
            self.parsed_data.append(instance)
            return 'Blank'
        else:
            self.text_buffer.append(text)
            return 'CodeBlock'

    def parseUlLists(self, text):
        #現在のリストの基準となるインデントを元に、各行が入れ子なのか否かを判断する。
        base_indent = self.countIndent(self.text_buffer[0])
        current_line_indent = self.countIndent(text)
        if block_rules['ulLists'].match(text):
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する
            # 行頭の'*'を残すことによって、子objectのparse関数がリストだと認識できるようにする。
            if current_line_indent >= base_indent + 2 and current_line_indent <= base_indent + 5:
                # 左端をbase_indent分だけトリミングする
                stripped_text = t
                # 左端の'*'マークまでトリミングする
                stripped_text = re.sub(r'\W*[\-\+\*]\s', '', text, 1)
                self.text_buffer.append(stripped_text)
                return 'ulLists'
        elif block_rules['olLists'].match(text):
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する
            # 行頭の'1.'を残すことによって、子objectのparse関数がリストだと認識できるようにする。
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
            instance = ulLists(self.text_buffer)
            instance.parse()
            self.parsed_data.append(instance)
            return 'Blank'
        else:
            # その他の場合、現在の行をリストの最後のitemの中身に含める。
            stripped_text = text.lstrip()
            self.text_buffer[-1] = self.text_buffer[-1] + ' ' + stripped_text
            return 'ulLists'

    def parseOlLists(self, text):
        base_indent = self.countIndent(self.text_buffer[0])
        current_line_indent = self.countIndent(text)
        if block_rules['olLists'].match(text):
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する。
            # 行頭の'1.'を残すことによって、子objectのparse関数がリストだと認識できるようにする。
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
            # 現在のインデントより2つ以上5つ以下インデントが大きくなったとき、入れ子のリストだと認識する。
            # 行頭の'*'を残すことによって、子objectのparse関数がリストだと認識できるようにする。
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
            instance = ulLists(self.text_buffer)
            instance.parse()
            self.parsed_data.append(instance)
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

    def parseDefinitionBlock(text):
        rule_id = re.compile(r"(\[)(?P<id>[^\[]+)(\]:)")
        rule_option = re.compile(r'([\"\'\(])(?P<option>.*)\1')
        #urlは、元のtextからidとoptional titleを取り除くことによって取得する。
        url = text
        optional_title = None
        id = rule_id.search(text).group('id')
        if rule_option.search(text):
            optional_title = rule_option.search(text).group('option')
            url = rule_option.sub('', url)
        url = rule_id.sub('', url)
        url = url.strip()
        #link_id_infoは、{id: {'url': url, 'optional_title': optional_title}, ...}
        #という形式をとる。
        id_information = {}
        id_information['url'] = url
        id_information['optional_title'] = optional_title
        link_id_info[id] = id_information
        return

class inlineObject:
    # this class will be inherited by inline objects.
    def expandToHTML(self):
        #this method will be overrided at each subclasses.
        raise NotImplementedError

class root(blockObject):
    pass
        
class table(blockObject):
    def __init__(self, listed_data):
        self.rawdata = listed_data
        self.headers = []
        self.alignments = []
        self.contents = []
        reset()

    def parse(self):
        i = self.start_index
        # 2行目の要素によって、|---|---|タイプか---|---タイプかを判別し、場合分けする。
        formal = re.compile(r'\|(\-{3,})\|')
        informal = re.compile(r'(\-{3,})\|')
        if formal.match(self.rawdata[1]):
            # [1,2,3,4,5][1:-1] = [2,3,4]
            self.headers = self.rawdata[i].split('|')[1:-1]
            i += 1
            self.alignments = self.rawdata[i].split('|')[1:-1]
            i += 1
            while i < len(self.rawdata):
                self.contents.append(self.rawdata[i].split('|')[1:-1])
        if informal.match(self.rawdata[1]):
            self.headers = self.rawdata[i].split('|')
            i += 1
            self.alignments = self.rawdata[i].split('|')
            i += 1
            while i < len(self.rawdata):
                self.contents.append(self.rawdata[i].split('|'))
                i += 1
        # 2行目の要素からalignmentの判断をする
        left_align = re.compile(r'\:(\-{3,})$')
        right_align = re.compile(r'(\-{3,})\:$')
        center_align = re.compile(r'\:(\-{3,})\:$')
        j = 0
        while j < len(self.alignments):
            if left_align.match(self.alignments[j]):
                self.alignments[j] = 'left'
            elif right_align.match(self.alignments[j]):
                self.alignments[j] = 'right'
            elif center_align.match(self.alignments[j]):
                self.alignments[j] = 'center'
            else:
                self.alignments[j] = None
            j += 1
        del self.rawdata
        return


class blockQuote(blockObject):
    pass

class headers(blockObject):
    def __init__(self, data, level=None):
        if level:
            self.level = level
            self.parsed_data = [data]
        else:
            self.rawdata = data
            self.parsed_data = []
            self.level = None
            reset()

    def parse(self):
        if self.level == None:
            self.level = self.countSharp(self.rawdata)
            self.parsed_data = self.rawdata.strip('#').strip()
            del self.rawdata
        return

    @staticmethod
    def countSharp(text):
        text = text.lstrip()
        sharp = re.compile(r'\#')
        count = 0
        while sharp.match(text):
            count += 1
            text = text.replace('#', '', 1)
        return count

class taggedBlock(blockObject):
    def parse(self):
        # 何もせずにparsed_dataへ格納
        for line in self.rawdata:
            self.parsed_data.append(line)
        del self.rawdata
        return

class ulLists(blockObject):
    pass

class olLists(blockObject):
    pass

class horizontalRule(blockObject):
    def __init__(self, listed_data):
        pass

class codeBlock(blockObject):
    def parse(self):
        # 何もせずにparsed_dataへ格納
        for line in self.rawdata:
            self.parsed_data.append(line)
        del self.rawdata
        return

class normalBlock(blockObject):
    pass

class lineBreak(inlineObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        del self.rawdata
        return


class links(inlineObject):
    def __init__(self, string):
        self.rawdata = string
        self.title = ""
        self.url = None
        self.id = None

    def shapeData(self):
        rule_url = re.compile(r'''
        \[
            (?P<title> [^ \[]+)
        \]
        \(
            (?P<url> [^\(]*?)
        \)
        ''', re.VERBOSE)
        rule_id = re.compile(r'''
        \[
            (?P<title> [^ \[]+)
        \]
        \[
            (?P<id> [^\[]*?)
        \]
        ''', re.VERBOSE)

        if rule_url.search(self.rawdata):
            self.title = rule_url.search(self.rawdata).group('title')
            self.url = rule_url.search(self.rawdata).group('url')
        if rule_id.search(self.rawdata):
            self.title = rule_id.search(self.rawdata).group('title')
            self.id = rule_id.search(self.rawdata).group('id')
            if self.id = '':
                self.id = self.title
        del self.rawdata
        return

class images(inlineObject):
    def __init__(self, string):
        self.rawdata = string
        self.title = ""
        self.url = None
        self.id = None

    def shapeData(self):
        rule_url = re.compile(r'''
        \!\[
            (?P<title> [^ \[]+)
        \]
        \(
            (?P<url> [^\(]*?)
        \)
        ''', re.VERBOSE)
        rule_id = re.compile(r'''
        \!\[
            (?P<title> [^ \[]+)
        \]
        \[
            (?P<id> [^\[]*?)
        \]
        ''', re.VERBOSE)

        if rule_url.search(self.rawdata):
            self.title = rule_url.search(self.rawdata).group('title')
            self.url = rule_url.search(self.rawdata).group('url')
        if rule_id.search(self.rawdata):
            self.title = rule_id.search(self.rawdata).group('title')
            self.id = rule_id.search(self.rawdata).group('id')
            if self.id = '':
                self.id = self.title
        del self.rawdata
        return

class boldFont(inlineObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        rule = re.compile(r'(\*\*)(?P<content> .*?)\1')
        shaped_text = rule.search(self.rawdata).group('content').strip()
        self.parsed_data = shaped_text
        del self.rawdata
        return


class emphasizedFont(inlineObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        rule = re.compile(r'(\*)(?P<content> .*?)\1')
        shaped_text = rule.search(self.rawdata).group('content').strip()
        self.parsed_data = shaped_text
        del self.rawdata
        return


class deletedFont(inlineObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        rule = re.compile(r'(\~\~)(?P<content> .*?)\1')
        shaped_text = rule.search(self.rawdata).group('content').strip()
        self.parsed_data = shaped_text
        del self.rawdata
        return


class inlineCode(inlineObject):
    def __init__(self, string):
        self.rawdata = string
        self.parsed_data = []
        
    def shapeData(self):
        rule = re.compile(r'(`{1,})(?P<content> .*?)\1')
        shaped_text = rule.search(self.rawdata).group('content').strip()
        self.parsed_data = shaped_text
        del self.rawdata
        return

