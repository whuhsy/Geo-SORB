import os
import pandas as pd

# 1. 遍历一个文件夹里的所有csv，读取并合并为一张总csv，列名不变
def merge_csv(folder_path):
    # 初始化一个空的DataFrame用于存储所有CSV文件的内容
    merged_df = pd.DataFrame()
    
    # 遍历文件夹中的所有CSV文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # 读取CSV文件并将其添加到总DataFrame中
            df = pd.read_csv(file_path)
            merged_df = pd.concat([merged_df, df])
    
    # 2. 将新的csv的Relationship列除列名外所有的值换成Total
    merged_df['Relationship'] = 'Total'
    
    return merged_df

# 3. 检查新的csv如果有Caller列和API列重复则合并为一条记录，并把Counts列数值相加
def merge_duplicates(df):
    # 合并重复记录并将Counts相加
    df = df.groupby(['Caller', 'API', 'Relationship']).agg({'Counts': 'sum'}).reset_index()
    return df


# 定义文件夹路径
folder_path = '09_Relationship_devide'

# 合并CSV文件
merged_df = merge_csv(folder_path)

# 合并重复记录
final_df = merge_duplicates(merged_df)

# 更新新的CSV文件
final_df.to_csv('11_Total_calls_counts.csv', index=False)
