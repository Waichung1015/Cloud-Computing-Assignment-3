from flask import Flask, render_template, g
import time

app = Flask(__name__)

@app.before_request
def start_request():
    g.start = time.time()
    print("before request: ", g.start)

@app.after_request
def end_request(responce):
    endtime = time.time()
    time_diff = endtime - g.start
    print("after request", endtime)
    print("Web Service total delay: ", time_diff)
    return responce

@app.route('/')
def run():
    return render_template('page.html')

if __name__ == '__main__':
    app.run(debug=True)