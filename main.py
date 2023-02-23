from flask import Flask, request, render_template, jsonify
from flask_cors import CORS,cross_origin
from backorder.pipeline.batch_prediction import start_batch_prediction

app = Flask(__name__)

@app.route('/home',methods = ['GET','POST'])
@cross_origin()
def home():
     return render_template('home.html')

@app.route("/predictiontype",methods = ['POST','GET'])
@cross_origin()
def predictiontype():
     if request.method == 'POST':
          pred_type = request.form['prediction']
          if pred_type == 'batchprediction':
               return render_template('batchprediction.html')
          elif pred_type == 'instanceprediction':
               return render_template('instanceprediction.html')

@app.route("/batchprediction",methods = ['POST','GET'])
@cross_origin()
def batchprediction():
     flag=0
     if request.method == 'POST':
          url = request.form['url']
          df,file_path = start_batch_prediction(url=url)
          if 'cat_prediction' in df.columns:
               return f"<h1> First 5 Predictions </h1> <br> {df.head().to_html()}"
          



if __name__ == '__main__':
     app.run(debug=True,host="0.0.0.0",port=8000)