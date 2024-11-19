import random
import hashlib
from okvs import H3NaiveClusterBlazeGctGf2eDokvs
from flask import Flask, request, jsonify
from vodm_receiver import Receiver
import json
import time
import requests
from datetime import datetime
import csv
app = Flask(__name__)
# 初始化 S 列表，用于存储解码结果
fp_length = 8  # 指纹长度 fp
fi_length = 4  # 索引编码长度 fi
key = "secret_key"  # 用于 F_OPRF 的密钥
def cuckoofilter(cuckoo_filter):
    # 假设 cuckoo_filter 是从 Sender 那里获得的布谷鸟过滤器对象
    # 在实际应用中，cuckoo_filter 需要通过通信从 Sender 获取
    # 这里我们假设 sender 已经生成并发送了 CF（在之前的代码中创建的）
    R=[]
    with open('R.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            # 如果单元格为空，将其转换为 None；否则，将其转换为整数
            value = None if row[0] == '' else int(row[0])
            R.append(value)
    print(R)
    receiver = Receiver(R, fp_length, fi_length, key, cuckoo_filter)
    bit_vector = receiver.decode()
    print("接收者的位向量 B:", bit_vector)

@app.route('/vodm', methods=['POST'])
def vodm():
    cuckoo_filter = request.get_data()
    cuckoofilter(cuckoo_filter)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8100)

