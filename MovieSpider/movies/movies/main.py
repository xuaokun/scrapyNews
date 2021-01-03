from scrapy import cmdline
from multiprocessing import Process
from flask import Flask
from flask import jsonify
app = Flask(__name__)
# cmdline.execute(["scrapy","crawl","maoyan_movies"])
#cmdline.execute(["scrapy","crawl","mtime_movies"])
#cmdline.execute(["scrapy","crawl","txpc_movies"])
#cmdline.execute(["scrapy","crawl","daomeng_movies"])
# cmdline.execute(["scrapy","crawl","qqmusic_toplist"])
#cmdline.execute(["scrapy","crawl","qq_music"])
# cmdline.execute(["scrapy","crawl","sohu_home"])
# cmdline.execute(["scrapy","crawl","baidu_home"])
@app.route('/helloworld')
def hello_world():
    return 'Hello, World!'


@app.route('/sohunews')
def sohu_start():
    crawl_threads = Process(target=sohu_scrapy)
    crawl_threads.start()

    return jsonify({
        'msg': 'ok'
    })

def sohu_scrapy():
    cmdline.execute(["scrapy","crawl","sohu_home"])

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="0.0.0.0", port=5000, debug=True)