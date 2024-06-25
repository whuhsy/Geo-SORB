import pandas as pd
import json

# 读取表格数据
df = pd.read_csv(r"11_Total_calls_counts.csv")  # 替换为你的表格文件名

# 将数据转换为JSON格式
nodes = set()
links = []

for index, row in df.iterrows():
    nodes.add(row['Caller'])
    nodes.add(row['API'])
    links.append({
        "source": row['Caller'],
        "target": row['API'],
        "type": row['Relationship'],
        "strength": row['Counts']
    })

# 构建 JSON
json_data = {"nodes": [{"id": node} for node in nodes], "links": links}

# 将 JSON 写入文件或打印输出
with open("17_Output_total.json", "w") as outfile:  # 替换为你想要输出的文件名
    json.dump(json_data, outfile, indent=2)

print("JSON 文件已生成。")
