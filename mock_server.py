# -*- coding: utf-8 -*-
# @Time    : 2020/3/3 23:21
# @Author  : dashenN72
"""
自定义接口地址、请求参数和返回数据，可用于模拟接口文档中定义的接口数据
"""

from flask import abort, jsonify, Flask, request, Response
import json
import ast
import os
import log
log = log.TestLog(logger='main').getlog()  # 实例化log

app = Flask(__name__)
# 增加配置，支持中文显示
app.config['JSON_AS_ASCII'] = False

data_config = []


def get_data_from_json(*params):
    """
    处理读取的json文件中是否有匹配的请求数据
    :param params: 配置文件内容+url+请求参数
    :return: 响应数据
    """
    for data_json in params[0]:
        for data in data_json['data']:
            if params[1] in data['name_interface'] and data['status'] == 1:  # 接口地址匹配
                for req in data['request_response']:
                    if req['status'] == 1 and \
                            (ast.literal_eval(params[2]) == req['value_request'] or str(params[2]) == str(req['value_request'])):  # 请求参数匹配
                        return req['value_response']


@app.route('/<path:requirt>', methods=['GET', 'POST'])
def get_response_by_request(requirt):
    log.info("[INFO]Request Url：%s" % requirt)
    if request.method == 'GET':
        param_request = request.full_path.split('?')[1]
    elif request.method == 'POST':
        param_request = request.get_data(as_text=True).replace('"', "'")
    else:
        param_request = ''
    log.info("[INFO]Request Param：%s" % param_request)
    # 从json文件中读取数据
    for filename in os.listdir("./config"):
        with open("./config//" + filename, 'r', encoding='utf-8') as fp:
            try:
                data_config.append(json.load(fp))
                result = get_data_from_json(data_config, str(requirt), str(param_request))
            except json.decoder.JSONDecodeError:
                result = {'code': 9999, 'message': filename+'文件格式错误'}
                break
    log.info("[INFO]Response：%s" % result)
    if result:
        return jsonify(result)
    else:
        return jsonify({'code': 0, 'message': 'json文件中没有匹配的接口地址或请求参数'})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=6868,
        debug=True
        )
