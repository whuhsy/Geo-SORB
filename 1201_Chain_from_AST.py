import os
import json
import csv
import re
from tqdm import tqdm

# 文件夹路径
folder_path = '05_AST_json'
# 输出CSV文件夹路径
output_folder_path = '13_Chain_from_AST'

def parse_ast(ast):
    if not ast:
        return None

    if ast['type'] == 'Program':
        return ' -> '.join(filter(None, (parse_ast(stmt) for stmt in ast.get('body', []))))
    elif ast['type'] == 'ExpressionStatement':
        return parse_ast(ast.get('expression'))
    elif ast['type'] == 'VariableDeclaration':
        declarations = [parse_ast(decl.get('init')) for decl in ast.get('declarations', []) if decl.get('init')]
        if len(declarations) > 1:
            return '{' + ' || '.join(filter(None, declarations)) + '}'
        return ' -> '.join(filter(None, declarations))
    elif ast['type'] == 'CallExpression':
        callee = parse_ast(ast.get('callee'))
        return callee if callee else None
    elif ast['type'] == 'MemberExpression':
        obj = parse_ast(ast.get('object'))
        prop = parse_ast(ast.get('property'))
        if obj and prop:
            return f"{obj}.{prop}"
        return None
    elif ast['type'] == 'Identifier':
        return ast.get('name')
    elif ast['type'] == 'IfStatement':
        test = parse_ast(ast.get('test'))
        consequent = parse_ast(ast.get('consequent'))
        alternate = parse_ast(ast.get('alternate')) if 'alternate' in ast and ast.get('alternate') else None
        if alternate:
            return f"if ({test}) {{ {consequent} }} else {{ {alternate} }}"
        return f"if ({test}) {{ {consequent} }}"
    elif ast['type'] == 'ForStatement':
        init = parse_ast(ast.get('init'))
        test = parse_ast(ast.get('test'))
        update = parse_ast(ast.get('update'))
        body = parse_ast(ast.get('body'))
        return f"for ({init}; {test}; {update}) {{ {body} }}"
    elif ast['type'] == 'WhileStatement':
        test = parse_ast(ast.get('test'))
        body = parse_ast(ast.get('body'))
        return f"while ({test}) {{ {body} }}"
    elif ast['type'] == 'FunctionDeclaration':
        name = parse_ast(ast.get('id'))
        body = parse_ast(ast.get('body'))
        if name:
            return name
        return body if body else None
    elif ast['type'] == 'BlockStatement':
        return ' -> '.join(filter(None, (parse_ast(stmt) for stmt in ast.get('body', []))))
    elif ast['type'] == 'ReturnStatement':
        argument = parse_ast(ast.get('argument'))
        return f"return {argument}"
    else:
        return None

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            ast = json.load(file)
            return parse_ast(ast)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def extract_script_name(filename):
    match = re.match(r'(\w+_\w+)_', filename)
    return match.group(1) if match else 'Unknown'


# 创建输出CSV文件夹
os.makedirs(output_folder_path, exist_ok=True)

# 初始化计数器
file_count = 0
csv_count = 1

# 准备写入CSV
output_csv_path = os.path.join(output_folder_path, f'chain_{csv_count}.csv')

# 记录处理的文件数量
total_files = len([filename for filename in os.listdir(folder_path) if filename.endswith('.txt')])

# 遍历文件夹中的所有txt文件，并显示进度条
with tqdm(total=total_files, desc='Processing Files', unit='file') as pbar:
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Script Name', 'Operator Chain'])

        # 遍历文件夹中的所有txt文件
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                operator_chain = process_file(file_path)
                if operator_chain:  # 仅在成功解析时写入CSV
                    script_name = extract_script_name(filename)
                    writer.writerow([script_name, operator_chain])
                    file_count += 1

                    # 更新进度条
                    pbar.update(1)

                    # 如果达到了10000个AST记录，创建新的CSV文件
                    if file_count % 10000 == 0:
                        csv_count += 1
                        output_csv_path = os.path.join(output_folder_path, f'chain_{csv_count}.csv')
                        file = open(output_csv_path, mode='w', newline='', encoding='utf-8')
                        writer = csv.writer(file)
                        writer.writerow(['Script Name', 'Operator Chain'])

print(f"Data has been successfully written to {output_folder_path}")
