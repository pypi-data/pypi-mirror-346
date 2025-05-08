# Personally tiny useful Python tips

[![License](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-stable-blue.svg)](https://domschl.github.io/ml-indie-tools/index.html)
[![PyPI version fury.io](https://badge.fury.io/py/ml-indie-tools.svg)](https://pypi.python.org/pypi/ml-indie-tools/)


## Version
0.0.1 - datetime object & string Integration management in Python

© 2024 GitHub : https://github.com/YongBeomKim



with open(file_path, 'r') as f:
    file_content = f.readlines()

new_file_content = []
for line in file_content:
    if line.startswith(f"{list_name} = "):
        # 해당 List 변수 line을 찾아서 내용 수정
        list_str = line.split("=")[1].strip()
        list_variable = ast.literal_eval(list_str)

        if isinstance(list_variable, list):
            modified_list = modification_function(list_variable)
            new_file_content.append(f"{list_name} = {str(modified_list)}\n")
        else:
            print(f"변수 '{list_name}'이(가) List 형태가 아닙니다.")
            return