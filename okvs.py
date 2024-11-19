import hashlib
import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from collections import defaultdict
import hashlib
import random
from concurrent.futures import ThreadPoolExecutor

# BytesUtils类，用于执行字节数组的按位XOR操作
class BytesUtils:
    @staticmethod
    def inner_product(storage, byte_length, positions):
        result = bytearray(byte_length)
        for pos in positions:
            if storage[pos] != bytes(byte_length):
                result = bytes(a ^ b for a, b in zip(result, storage[pos]))
        return result


# MathPreconditions类，提供一些检查条件的方法
class MathPreconditions:
    @staticmethod
    def check_less_or_equal(name, value, threshold):
        # 删除阈值检查逻辑
        pass

    @staticmethod
    def check_equal(name1, name2, value1, value2):
        # 删除相等检查逻辑
        pass


# H3NaiveClusterBlazeGctGf2eDokvs类，用于实现基于三哈希的加密布谷鸟表
class H3NaiveClusterBlazeGctGf2eDokvs:
    def __init__(self, n, l, secure_random=None):
        self.n = n
        self.l = l
        self.secure_random = secure_random or random.SystemRandom()
        self.storage = [bytes(l)] * (n * 2)
        self.bin_num = 3
        self.binM = len(self.storage) // self.bin_num

    def positions(self, key):
        key_bytes = str(key).encode('utf-8')
        return [(int(hashlib.sha256(key_bytes + str(i).encode()).hexdigest(), 16) % self.binM + i * self.binM)
                for i in range(self.bin_num)]

    def _encode_bin(self, bin_key_value_map):
        for key, value in bin_key_value_map.items():
            value = value.to_bytes(self.l, byteorder='big') if isinstance(value, int) else value
            for pos in self.positions(key):
                if self.storage[pos] == bytes(self.l):
                    self.storage[pos] = value
                    break

    def encode(self, key_value_map):
        # 移除阈值检查
        key_value_maps = [defaultdict(lambda: None) for _ in range(self.bin_num)]

        for key, value in key_value_map.items():
            bin_index = int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % self.bin_num
            key_value_maps[bin_index][key] = value

        with ThreadPoolExecutor() as executor:
            executor.map(self._encode_bin, key_value_maps)
        return self.storage

    def decode(self, storage, key):
        # 移除相等检查
        positions = self.positions(key)
        decoded_value = BytesUtils.inner_product(storage, self.l, positions)

        # 尝试将解码后的字节数组转换为整数，如果失败则返回字节数组
        try:
            return int.from_bytes(decoded_value, byteorder='big')
        except ValueError:
            return decoded_value  # 如果不能转换成整数，则返回字节数组


# BytesUtils类，用于执行字节数组的按位XOR操作
class BytesUtils:
    @staticmethod
    def inner_product(storage, byte_length, positions):
        result = bytearray(byte_length)
        for pos in positions:
            if storage[pos] != bytes(byte_length):
                result = bytes(a ^ b for a, b in zip(result, storage[pos]))
        return result


# MathPreconditions类，提供一些检查条件的方法
class MathPreconditions:
    @staticmethod
    def check_less_or_equal(name, value, threshold):
        if value > threshold:
            raise ValueError(f"{name} ({value}) cannot be greater than {threshold}")

    @staticmethod
    def check_equal(name1, name2, value1, value2):
        if value1 != value2:
            raise ValueError(f"{name1} ({value1}) must equal {name2} ({value2})")

# 测试代码
# n, l = 1600, 16
#
#
#
# okvs = H3NaiveClusterBlazeGctGf2eDokvs( n, l)
#
# key_value_map = {
#     "apple": 1,
#     "carrot": 2,
#     "banana": 3,
#     "potato": 987654321,
#     "wuue":726,
# "wue":5,
# "ue":7,
# "e":6,
# "u":8,
# }
#
# encoded_storage = okvs.encode(key_value_map)
# print("Encoded storage:", encoded_storage)
#
# decoded_values = {key: okvs.decode(encoded_storage, key) for key in key_value_map}
# print("\nDecoded values:")
# for key, value in decoded_values.items():
#     print(f"{key}: {value}")
