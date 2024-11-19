import random
import hashlib
# 示例 F_OPRF 函数，可以根据需求替换为实际的伪随机函数实现

def F_OPRF(key, x):
    hash_input = f"{key}:{x}".encode()
    return int(hashlib.sha256(hash_input).hexdigest(), 16)
# Receiver 实现
class Receiver:
    def __init__(self, input_vector, fp_length, fi_length, key, cuckoo_filter):
        self.input_vector = input_vector  # {r1, r2, ..., rm}
        self.fp_length = fp_length  # 指纹长度 fp
        self.fi_length = fi_length  # 索引编码长度 fi
        self.key = key  # 用于 F_OPRF 的密钥
        self.cuckoo_filter = cuckoo_filter  # 从 Sender 接收的布谷鸟过滤器
        self.f = fp_length + fi_length  # 总的指纹长度 f = fp + fi

    def decode(self):
        # 初始化位向量 B
        B = [0] * len(self.input_vector)

        # 调用 F_OPRF 生成 {q1', q2', ..., qm'}
        q_prime_vector = [F_OPRF(self.key, r) for r in self.input_vector]

        # 遍历每个输入元素，计算并查找 fingerprint
        for i, q_prime in enumerate(q_prime_vector):
            # 计算指纹部分 fp_i' 和索引编码 idx_i'
            fp_i_prime = q_prime % (2 ** self.fp_length)
            idx_i_prime = i % (2 ** self.fi_length)

            # 合并指纹和索引编码
            fingerprint_i_prime = (fp_i_prime << self.fi_length) | idx_i_prime

            # 在布谷鸟过滤器中查找 fingerprint_i_prime
            if fingerprint_i_prime in self.cuckoo_filter:
                B[i] = 1  # 如果找到，设置 B[i] 为 1
            else:
                B[i] = 0  # 如果未找到，设置 B[i] 为 0

        # 返回位向量 B
        return B

# 测试 Receiver 的示例用法
input_vector = [1, 4, 8, 6, 7]  # 示例输入向量 {r1, r2, ..., rm}
fp_length = 8  # 指纹长度 fp
fi_length = 4  # 索引编码长度 fi
key = "secret_key"  # 用于 F_OPRF 的密钥
cuckoo_filter=[1632, 2529, 770, 3267, 1332]
# 假设 cuckoo_filter 是从 Sender 那里获得的布谷鸟过滤器对象
# 在实际应用中，cuckoo_filter 需要通过通信从 Sender 获取
# 这里我们假设 sender 已经生成并发送了 CF（在之前的代码中创建的）

receiver = Receiver(input_vector, fp_length, fi_length, key, cuckoo_filter)
bit_vector = receiver.decode()

print("接收者的位向量 B:", bit_vector)
