from utils.logger import logging
from utils.custom_exception import CustomException
import sys

def d(a,b):
    try:
        logging.info("Division started")
        r = a/b
        return r
    except Exception as e:
        raise CustomException(e, sys)

if __name__=="__main__":
    d(10,0)