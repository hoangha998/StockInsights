from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, Response
from code.TradingStyles.dash_app import get_dash_app
from code.NeuralNetwork.Predictor import TrendPredictor

app = Flask(__name__)

# initialize trend predictor 
trend_predictor = TrendPredictor()

# intialize dash app
dash_app = get_dash_app(app)

@app.route("/")
def index():
	return render_template('README.html')


@app.route("/trend_prediction", methods=['GET', 'POST'])
def trend_prediction():
	if request.method == 'POST':
		ticker = request.form.get('ticker')
		print("new ticker ({}) requested..".format(ticker))
		trend_predictor.set_ticker(ticker)
		decrease, increase, same = trend_predictor.predict()
		increase = '{:.2f}'.format(increase*100)
		decrease = '{:.2f}'.format(decrease*100)
		same = '{:.2f}'.format(same*100)
		result = {
			'ticker': ticker,
			'increase_confidence': increase,
			'decrease_confidence': decrease,
			'same_confidence': same
		}
		return render_template("trend_prediction.html", result = result) 
	
	return render_template("trend_prediction.html", result = False)

@app.route("/Andrew")
def andrew():
	variable = 100
	return render_template('andrew.html', number=variable)

@app.route("/Zach")
def zach():
	return render_template('zach.html')

@app.route("/keith")
def keith():
	#from code import TradingStyles

	return dash_app.index()
	

@app.route("/john")
def john():
	return render_template('john.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
