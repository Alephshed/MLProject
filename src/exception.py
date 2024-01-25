import sys
#sys brinda acceso a argumentos de línea de comandos y funciones del sistema,
#como gestión de I/O (Input/Output) y variables de entorno.

import logging #Testeo del funcionamiento de logger y exception
import src.logger #Hay que importar esto para que funcione, logger =! logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info() #3 important info, descartamos los dos primeros de momento
    #exc_tb dará info del archivo o linea donde está el error
    file_name = exc_tb.tb_frame.f_code.co_filename 
    #esto es saberlo, de la custom excepcion handling
    error_message = "Error ocurred in python script name[{0}] line number [{1}], with error message[{2}]".format(
        file_name,exc_tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
    #Init te define las condicioens para instanciar la clase
        super().__init__(error_message)
        #No entiendo el porque de este super
        self.error_message= error_message_detail(error_message, error_detail = error_detail)
    
    def __str__(self):
        #El str es lo que se printeara cuando llamemos a la clase
        return self.error_message

"""
Testing/Debugging version 
if __name__ == "__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divided by 0 error")
        raise CustomException(e,sys) #NECESITA LOS PARÁMETROS
"""         