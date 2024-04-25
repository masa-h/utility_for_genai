# ソースコード貼り付け用のマークダウン生成スクリプト

このスクリプトは、指定されたディレクトリ内のソースコードファイルをマークダウン形式に変換し、クリップボードにコピーします。

## 使い方

```command
python files_to_paste.py <ディレクトリ> <拡張子>
```

- `<ディレクトリ>`: ソースコードファイルが含まれるディレクトリのパス
- `<拡張子>`: 対象とするファイルの拡張子（例: `.py`）。すべてのファイルを対象とする場合は `all` を指定

## 機能

- 指定されたディレクトリ内を再帰的に探索し、指定された拡張子に一致するファイルを見つけます。
- 各ファイルの内容をマークダウン形式に変換します。
  - ファイルのパスをヘッダーとして追加
  - ファイルの内容をコードブロック内に配置
- 変換されたマークダウンをクリップボードにコピーします。

## 注意事項

- スクリプト自体のファイルは除外されます。
- テキスト形式のファイルのみが処理対象となります。
- ファイルの読み込みでエラーが発生した場合は、エラーメッセージがマークダウンに含まれます。

## 使用例

```command
python files_to_paste.py /path/to/your/code/ .py
```

上記のコマンドを実行すると、`/path/to/your/code/` ディレクトリ内の `.py` ファイルがマークダウン形式に変換され、クリップボードにコピーされます。後は好きな場所にペーストするだけで、ソースコードを共有することができます。

## 依存ライブラリ

- `pyperclip`: クリップボード操作用のライブラリ

## pyperclipのインストール方法

`pyperclip`は、pipを使用して簡単にインストールできます。以下の手順に従ってください。

1. ターミナル（またはコマンドプロンプト）を開きます。

2. 以下のコマンドを実行して、`pyperclip`をインストールします。

```command
pip install pyperclip
```

## 動作環境

- Python 3.x