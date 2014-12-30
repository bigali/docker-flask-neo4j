# -*- coding: utf-8 -*-

from flask import Flask
application = Flask(__name__)

@application.route('/', methods=['GET'])
def index():
    return 'Hello world!'

def test():
    application.run(debug=True)

if __name__ == '__main__':
    test()
