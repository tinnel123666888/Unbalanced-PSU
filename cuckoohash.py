import hashlib
import math
import csv
from okvs import H3NaiveClusterBlazeGctGf2eDokvs
class CuckooHashSender:
    def __init__(self, X, alpha, epsilon=0.27, max_attempts=100):
        self.X = X  # 发送方的输入集合
        self.n = len(X)  # 输入集合大小
        self.epsilon = epsilon  # 调整因子 ε
        self.m = math.ceil((1 + epsilon) * self.n)  # 计算桶数量
        self.alpha = alpha  # 独立哈希函数的数量
        self.max_attempts = max_attempts  # 最大尝试次数，防止无限循环
        self.TX = [None] * self.m  # 初始化一个有 m 个桶的空的布谷鸟哈希表

    def hash_function(self, x, i):
        hash_input = f"{x}-{i}".encode()
        return int(hashlib.md5(hash_input).hexdigest(), 16) % self.m

    def combine(self, x, i):
        # 使用字符串拼接 x 和 i，然后转换为整数
        return int(f"{x}{i}")

    def extract_original_element(self, combined_value, i):
        # 从组合的整数中提取原始的 x，假设组合方式是简单连接
        x_str = str(combined_value)[:-len(str(i))]  # 去掉末尾的 i 部分
        return int(x_str)  # 将字符串 x 转换回整数

    def insert_to_table(self, x):
        inserted = False
        attempt = 0
        while not inserted:
            if attempt >= self.max_attempts:
                print(f"插入失败：在插入元素 {x} 时超过最大尝试次数 {self.max_attempts}。")
                return False  # 插入失败，超过最大尝试次数

            j = (attempt % self.alpha) + 1  # 按固定顺序循环尝试哈希函数
            h_j = self.hash_function(x, j)
            if self.TX[h_j] is None:
                combined_value = self.combine(x, j)
                self.TX[h_j] = combined_value
                inserted = True
            else:
                x_prime = self.extract_original_element(self.TX[h_j], j)
                self.TX[h_j] = self.combine(x, j)
                x = x_prime
            attempt += 1
        return True  # 插入成功

    def execute(self):
        print(self.m)
        for x in self.X:
            if not self.insert_to_table(x):
                print("无法完成所有元素的插入。请考虑增加哈希表大小或调整参数。")
                break
        return self.TX

# 初始化 X 列表
X = []

# 读取 CSV 文件中的数据并存储到 X 中
with open('sender.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        # 假设我们需要第一列的数据
        X.append(int(row[0]))  # 根据需要将元素转换为整数，或改为适合的数据类型
# 示例用法
#X = [1, 2, 3, 4, 5]  # 发送方的输入集合
alpha = 3  # 哈希函数的数量
epsilon = 0.27  # ε参数

sender = CuckooHashSender(X, alpha, epsilon)
TX = sender.execute()

# 显示哈希表
print(TX)
# print("发送方的布谷鸟哈希表 (TX):")
# for i, v in enumerate(TX):
#     print(f"桶 {i}: {v}")
# 将 TX 列表写入 CSV 文件
with open('TX_output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for value in TX:
        writer.writerow([value])
print("TX 列表已写入 TX_output.csv 文件。")
# 初始化参数
n, l = 6145, 2
okvs = H3NaiveClusterBlazeGctGf2eDokvs(n, l)
# 初始化 S 列表，用于存储解码结果

S = []
storage=[]
# 对 TX 中的每个元素调用 decode 方法
for i, value in enumerate(TX):
    if value is not None:
        # 调用 decode 方法，将解码的结果添加到 S 列表
        decoded_value = okvs.decode(storage, value)
        S.append(decoded_value)
    else:
        # 如果 TX[i] 是 None，则在 S 中添加 None
        S.append(None)

# 输出 S 列表
print("解码后的 S 列表:", S)