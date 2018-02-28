import logging
import json
# import crawler
# import predict
import flask
from flask import request, Response

application = flask.Flask(__name__)
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']


@application.route('/run_crawler', methods=['POST'])
def run_crawler():
    # crawler.run()
    # predict.run()
    logging.info('test!')
    return response = Response("succ!", status=478)


if __name__ == '__main__':
    application.run(host='0.0.0.0')