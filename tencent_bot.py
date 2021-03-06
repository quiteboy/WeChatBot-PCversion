# -*- coding: utf-8 -*-
import hashlib
from urllib import parse
import time
import random
import string
import requests


URL = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
app_id = ''
app_key = ''


def md5_encode(text):
    """
    生成MD5
    :param text: 待处理字符串
    :return: 处理后的MD5字符串
    """
    if not isinstance(text, str):
        text = str(text)
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    encodedStr = md5.hexdigest().upper()
    return encodedStr


def get_response(text, userID):
    """
    智能闲聊（腾讯）<https://ai.qq.com/product/nlpchat.shtml>
    接口文档：<https://ai.qq.com/doc/nlpchat.shtml>
    :param text: 请求的话
    :param userID: 任意字符串，保证各会话独立
    :return: str
    """
    global app_id, app_key

    try:
        if not app_id or not app_key:
            print('app_id 或 app_key 为空，请求失败')
            return

        # 产生随机字符串
        nonce_str = ''.join(random.sample(
            string.ascii_letters + string.digits, random.randint(10, 16)))
        time_stamp = int(time.time())  # 时间戳
        params = {
            'app_id': app_id,  # 应用标识
            'time_stamp': time_stamp,  # 请求时间戳（秒级）
            'nonce_str': nonce_str,  # 随机字符串
            'session': md5_encode(userID),  # 会话标识
            'question': text  # 用户输入的聊天内容
        }
        # 签名信息
        params['sign'] = get_req_sign(params, app_key)
        resp = requests.get(URL, params=params)
        if resp.status_code == 200:
            # print(resp.text)
            content_dict = resp.json()
            # print(content_dict)
            if content_dict['ret'] == 0:
                data_dict = content_dict['data']
                return data_dict['answer']
            else:
                print('智能闲聊 获取数据失败:{}'.format(content_dict['msg']))
        return None
    except Exception as exception:
        print(str(exception))


def get_req_sign(parser, app_key):
    """
    获取请求签名，接口鉴权 https://ai.qq.com/doc/auth.shtml
    1.将 <key, value> 请求参数对按 key 进行字典升序排序，得到有序的参数对列表 N
    2.将列表 N 中的参数对按 URL 键值对的格式拼接成字符串，得到字符串 T（如：key1=value1&key2=value2），
        URL 键值拼接过程 value 部分需要 URL 编码，URL 编码算法用大写字母，例如 %E8，而不是小写 %e8
    3.将应用密钥以 app_key 为键名，组成 URL 键值拼接到字符串 T 末尾，得到字符串 S（如：key1=value1&key2=value2&app_key = 密钥)
    4.对字符串 S 进行 MD5 运算，将得到的 MD5 值所有字符转换成大写，得到接口请求签名
    :param parser: dect
    :param app_key: str
    :return: str,签名
    """
    params = sorted(parser.items())
    uri_str = parse.urlencode(params, encoding="UTF-8")
    sign_str = '{}&app_key={}'.format(uri_str, app_key)
    # print('sign =', sign_str.strip())
    hash_md5 = hashlib.md5(sign_str.encode("UTF-8"))
    return hash_md5.hexdigest().upper()


if __name__ == '__main__':
    to_text = '你刚刚不是说不爱我吗'
    userId = 'userId'
    form_text = get_response(to_text, userId)
    print(form_text)
    # print()