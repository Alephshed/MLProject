#Aquí entrenaremos diferentes modelos y compararemos los renidimentos
import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path= os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig()
    
    #Contexto
    #u = data_transformation.initiate_data_transformation(train_data,test_data)
    #u[0].shape = (800, 20)
    #u[1].shape = (200, 20)
    #u[2] = 'artifacts\\preprocessor.pkl'
    #Como nota, los paths están pensados para que se ejecute desde la carpeta de ML project por lo que si lo ejecutas desde
    #otra, se desbaratan los paths, tanto relativos de carga como de creación de carpetas.
    def initiate_model_trainer(self,train_array,test_array,preprocessor_path=None):
        try:
            logging.info("Split train and test input data")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1], #take out the last column
                train_array[:,-1], #all the columns or rows?
                test_array[:,:-1],
                test_array[:,-1] 
            )
            #No tienen parámeter tunning
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Classifier": KNeighborsRegressor(), #No me gusta que se llamen classifier
                "XGBClassifier": XGBRegressor(),
                "CatBoosting Classifier": CatBoostRegressor(verbose=False),
                "AdaBoost Classifier": AdaBoostRegressor(),
            }
            #Esta función se crea en el utils
            model_report:dict=evaluate_models(X_train=X_train, y_train=y_train, X_test= X_test, y_test=y_test,
                                              models=models)
        
            #Get best model score
            best_model_score = max(sorted(model_report.values())) #El sorted de momento es redundante

            best_mdoel_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_mdoel_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found") #Este threshold es pobre
            logging.info(f"Best found model on both training and testin dataset")

            #Se queda a medias usar esto -->preprocessing_obj =  
            save_object(
                file_path= self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test,predicted)
            return r2_square
        
        except Exception as e:
            raise CustomException(e,sys)