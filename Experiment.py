from flask import Flask, render_template, g, request_started, request_finished
import time

app = Flask(__name__)

@app.before_request
def start_request():
    g.start = time.time()

@app.after_request
def end_request(responce):
    g.endtime = time.time()
    g.exediff = g.endtime - g.start
    print("Execution delay: ", g.exediff)
    return responce

def requeststarted(sender, **extra):
    g.started = time.time()
    return "start"

request_started.connect(requeststarted,app)

def requestfinish(sender, response, **extra):
    endtime = time.time()
    g.totaldiff = endtime-g.started
    g.transitdiff = g.totaldiff-(g.endtime-g.start)
    print("Total Delay: ", g.totaldiff)
    print("Network Transit Delay: ", g.transitdiff)

    return "finish"

request_finished.connect(requestfinish,app)

@app.route('/')
def run():
    return render_template('page.html', totaldelay=str(g.totaldiff), executiontime=str(g.exediff), networkdelay=str(g.transitdiff))

if __name__ == '__main__':
    app.run(debug=True)