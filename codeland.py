import os
import sys
import pyperclip
import mimetypes
from openai import OpenAI
from dotenv import load_dotenv
import json
import argparse

IGNORE_FILE = '.codeignore'
BASE_HEADER = "# Source Code\n"
ERROR_READING = "```\nファイル読み込みエラー\n```"

def load_codeignore(directory):
    codeignore_path = os.path.join(directory, IGNORE_FILE)
    if os.path.exists(codeignore_path):
        with open(codeignore_path, 'r') as f:
            result = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print("読み込まないファイル:",result)
            return result
    return []

def is_ignored(file_path, codeignore_list):
    file_path = os.path.abspath(file_path)
    for pattern in codeignore_list:
        abs_pattern = os.path.abspath(pattern)
        if os.path.isdir(abs_pattern) and file_path.startswith(abs_pattern + os.sep):
            return True
        elif os.path.isfile(abs_pattern) and file_path == abs_pattern:
            return True
    return False

def generate_markdown(directory, extension, codeignore_list=[]):
    output = []
    output.append(BASE_HEADER)
    base_path = os.path.abspath(directory)
    script_name = os.path.basename(__file__)
    
    if extension == 'all':
        extension = ''
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, base_path)
 
            if file.endswith(extension) and file != script_name and not is_ignored(relative_path, codeignore_list):
                output.append(f"## {relative_path}\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        output.append(f"```\n{content}\n```\n")
                except UnicodeDecodeError:
                    output.append(ERROR_READING)
    
    return "".join(output)


def generate_requirements_document(source_code, type):
    prompt = ""

    if type == "c":

        prompt += f'''
あなたは天才エンジニアです。以下の手順に従って、提供された[Source Code]からソースコード仕様書を作成してください。

# 手順
1. **ソースコードの確認**
   - 提供された[Source Code]を詳細に確認する。
2. **ソースコード仕様書の作成**
   - [Source Code]に基づいて、以下の[出力フォーマット]に従ってソースコード仕様書を作成する。
   - 出力はマークダウン形式で記述する。
3. **出力の長さ**
   - ソースコード仕様書の長さは、最小1000文字、最大3000文字とする。
   - 各ファイルの説明は、100〜200文字程度とする。

# ソースコード
{source_code}

# 出力フォーマット
## 1. ソースコードのフォルダ構成と内容
- [Source Code]の全ファイルをフォルダ構成に基づいて一つずつ記述する。
- 各ファイルの役割や関連性を簡潔に説明する。

## 2. ソースコードの内容と説明
- [Source Code]の全ファイルの処理内容を一つずつ記述する。
- 各ファイルの主要な関数、クラス、変数などを説明する。
- 処理の流れや目的を簡潔に説明する。

# サンプル出力
## 1. ソースコードのフォルダ構成と内容
- `main.py`: プロジェクトのエントリーポイントとなるメインファイル。
- `utils/`: ユーティリティ関数を含むフォルダ。
  - `file_handler.py`: ファイルの読み書きを担当する関数を含むファイル。
  - `data_processor.py`: データの前処理を行う関数を含むファイル。

## 2. ソースコードの内容と説明
### `main.py`
- `main()`関数: プログラムのエントリーポイント。コマンドライン引数を解析し、適切な関数を呼び出す。
- `process_data()`関数: データの読み込み、前処理、および結果の出力を行う。

### `utils/file_handler.py`
- `read_data_from_file()`関数: 指定されたファイルからデータを読み込む。
- `write_data_to_file()`関数: 指定されたファイルにデータを書き込む。

### `utils/data_processor.py`
- `preprocess_data()`関数: 入力データに対して前処理を行う。
- `normalize_data()`関数: データを正規化する。
        '''

    elif type == "d":
        prompt += f'''
あなたは天才エンジニアです。以下の手順に従って、提供された[Source Code]をデバッグし、デバッグドキュメントを作成してください。

# 手順
1. **ソースコードの確認**
   - 提供された[Source Code]を詳細に確認し、潜在的な問題点を特定する。
   - コードの理解に必要な情報を収集する。
2. **問題点の優先順位付け**
   - 特定した問題点を重要度に基づいて優先順位付けする。
   - 重大な問題から順に対処する。
3. **問題点の分析と修正方針の決定**
   - 各問題点について、原因を分析し、修正方針を決定する。
   - 修正方針は、コードの品質、可読性、効率性を考慮して選択する。
4. **コードの修正**
   - 決定した修正方針に基づいて、コードを修正する。
   - 修正後のコードが問題を適切に解決していることを確認する。
5. **デバッグドキュメントの作成**
   - 以下の[出力フォーマット]に従って、デバッグドキュメントを作成する。
   - 出力はマークダウン形式で記述する。
6. **出力の長さ**
   - デバッグドキュメントの長さは、最小1000文字、最大3000文字とする。
   - 各問題点の説明は、150〜300文字程度とする。

# ソースコード
{source_code}

# 出力フォーマット
## 1. デバッグ結果
- [Source Code]の全ファイルをデバッグした結果を一つずつ記述する。
- 各問題点について、以下の内容を含める:
  - 問題点の概要
  - 問題の原因
  - 修正方針
  - 修正後のコード
  - 修正の説明

# サンプル出力
## 1. デバッグ結果
### `main.py`
#### 問題点1
- 概要: ファイルのクローズ漏れがある。
- 原因: `open()`で開いたファイルオブジェクトが、`close()`されていない。
- 修正方針: `with`文を使用してファイルを開き、自動的にクローズする。

修正後のコード:
```python
with open("data.txt", "r") as file:
    data = file.read()

- 説明: with文を使用することで、ファイルを自動的にクローズできる。これにより、ファイルのクローズ漏れを防ぐことができる。
### utils/data_processor.py
#### 問題点2
概要: 変数名が不適切で、コードの可読性が低い。
原因: 変数名が省略されており、変数の意味が理解しづらい。
修正方針: 変数名を詳細で説明的な名前に変更する。

修正後のコード:
pythonCopy codedef preprocess_data(raw_data):
    cleaned_data = remove_noise(raw_data)
    normalized_data = normalize(cleaned_data)
    return normalized_data

説明: 変数名を dataから raw_data、cleaned_data、normalized_dataに変更することで、各変数の役割が明確になり、コードの可読性が向上する。
        '''
    else:
        # エラーを発生させる
        raise ValueError("不正なタイプが指定されました。")

    load_dotenv(".codeenv")
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    response = client.chat.completions.create(
        model=os.getenv('OPENAI_MODEL'),
        messages=[
            {"role": "system", "content": prompt},
        ],
        temperature=0,
    )

    requirements_document = response.choices[0].message.content

    return requirements_document

def main():

    parser = argparse.ArgumentParser(description='ソースコードをマークダウン形式に変換します。')

    parser.add_argument('directory', type=str, help='ディレクトリのパスです。')
    parser.add_argument('extension', type=str, help='ファイルの拡張子です。')
    parser.add_argument('-c', '--create-docs', action='store_true', help='設定されている場合、ソースコード仕様書が作成されます。')
    parser.add_argument('-p', '--paste', action='store_true', help='設定されている場合、ソースコードがクリップボードにコピーされます。')
    parser.add_argument('-d', '--debug', action='store_true', help='設定されている場合、デバッグ出力を行います。')

    args = parser.parse_args()
    
    directory_path = args.directory
    extension = args.extension
    
    markdown_output = generate_markdown(directory_path, extension, load_codeignore(directory_path))

    if args.paste:
        pyperclip.copy(markdown_output)
        print("マークダウン出力がクリップボードにコピーされました。好きなところでペーストしてください。")

    if args.create_docs:
        try:
            requirements_document = generate_requirements_document(markdown_output, "c")
            with open("codeland/requirements.md", "w") as f:
                f.write(requirements_document)
                print("\nソースコード仕様書の作成完了:\n")
        except Exception as e:
            print(f'ソースコード仕様書の作成中にエラーが発生: {e}')

    if args.debug:
        
        try:
            debug_document = generate_requirements_document(markdown_output, "d")
            os.makedirs("codeland", exist_ok=True)
            with open("codeland/debug.md", "w") as f:
                f.write(debug_document)
                print("\nデバッグドキュメントの作成完了:\n")
        except Exception as e:
            print(f'デバッグドキュメントの作成中にエラーが発生: {e}')


if __name__ == "__main__":
    main()