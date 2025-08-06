from utils.logger import logging
from utils.custom_exception import CustomException
from src.data_converter import DataConverter
from src.config import Config
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb import AstraDBVectorStore
import sys

class DataIngest():
    def __init__(self):
        try:
            self.embedding = HuggingFaceEmbeddings(
                model=Config.EMBEDDING_MODEL,
                )

            self.vstore = AstraDBVectorStore(
                embedding=self.embedding,
                collection_name="flipkart_db",
                api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
                token=Config.ASTRA_DB_APPLICATION_TOKEN,
                namespace=Config.ASTRA_DB_KEYSPACE
            )
        except Exception as e:
             raise CustomException(e,sys)

    def ingest(self, load_existing=True):
        if load_existing==True:
                logging.info("Vector store already exists and loading from it")
                return self.vstore
        try:    
            logging.info("Vstore is getting initialized")

            docs = DataConverter("data/flipkart_product_review.csv").convert()
            self.vstore.add_documents(docs)
            logging.info("Vstore loaded with the data")

            return self.vstore

        except Exception as e:
            CustomException(e, sys)



