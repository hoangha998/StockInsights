from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, Response

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/test")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/Andrew")
def andrew():
	variable = 100
    graphJSON=positiveNegativeCallBackTest()
	return render_template('andrew.html', number=variable)

@app.route("/Zach")
def zach():
	return render_template('zach.html')

@app.route("/Keith")
def keith():
	return render_template('keith.html')

@app.route("/John")
def john():
	return render_template('john.html')
    
@app.route("/Hoang")
def hoang():
	return render_template('hoang.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
