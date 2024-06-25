import pandas as pd
import os

def process_csv(file_path, ref_df):
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 删除任何包含空数据的行
    df.dropna(inplace=True)

    # 处理第一列和第二列的数据
    for col in ['Caller', 'API']:
        df[col] = df[col].apply(lambda x: x if x.startswith('ee') else x.split('.')[-1])

    # 确保参考数据中包含的是唯一值
    ref_set = set(ref_df.iloc[:, 0].dropna().unique())

    # 过滤出第一列和第二列中数据存在于参考数据中的行
    df = df[df['Caller'].isin(ref_set) & df['API'].isin(ref_set)]

    # 删除重复的行，保留第一次出现的行
    df.drop_duplicates(inplace=True)

    return df

def process_folder(input_folder, output_folder, ref_csv_path):
    # 读取参考CSV
    ref_df = pd.read_csv(ref_csv_path)

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 处理每个CSV文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            processed_df = process_csv(file_path, ref_df)
            processed_df.to_csv(os.path.join(output_folder, filename), index=False)
            print(f'Processed {filename}')


# 使用示例
input_folder = '07_API_relationship'  # 输入文件夹路径
output_folder = '07_API_relationship'  # 输出文件夹路径
ref_csv_path = r'Reference_information\all_GEE_APIs_save_3.csv'  # 参考CSV文件路径

process_folder(input_folder, output_folder, ref_csv_path)
