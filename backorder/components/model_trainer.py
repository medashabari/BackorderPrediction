from backorder.exception import BackOrderException
from backorder.logger import logging
import os, sys 
from backorder.entity import config_entity,artifact_entity
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from backorder import utils

class ModelTrainer:
    """
    Description : Trains the Model.
    """
    def __init__(self,data_transformation_artifact:artifact_entity.DataTransformationArtifact,model_trainer_config: config_entity.ModelTrainerConfig):
        try:
            logging.info("=================================Model Trainer====================================")
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys) 

    def train_model(self,X,y):
        """
        Description : Fits the model with RandomForestClassifier
        Params :
            X : Input Feature
            y : Target Feature
        =====================================
        Return:
            RandomForestClassifier Model
        """
        random_forest_classifier = RandomForestClassifier()
        random_forest_classifier.fit(X,y)
        return random_forest_classifier

    def initiate_model_training(self)->artifact_entity.ModelTrainerArtifact:
        """
        Description : Initiates Model Training and generates Model Training Artifacts
        """
        try:
            train_array = utils.load_numpy_array(file_path=self.data_transformation_artifact.transformed_train_path)
            test_array = utils.load_numpy_array(file_path=self.data_transformation_artifact.transformed_test_path)
            
            logging.info(f"Splitting input and target feature from both train and test array.")
            X_train , y_train = train_array[:,:-1] , train_array[:,-1]
            X_test , y_test = test_array[:,:-1] , test_array[:,-1]

            logging.info("Training the model")
            model = self.train_model(X=X_train, y=y_train)

            logging.info("Training Predictions")
            yhat_train = model.predict(X_train)
            f1_train_score = f1_score(y_true=y_train, y_pred=yhat_train)
            logging.info(f"Training f1 score {f1_train_score}")

            logging.info("Testing the model")
            yhat_test = model.predict(X_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test)
            logging.info(f"Testing f1 score {f1_test_score}")

            # Checking for Expected test score
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not able to give the accuracy. Expected Accuracy {self.model_trainer_config.expected_score} \
                    Actual Test Accurary {f1_test_score}")

            diff = abs(f1_train_score-f1_test_score)

            if diff >self.model_trainer_config.over_fitting_threshold:
                raise Exception(f"Train and test score diff : {diff} is more than overfitting threshold {self.model_trainer_config.over_fitting_threshold}")

            logging.info('Saving model object')
            utils.save_object(file_path=self.model_trainer_config.model_object_path, obj=model)
            
            logging.info('Prepare model Trainer artifacts')
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_file_path=self.model_trainer_config.model_object_path,
                f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model Trainer Artifacts {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise BackOrderException(error=e, error_detail=sys)