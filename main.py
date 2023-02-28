from flask import Flask, request, render_template, jsonify
from flask_cors import CORS,cross_origin
from backorder.exception import BackOrderException
from backorder.pipeline.batch_prediction import start_batch_prediction
from backorder.pipeline.instance_prediction import instance_prediction
import warnings
import os,sys
warnings.filterwarnings('ignore')

# Creating The Flask Object
app = Flask(__name__)

#Routing to Home Page
@app.route('/',methods = ['GET','POST'])
@cross_origin()
def home():
     return render_template('home.html')

#Routing to select prediction type
@app.route("/predictiontype",methods = ['POST','GET'])
@cross_origin()
def predictiontype():
     try:
          if request.method == 'POST':
               pred_type = request.form['prediction']
               if pred_type == 'batchprediction':
                    return render_template('batchprediction.html')
               elif pred_type == 'instanceprediction':
                    return render_template('instanceprediction.html')
     except Exception as e:
          raise BackOrderException(error=e, error_detail=sys)

#Routing to perform batchprediction
@app.route("/batchprediction",methods = ['POST','GET'])
@cross_origin()
def batchprediction():
     try:
          if request.method == 'POST':
               url = request.form['url']
               df,file_path = start_batch_prediction(url=url)
               if 'cat_prediction' in df.columns:
                    return f"<h1> First 100 Predictions </h1> <br> {df.head(100).to_html()}"
     except Exception as e:
          raise BackOrderException(error=e, error_detail=sys)

#Routing to perform instance prediction
@app.route("/instanceprediction",methods=['GET','POST'])
@cross_origin()
def instanceprediction():
     try:
          if request.method == 'POST':
               data_dict = request.form.to_dict()
               for key,value in data_dict.items():
                    if type(value)==str:
                         data_dict[key] = value.capitalize()
               pred = instance_prediction(data_dict)
               if pred == "No":
                    res = "The Product is not going be BackOrdered"
                    return render_template('instance_prediction_result.html', result=res)
               elif pred == 'Yes':
                    res = "The Product is going to be Backordered"
                    return render_template('instance_prediction_result.html', result=res)
     except Exception as e:
          raise BackOrderException(error=e, error_detail=sys)

          



if __name__ == '__main__':
     app.run(debug=True,host="0.0.0.0")
