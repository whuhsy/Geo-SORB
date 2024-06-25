import os
import re

def is_comment(line):
    """
    判断是否是单行注释
    """
    return line.strip().startswith('//') or line.strip().startswith('#') or line.strip().startswith('/*') or line.strip().endswith('*/')

def is_multiline_comment_start(line):
    """
    判断是否是多行注释的开始
    """
    return line.strip().startswith('/*')

def is_multiline_comment_end(line):
    """
    判断是否是多行注释的结束
    """
    return line.strip().endswith('*/')

def is_code_comment(line):
    """
    判断注释行是否是代码行
    """
    return bool(re.search(r'[;,{}()]$', line.strip()))

def is_text_info(line):
    """
    判断注释行是否含有自然语言信息
    """
    if 'https://' in line:
        return True
    stripped_line = line.strip()
    return (stripped_line.startswith(' ') and 
            (stripped_line[1:].startswith(tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) or 'ing' in stripped_line))

def filter_comments(script_lines):
    """
    过滤注释行
    """
    filtered_lines = []
    in_multiline_comment = False
    for line in script_lines:
        if in_multiline_comment:
            if is_multiline_comment_end(line):
                in_multiline_comment = False
            if is_text_info(line) and not is_code_comment(line):
                filtered_lines.append(line)
        else:
            if is_multiline_comment_start(line):
                in_multiline_comment = True
                if is_text_info(line) and not is_code_comment(line):
                    filtered_lines.append(line)
            elif not is_comment(line):
                filtered_lines.append(line)
            else:
                if is_text_info(line) and not is_code_comment(line):
                    filtered_lines.append(line)
    return filtered_lines

def process_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    filtered_lines = filter_comments(lines)
    return filtered_lines

def get_script_size_in_kb(file_path):
    """
    计算脚本大小（以KB为单位）
    """
    return os.path.getsize(file_path) / 1024

def filter_scripts_by_size(script_paths, min_size=2, max_size=20):
    """
    过滤脚本路径，保留大小在2-20KB之间的脚本
    """
    return [script for script in script_paths if min_size <= get_script_size_in_kb(script) <= max_size]

def save_script(script_lines, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(script_lines)

def process_scripts_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    script_paths = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.txt')]
    filtered_script_paths = filter_scripts_by_size(script_paths)

    for script_path in filtered_script_paths:
        script_lines = process_script(script_path)
        output_path = os.path.join(output_folder, os.path.basename(script_path))
        save_script(script_lines, output_path)

# 使用示例
input_folder = '01_Input_raw_script/01_Input_raw_script'  # 替换为实际输入文件夹路径
output_folder = '03_Raw_script_filter'  # 替换为实际输出文件夹路径
process_scripts_in_folder(input_folder, output_folder)