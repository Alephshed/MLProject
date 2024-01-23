import logging
import os
from datetime import datetime 

#Creamos un logfile

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)
#Esto crea archivos que se llaman log y la fecha
os.makedirs(logs_path, exist_ok=True) 
#Parece que esta fila crea el directorio y el flag evita que de un error si ya existe

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    #name = nombre del logger, si no tiene es root
    #levelsname = nivel de severidad del error
    #message = el mensaje del log
    level= logging.INFO, #establece el nivel minimo de severidad del error
    #En este caso ignora debug y muestra el resto (WARNING,ERROR,CRITICAL)
    )

""" 
Testing/Debugging version

if __name__ == "__main__":
    logging.info("Logging has started")
"""
