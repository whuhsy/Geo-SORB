import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from tqdm import tqdm

# 读取CSV文件
data = pd.read_csv('11_Total_calls_counts.csv')

# 构建交易数据，这里我们假设每个“Caller”是一个交易，其“API”是购买的项目
transactions = data.groupby('Caller')['API'].apply(list).values.tolist()

# 使用TransactionEncoder转换数据
encoder = TransactionEncoder()
trans_encoded = encoder.fit_transform(transactions)
trans_df = pd.DataFrame(trans_encoded, columns=encoder.columns_)

# 使用Apriori算法找出频繁项集
with tqdm(total=3, desc="Processing") as pbar:
    pbar.set_postfix_str("Finding frequent itemsets...")
    frequent_itemsets = apriori(trans_df, min_support=0.05, use_colnames=True)
    pbar.update(1)

    # 挖掘关联规则
    pbar.set_postfix_str("Mining association rules...")
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
    pbar.update(1)

    # 输出频繁项集到CSV文件
    pbar.set_postfix_str("Saving frequent itemsets to CSV...")
    frequent_itemsets.to_csv('15_frequent_itemsets.csv', index=False)
    pbar.update(1)

# 输出关联规则到CSV文件
print("Saving association rules to CSV...")
rules.to_csv('15_association_rules.csv', index=False)

# 打印输出的文件路径确认
print("Frequent itemsets and association rules have been saved to 'frequent_itemsets.csv' and 'association_rules.csv'.")
