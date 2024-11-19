import hashlib
import random
import json
import requests
# 示例 F_OPRF 函数，可以根据需求替换为实际的伪随机函数实现

def F_OPRF(key, x):
    hash_input = f"{key}:{x}".encode()
    return int(hashlib.sha256(hash_input).hexdigest(), 16)
# 发送方实现
class Sender:
    def __init__(self, input_vector, fp_length, fi_length, key):
        self.input_vector = input_vector  # {s1, s2, ..., sm}
        self.fp_length = fp_length  # 指纹长度 fp
        self.fi_length = fi_length  # 索引编码长度 fi
        self.key = key  # 用于 F_OPRF 的密钥
        self.f = fp_length + fi_length  # 总的指纹长度 f = fp + fi
        self.cf = []  # 使用列表来模拟布谷鸟过滤器

    def encode(self):
        # 调用 F_OPRF 生成 {q1, q2, ..., qm}
        q_vector = [F_OPRF(self.key, s) for s in self.input_vector]

        # 遍历每个输入元素，计算并插入 fingerprint
        for i, q in enumerate(q_vector):
            # 计算指纹部分 fp_i 和索引编码 idx_i
            fp_i = q % (2 ** self.fp_length)
            idx_i = i % (2 ** self.fi_length)

            # 合并指纹和索引编码
            fingerprint_i = (fp_i << self.fi_length) | idx_i

            # 将 fingerprint_i 添加到模拟的布谷鸟过滤器列表中
            self.cf.append(fingerprint_i)

        # 返回布谷鸟过滤器供接收方使用
        return self.cf


# 测试 Sender 的示例用法
input_vector = [1, 2, 3, 6, 7]  # 示例输入向量 {s1, s2, ..., sm}
fp_length = 8  # 指纹长度 fp
fi_length = 4  # 索引编码长度 fi
key = "secret_key"  # 用于 F_OPRF 的密钥

sender = Sender(input_vector, fp_length, fi_length, key)
cuckoo_filter = sender.encode()

print("模拟的布谷鸟过滤器内容:", cuckoo_filter)

# data = json.dumps(cuckoo_filter)
# url = "http://172.24.122.105:8100/vodm"
# headers = {
#             "User-Agent": "123"
# }
# x = requests.post(url=url, data=data, headers=headers)
# print(x.content)

