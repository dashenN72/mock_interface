# -*- coding: utf-8 -*-
# @Time    : 2020/3/3 23:21
# @Author  : dashenN72
"""
自定义接口地址、请求参数和返回数据，可用于模拟接口文档中定义的接口数据
"""

from flask import abort, jsonify, Flask, request, Response
import ast
import db
import log
opt = db.OperationDbInterface()  # 实例化数据库
log = log.TestLog(logger='main').getlog()  # 实例化log

app = Flask(__name__)
# 增加配置，支持中文显示
app.config['JSON_AS_ASCII'] = False


@app.route('/<path:requirt>', methods=['GET', 'POST'])
def get_response_by_request(requirt):
    log.info("request params：%s" % requirt)
    if request.method == 'GET':
        param_request = request.full_path.split('?')[1]
    elif request.method == 'POST':
        # print(request.get_data(as_text=True))
        param_request = request.get_data(as_text=True).replace('"', "'")
    else:
        param_request = ''
    log.info("preprocess params：%s" % param_request)
    result = opt.select_one('SELECT param_response FROM relation WHERE url_interface="%s" AND param_request="%s" '
                            'AND status=1' % (str(requirt), str(param_request)))
    log.info("db result：%s" % result)
    if result['data'] and result['code'] == '0000':  # 从db中拿到数据
        return jsonify(ast.literal_eval(result['data']['param_response']))
    elif result['code'] != '0000':  # db查询数据失败
        return jsonify({'code': 9, 'message': 'unexpect error on get db data'})
    else:  # db中无数据
        return jsonify({'code': 0, 'message': 'db data is null'})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=6868,
        debug=True
        )
