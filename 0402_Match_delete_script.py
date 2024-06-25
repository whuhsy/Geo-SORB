import os

def get_base_filenames(directory, suffix_to_remove):
    """
    获取文件夹中的文件名，去掉指定的后缀后返回
    """
    filenames = os.listdir(directory)
    base_filenames = [filename.replace(suffix_to_remove, '') for filename in filenames]
    return set(base_filenames)

def filter_files(ast_dir, raw_dir, suffix_to_remove='_ast.txt'):
    """
    根据AST文件夹中的文件名过滤原始脚本文件夹中的文件
    """
    ast_filenames = get_base_filenames(ast_dir, suffix_to_remove)
    raw_filenames = os.listdir(raw_dir)

    for filename in raw_filenames:
        base_filename, _ = os.path.splitext(filename)
        if base_filename not in ast_filenames:
            os.remove(os.path.join(raw_dir, filename))
            print(f"Deleted: {filename}")
        else:
            print(f"Kept: {filename}")

# 示例文件夹路径
ast_directory = '05_AST_json'  # 替换为05_AST_json文件夹的实际路径
raw_directory = '03_Raw_script_filter'  # 替换为03_Raw_script_filter文件夹的实际路径

filter_files(ast_directory, raw_directory)
