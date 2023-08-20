from flask import Flask, render_template, request
import tedori_calc
from distutils.util import strtobool

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gakumen = int(request.form['gakumen'])
        kenkou_rate = float(request.form['kenkou_rate_ippan']) + float(request.form['kenkou_rate_kaigo'])
        kintouwari = int(request.form['kintouwari'])
        has_haigusha = int(strtobool(request.form['haigusha']))
        gakumen_haigusha = 0
        if has_haigusha:
            gakumen_haigusha = int(request.form['haigusha_gakumen'])
        return render_template("index.html", form_dict=request.form) + tedori_calc.generate_tedori_result_str(gakumen, kenkou_rate, kintouwari, bool(has_haigusha), gakumen_haigusha)
    else: # GET
        return render_template("index.html")