from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from flask import Flask, render_template, g, request_started, request_finished
import time
import logging,sys
import logging.handlers


app = Flask(__name__)

logging.basicConfig(filename='app.log',level=logging.INFO,format='%(asctime)s %(name)s :%(message)s',datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()
handler = logging.StreamHandler()
myFormatter = logging.Formatter('%(asctime)s %(name)s :%(message)s')
handler.setFormatter(myFormatter)
logger.addHandler(handler)


@app.before_request
def start_request():
    g.start = time.time()


@app.after_request
def end_request(responce):
    endtime = time.time()
    g.exediff = endtime - g.start
    print("Execution delay: ", g.exediff)
    logger.info('Execution delay:\t%s',str(g.exediff))

    return responce

def requeststarted(sender, **extra):
    g.started = time.time()
    return "start"

request_started.connect(requeststarted,app)


def requestfinish(sender, response, **extra):
    endtime = time.time()
    g.totaldiff = endtime-g.started
    g.transitdiff = g.totaldiff-(endtime-g.start)
    print("Total Delay: ", g.totaldiff)

    logger.info('Total delay:\t%s',g.totaldiff)
    print("Network Transit Delay: ", g.transitdiff)

    logger.info('Network Transit delay:\t%s', g.transitdiff)

    return "finish"

request_finished.connect(requestfinish,app)

@app.route('/',methods=['GET'])
def run():
    return render_template('page.html')

@app.route('/log', methods=['POST'])
def log():
    '''
    def read():
        with open('app.log') as f:
            while True:
                yield f.read()
    return app.response_class(read(), mimetype='text/plain')
    '''
    file = open('app.log','r')
    file_content = file.read()
    #lines = file_content.split('\n')
    #context = {'file_content': lines}
    return app.response_class(file_content, mimetype='text/plain')
    #return render_template("log.html", file_content=file_content)

if __name__ == '__main__':
    app.run(debug=True)