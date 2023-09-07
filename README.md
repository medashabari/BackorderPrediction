# BACK ORDER PREDICTION

## Problem Statement
  - Backorders are unavoidable, but by anticipating which things will be backordered,planning can be streamlined at several levels, preventing unexpected strain on production, logistics, and transportation. 
  - ERP systems generate a lot of data (mainly structured) and also contain a lot of historical data; if this data can be properly utilized, a predictive model to forecast backorders and plan accordingly can be constructed.
  - Based on past data from inventories, supply chain, and sales, classify the products as going into backorder (Yes or No).
  - The Problem is to prevent the unexpected strain on production,logistcs and transportation.
  - From then problem statement we need reduce the both False Positve and False Negative.
  - False Negative reduction will help us to prevent the unexpected strain on production,logistics and transportation
  - False positive is not that much important to the company because even if it is predicted as product is going to be backordered but actually is not backorded.

## Project Architecture
![Project Architecture](https://github.com/medashabari/BackorderPrediction/blob/main/Documents/PROJECT%20ARCHITECUTRE%20MAIN%20(2).png?raw=true)

## Project PipeLine Stages
 In this project, I have developed a machine learning model that predicts the likelihood of back orders for products. The project pipeline is as follows:

### Data Ingestion: 
- The project begins with data ingestion from S3 buckets. The data is retrieved and preprocessed for further analysis.

### Data Validation:
- The data is carefully validated to ensure its integrity and consistency. This step involves checking for missing values, handling outliers, and verifying data types.

### Data Transformation: 
- To prepare the data for modeling, various transformation techniques are applied, such as feature scaling, one-hot encoding, or label encoding. This step ensures that the data is in a suitable format for model training.

### Model Training: 
- Machine learning algorithms are utilized to train a predictive model using the transformed data. Several models, such as Random Forest, Gradient Boosting, or Support Vector Machines, can be explored to identify the best-performing model.

### Model Evaluation:
- The trained model is evaluated using appropriate evaluation metrics like accuracy, precision, recall, or F1 score. This step helps assess the model's performance and identify areas for improvement.

### Model Pusher: 
- Once a satisfactory model is obtained, it is pushed to a production environment or deployed as an API to make predictions on new data.

### Frontend Website: 
- To provide a user-friendly interface for interaction, I have used Streamlit to create a frontend website. Users can input relevant information and receive predictions for back orders based on the trained model.
- **Deployed stremlit app link**
 - Click on link
 [Backorder prediction](https://medashabari-backorderprediction-main-43n2rq.streamlit.app/)
 

![Project PipeLine Stages](https://github.com/medashabari/BackorderPrediction/blob/main/Documents/Ml%20Design%20flow.png?raw=true)

### Usage
To run the project locally, follow these steps:

1. Clone the repository:
  ```
  git clone [https://github.com/your-username/backorder-prediction.git](https://github.com/medashabari/BackorderPrediction.git)
  ```
2. Install the required dependencies:
  ```
  pip install -r requirements.txt
  ```
3. Run the Streamlit application:
 ```
 streamlit run main.py
 ```
4. Access the application in your browser at `http://localhost:8501`.

## Contributing
- Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary modifications.
4. Commit your changes and push the branch.
5. Submit a pull request with a detailed description of your changes.
  

## Contact
If you have any questions or would like to collaborate on this project, please feel free to reach out to me. You can contact me via email at medashabari@gmail.com or connect with me on LinkedIn.

Let's make accurate backorder predictions together!

