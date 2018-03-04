import logging
import json
import sys
# import crawler
# import predict
import flask
from flask import request, Response

application = flask.Flask(__name__)
logging.StreamHandler(sys.stdout)

@application.route('/run_crawler', methods=['POST'])
def run_crawler():
    # crawler.run()
    # predict.run()
    logging.info('test!')
    return Response("", status=200)


if __name__ == '__main__':
    application.run(host='0.0.0.0')