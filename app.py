from flask import Flask, render_template, request
import tedori_calc

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gakumen = int(request.form['gakumen'])
        kenkou_rate = float(request.form['kenkou_rate_ippan']) + float(request.form['kenkou_rate_kaigo'])
        kintouwari = int(request.form['kintouwari'])
        return render_template("index.html", gakumen=gakumen, kenkou_rate=kenkou_rate, kintouwari=kintouwari) + tedori_calc.generate_tedori_result_str(gakumen, kenkou_rate, kintouwari)
    else: # GET
        return render_template("index.html")