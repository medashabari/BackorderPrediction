from flask import Flask, request, render_template, jsonify
from flask_cors import CORS,cross_origin

app = Flask(__name__)

@app.route("/home",methods = ['GET','POST'])
@cross_origin()
def home():
     render_template('home.html')

@app.route("/prediction_type",methods=['GET','POST'])
@cross_origin()
def prediction_type():
     ...
if __name__ == '__main__':
     app.run(debug=True)