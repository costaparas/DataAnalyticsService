from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
	return render_template('template-results.html')


@app.route('/')
def index():
	return render_template('template.html')


if __name__ == '__main__':
	app.run(debug=True)