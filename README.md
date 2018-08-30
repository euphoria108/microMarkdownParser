# microMarkdownParser

このプログラムではmarkdownを構文解析してHTMLファイルに変換するよ。
最低でも構文解析の機能は実装するよ。

## 対応するmarkdownの機能
* ヘッダ(h1-h6)
* テーブル
* 番号なしリスト
* 番号付きリスト
* 引用ブロック
* コードブロック
* 太字、強調、消字
* インラインコード
* リンク付き文字
* 画像

## 未対応の機能
* 1行空けによる段落替え
* 自動リンク
* バックスラッシュによる文字のエスケープ
* メールアドレスの自動変換

## 使い方
cloneしたディレクトリをカレントディレクトリに指定し、pythonコンソールを開きます。

    > import mmparser                              # モジュールを読み込みます
    > parser = mmparser.MarkdownParser()           # インスタンスを生成します。
    > parser.parseFile('path/to/markdownfile.md')  # ファイルを読み込み、構文解析を行います。
    > parser.exportHTML('filename.html')           # 指定したファイル名でHTMLを書き出します。
