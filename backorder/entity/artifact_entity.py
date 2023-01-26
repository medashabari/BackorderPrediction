from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DatavalidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformer_object_file_path:str
    transformed_train_path:str 
    transformed_test_path:str 
    categorical_encoder_object_file_path:str
    target_encoder_object_file_path:str
@dataclass
class ModelTrainerArtifact:
    model_file_path:str
    f1_train_score:float
    f1_test_score:float
class ModelEvaluationArtifact:...
class ModelPusherArtifact:...