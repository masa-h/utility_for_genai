import os
import sys
import pyperclip
import mimetypes

def generate_markdown(directory, extension):
    output = "# Source Code\n"
    base_path = os.path.abspath(directory)
    script_name = os.path.basename(__file__)
    
    if extension == 'all':
        extension = ''
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension) and file != script_name:
                file_path = os.path.join(root, file)
                mime_type, _ = mimetypes.guess_type(file_path)
                
                if mime_type and mime_type.startswith('text'):
                    relative_path = os.path.relpath(file_path, base_path)
                    output += f"## {relative_path}\n"
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            output += f"```\n{content}\n```\n\n"
                    except UnicodeDecodeError:
                        output += "```\nファイル読み込みエラー\n```\n\n"
    
    return output

def main():
    if len(sys.argv) != 3:
        print("使い方: python files_to_paste.py <ディレクトリ> <拡張子>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    extension = sys.argv[2]
    
    markdown_output = generate_markdown(directory_path, extension)
    pyperclip.copy(markdown_output)
    print("マークダウン出力がクリップボードにコピーされました。好きなところでペーストしてください。")

if __name__ == "__main__":
    main()