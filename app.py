from flask import Flask
import tedori_calc

app = Flask(__name__)

@app.route("/")
def hello_world():
    kousei = tedori_calc.calc_kouseinenkin(1000000)
    return "<p>Hello, World!{}</p>".format(kousei)