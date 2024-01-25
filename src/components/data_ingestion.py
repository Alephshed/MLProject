import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


#Los imputs que necesitamos se crean en esta clase, cosas como los paths, de entrada

#El decorador facilita la creación de la clase, creando el init de manera automática, por ejemplo.
#Esta sería la sintaxis sin el decorador:
"""
class DataIngestionConfig:
    def __init__(self, train_data_path):
        self.train_data_path = train_data_path

"""
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        #Si hubiera una base de datos de la que leer, ese código iría aquí (aunque podría ponerse en utils y ejecutarse aquí)
        logging.info("Entered te data ingestion method or component")
        try:
            df = pd.read_csv('notebook\data\stud.csv') #Esto está bien que sea un path relativo
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #Esto crea un directorio
            #Tengo dudas sobre como se encadenan los directorios

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Train test split initiated")

            train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data ingestion completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    #Esta estuctura se usa porque solo se ejecuta si el script se está ejecutando directamente, pero no si se llama desde otro script
    #vale para pruebas o demos bien
    obj=DataIngestion()
    obj.initiate_data_ingestion()