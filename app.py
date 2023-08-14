from flask import Flask, render_template, request
import tedori_calc

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gakumen = request.form['gakumen']
        gakumen_int = int(gakumen)
        kenkou_rate = request.form['kenkou_rate']
        kenkou_rate_int = float(kenkou_rate)
        kintouwari = request.form['kintouwari']
        kintouwari_int = int(kintouwari)
        return render_template("index.html", gakumen=gakumen, kenkou_rate=kenkou_rate, kintouwari=kintouwari) + tedori_calc.generate_tedori_result_str(gakumen_int, kenkou_rate_int, kintouwari_int)
    else: # GET
        return render_template("index.html")