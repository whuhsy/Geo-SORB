import os
import json
import esprima
from esprima.error_handler import ErrorHandler

def analyze_ast(file_path):
    # 读取文件内容（使用 UTF-8 编码）
    with open(file_path, 'r', encoding='utf-8') as file:
        script = file.read()
    
    # 使用 esprima 解析 JavaScript 代码并生成 AST
    try:
        ast = esprima.parseScript(script)
    except Exception as e:
        print(f"Error parsing script {file_path}: {e}")
        return None
    
    # 返回 AST
    return ast

def convert_ast_to_json_serializable(ast):
    # 将 AST 对象转换为 JSON 可序列化的格式
    if hasattr(ast, 'toDict'):
        return ast.toDict()
    elif isinstance(ast, list):
        return [convert_ast_to_json_serializable(node) for node in ast]
    elif isinstance(ast, dict):
        return {key: convert_ast_to_json_serializable(value) for key, value in ast.items()}
    elif isinstance(ast, esprima.nodes.Pattern):
        return None
    else:
        return ast

def save_ast_to_file(ast, output_file):
    # 将 AST 转换为 JSON 可序列化的格式
    ast_serializable = convert_ast_to_json_serializable(ast)
    
    # 将 AST 转换为 JSON 格式字符串
    ast_json = json.dumps(ast_serializable, default=str, indent=2)
    
    # 将 JSON 字符串写入到输出文件中
    with open(output_file, 'w') as file:
        file.write(ast_json)

def batch_analyze_ast(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的所有 txt 文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name.replace('.txt', '_ast.txt'))
            
            # 分析 AST
            ast = analyze_ast(input_file)
            
            # 将 AST 写入到输出文件中
            if ast:
                save_ast_to_file(ast, output_file)


# 设置输入文件夹和输出文件夹的路径
input_folder = '03_Raw_script_filter'  # 输入文件夹，包含所有 GEE 脚本的 txt 文件
output_folder = '05_AST_json'  # 输出文件夹，用于存储分析后的 AST 结果

# 批量分析 AST 并保存结果
batch_analyze_ast(input_folder, output_folder)