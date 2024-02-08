import sys
import os
from dataclasses import dataclass

import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer #Facilito, probablemente no sea lo mejor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException #Handle Exceptions
from src.logger import logging
from src.utils import save_object

@dataclass
#Esto se usa principalmente en las clases cuyo uso es guardar datos
class DataTansformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl') #No veo claro la necesidad de hacer un pkl de esto, pero weno

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTansformationConfig()
    
    def get_data_transformer_object(self):
        #Es la que define el objeto que vamos a guardar en el pickle
        #Esta función es responsable de las tranformaciones
        try:
            numerical_columns = ['writing_score','reading_score']
            categorical_columns = ['gender', 
                                   'race_ethnicity', 
                                   'parental_level_of_education', 
                                   'lunch', 
                                   'test_preparation_course']
            #No me acaba de gustar como está hecho, yo usaría esto:
            # categorical_features = [feature for feature in df.columns if df[feature].dtype == 'O']

            #primero crearemos una pipeline, teniendo en cuenta los missing values

            num_pipeline =Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")), #usamos la median por los outliers
                    ("scaler", StandardScaler(with_mean=False)) #!! (with_mean=False)
                ]
            )
            logging.info("Numerical columns standard scaling completed")

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)) #parece redundante con el onehot
                ]

            )
            #Recordemos que la idea es usarlos en train y en test

            logging.info("Categorical columns encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            #Es este preprocessor lo que se va como un pickle
            return preprocessor 
        

        except Exception as e:
            raise CustomException(e,sys) #No tengo del todo claro esto
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")


            logging.info("Obtainig preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score" #No me convence esta forma, es poco general
            numerical_columns = ['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns = [target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns = [target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Apply preprocessing object on train and test df"
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) #pone train

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")
            
            #Esta función se escribe en utils
            save_object( 
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )



        except Exception as e:
            raise CustomException(e,sys)
