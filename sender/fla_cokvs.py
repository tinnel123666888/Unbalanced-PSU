from okvs import H3NaiveClusterBlazeGctGf2eDokvs
from flask import Flask, request, jsonify
from vodm_sender import Sender
import json
import time
import requests
from datetime import datetime
import csv
app = Flask(__name__)
fp_length = 8  # 指纹长度 fp
fi_length = 4  # 索引编码长度 fi
key = "secret_key"  # 用于 F_OPRF 的密钥
# 初始化参数
n, l = 6145, 2
okvs = H3NaiveClusterBlazeGctGf2eDokvs(n, l)
# 初始化 S 列表，用于存储解码结果
S = []
def decode_tx_elements(data):
    TX = []
    # 从 CSV 文件中读取数据
    with open('TX_output.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            # 如果单元格为空，将其转换为 None；否则，将其转换为整数
            value = None if row[0] == '' else int(row[0])
            TX.append(value)

    # 输出读取的 TX 列表
    #print("从 CSV 文件读取的 TX 列表:", TX)
    """
    对 TX 列表中的每个元素调用 okvs 的 decode 方法进行解码，并返回解码后的列表 S。

    参数:
    - okvs: 具有 decode 方法的对象，用于解码
    - TX: 要解码的元素列表，其中可能包含 None 值
    - data: decode 方法需要的 storage 参数

    返回:
    - S: 解码后的结果列表，与 TX 的结构相同，None 的位置保持不变
    """
    # 初始化解码后的结果列表 S
    # 对 TX 中的每个元素调用 decode 方法
    for i, value in enumerate(TX):
        if value is not None:
            # 调用 decode 方法，将解码的结果添加到 S 列表
            decoded_value = okvs.decode(data, value)
            S.append(decoded_value)
        else:
            # 如果 TX[i] 是 None，则在 S 中添加 None
            S.append(None)
    print(S)

    sender = Sender(S, fp_length, fi_length, key)
    cuckoo_filter = sender.encode()
    print("模拟的布谷鸟过滤器内容:", cuckoo_filter)

    # data = json.dumps(cuckoo_filter)
    # url = "http://172.24.122.105:8100/vodm"
    # headers = {
    #     "User-Agent": "123"
    # }
    # x = requests.post(url=url, data=data, headers=headers)
    # print(x.content)


@app.route('/cokvs', methods=['POST'])
def gs():
    data = request.get_data()
    decode_tx_elements(data)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)