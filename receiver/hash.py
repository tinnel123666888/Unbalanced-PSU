from okvs import H3NaiveClusterBlazeGctGf2eDokvs
import hashlib
import csv
import random
import time
import threading
import sys
import requests
import json
class ReceiverHashTable:
    def __init__(self, Y, m, alpha):
        self.Y = Y  # 接收者的输入集合
        self.m = m  # 哈希表的大小
        self.alpha = alpha  # 独立哈希函数的数量
        self.TY = [None] * m  # 初始化一个有 m 个桶的空的哈希表 TY

    def hash_function(self, y, i):
        # 使用 hashlib 生成一致的哈希值
        hash_input = f"{y}-{i}".encode()
        return int(hashlib.md5(hash_input).hexdigest(), 16) % self.m

    def combine(self, y, j):
        # 使用整数拼接的方式表示 y || j
        return int(f"{y}{j}")

    def insert_to_table(self):
        # 对 Y 中的所有元素执行哈希插入
        for y in self.Y:
            for j in range(1, self.alpha + 1):
                h_j = self.hash_function(y, j)
                # 使用整数拼接来表示 y || j
                combined_value = self.combine(y, j)
                if self.TY[h_j] is None:
                    self.TY[h_j] = [combined_value]
                else:
                    self.TY[h_j].append(combined_value)  # 如果该桶已存在，则添加到列表中

    def execute(self):
        self.insert_to_table()
        return self.TY


# 示例用法
# 读取 CSV 文件中的数据并存储到 X 中
Y=[]
with open('receiver20.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        # 假设我们需要第一列的数据
        Y.append(int(row[0]))  # 根据需要将元素转换为整数，或改为适合的数据类型
m = 1301  # 哈希表的大小
alpha = 3  # 哈希函数的数量
# 初始化TY并生成m个随机值
R = [random.randint(0, 100) for _ in range(m)]
with open('R.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for value in R:
        writer.writerow([value])
print("R 列表已写入 R.csv 文件。")

receiver = ReceiverHashTable(Y, m, alpha)
TY = receiver.execute()
#显示接收者的哈希表 TY
# print(TY)
# print("接收者的哈希表 (TY):")
# for i, v in enumerate(TY):
#     print(f"桶 {i}: {v}")

#初始化空字典
key_value = {}
#遍历 R 和 TY，将它们组合成键值对
for i in range(len(R)):
    r_value = R[i]
    ty_item = TY[i]

    # 如果 TY 的元素是列表，遍历其中的每个值
    if isinstance(ty_item, list):
        for val in ty_item:
            key_value[str(val)] = r_value
    else:
        # 如果 TY 的元素是单个值
        key_value[str(ty_item)] = r_value

# 输出结果
#print("生成的键值对结构:", key_value)
#
#
# 初始化参数
n, l = 6145, 2
okvs = H3NaiveClusterBlazeGctGf2eDokvs(n, l)
start = time.perf_counter()  # 返回系统运行时间
# 调用 encode 方法
encoded_storage = okvs.encode(key_value)
end = time.perf_counter()
print('用时：{:.5f}s'.format(end - start))

# print("Encoded storage:", encoded_storage)
# data = json.dumps(encoded_storage)
# url = "http://172.24.122.105:8000/cokvs"
# headers = {
#             "User-Agent": "123"
# }
# x = requests.post(url=url, data=data, headers=headers)
# print(x.content)
