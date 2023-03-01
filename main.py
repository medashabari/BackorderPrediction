import streamlit as st 
from backorder.pipeline.batch_prediction import start_batch_prediction
from backorder.pipeline.instance_prediction import instance_prediction
import warnings
import os,sys
import pandas as pd
warnings.filterwarnings('ignore')
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


st.write("""
# Backorder Prediction""")

pred_type=st.sidebar.selectbox(
    "PREDICTION TYPE",
    ("Please select prediction type","InstancePrediction","BatchPrediction")
)

if pred_type=="InstancePrediction":
    d={}
    national_inv = st.number_input("Current inventory level for the product")
    d['national_inv'] = national_inv
    lead_time = st.number_input("Transit time for product",min_value=0)
    d['lead_time'] = lead_time
    transit_time = st.number_input("Amount of products in transit from source",min_value=0)
    d['in_transit_qty'] = transit_time
    forecast3 = st.number_input("Forecast sales for the next 3 months",min_value=0)
    d['forecast_3_month'] = forecast3
    forecast6 = st.number_input("Forecast sales for the next 6 months",min_value=0)
    d["forecast_6_month"] = forecast6
    forecast9 = st.number_input("Forecast sales for the next 9 months",min_value=0)
    d['forecast_9_month'] = forecast6
    sale1 = st.number_input("Sales quantity for the prior 1 month time period",min_value=0)
    d['sales_1_month'] = sale1
    sale3 = st.number_input("Sales quantity for the prior 3 month time period",min_value=0)
    d['sales_3_month'] = sale3
    sale6 = st.number_input("Sales quantity for the prior 6 month time period",min_value=0)
    d['sales_6_month'] = sale6
    sale9 = st.number_input("Sales quantity for the prior 9 month time period",min_value=0)
    d['sales_9_month'] = sale9
    min_bank = st.number_input("Minimum recommend amount to stock",min_value=0)
    d["min_bank"] = min_bank
    potential_issue = st.radio("Source issue for part identified (Potential damage)",("Yes","No"))
    d['potential_issue']= potential_issue
    pieces_past = st.number_input("Parts overdue from source (Products overdue from source)",min_value=0)
    d['pieces_past_due'] = pieces_past
    perf6 = st.number_input("Source performance for prior 6 month period",min_value=-99,max_value=1)
    d['perf_6_month_avg'] = perf6
    perf12 = st.number_input("Source performance for prior 12 month period",min_value=-99,max_value=1)
    d['perf_12_month_avg'] = perf12
    local_bo_quantity = st.number_input("Amount of stock orders overdue",min_value=0)
    d['local_bo_qty'] = local_bo_quantity
    deck_risk = st.radio("Part risk flag(The products that might remain in the deck/shop/stock)",("Yes","No"))
    d['deck_risk'] = deck_risk
    oe_constraint = st.radio("Part risk flag(Products that are facing operational limiting factors such as bottleneck)",("Yes","No"))
    d['oe_constraint'] = oe_constraint
    ppap_risk = st.radio("Part risk flag (Risks associated with packaging and production )",("Yes","No"))
    d['ppap_risk'] = ppap_risk
    stop_auto_buy = st.radio("Part risk flag(Whether automatic selling process has been stopped or not)",("Yes","No"))
    d['stop_auto_buy'] = stop_auto_buy
    rev_stop = st.radio("Part risk flag (Revenue status for product)",('Yes','No'))
    d['rev_stop'] = rev_stop

    if st.button("Submit",help='Please click submit it all values are entered'):
        pred = instance_prediction(d)
        if pred == 'No':
            st.write("""
            ## The product is not going to be backordered""")
        elif pred == 'Yes':
            st.write("""
            ## The product is going to be backorderd""")

if pred_type == 'BatchPrediction':
    st.write("""
    ## Batch Prediction Upload Dataset""")
    uploadedfile = st.file_uploader("Upload your data")
    if st.button("Submit"):
        if uploadedfile is not None:
            df = pd.read_csv(uploadedfile)
            df = start_batch_prediction(df=df)
            st.write(df)
            csv=convert_df(df)
            btn =st.download_button("Dowload Prediction file",data=csv,file_name='predictions.csv')
