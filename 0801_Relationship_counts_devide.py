import os
import csv
from collections import Counter
from tqdm import tqdm

def process_csv_files(input_folder):
    all_data = {'nested': Counter(), 'parallel': Counter(), 'sequential': Counter()}

    for filename in tqdm(os.listdir(input_folder), desc="Processing CSV files", unit="file"):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header row

                for row in csvreader:
                    relationship = row[2]  # Extract relationship
                    key = tuple(row[:3])  # Create a tuple as the key
                    all_data[relationship][key] += 1  # Count occurrences of each row

    return all_data

def write_to_csv(output_folder, filename, data):
    output_path = os.path.join(output_folder, filename)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Caller', 'API', 'Relationship', 'Counts'])  # Write header
        for key, count in data.items():
            csvwriter.writerow(key + (count,))  # Write each row with count

def main(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    all_data = process_csv_files(input_folder)

    for relationship, data in all_data.items():
        write_to_csv(output_folder, f'{relationship}_repeat.csv', data)


# 使用示例
input_folder = '07_API_relationship'  # 替换为实际输入文件夹路径
output_folder = '09_Relationship_devide'  # 替换为实际输出文件夹路径

main(input_folder, output_folder)
