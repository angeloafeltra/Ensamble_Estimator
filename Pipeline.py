import os
import pandas as pd
import pymongo
from DatabaseManagement import DatabaseManagement

class Pipeline:


    def __init__(self,id):
        self.id=id
        self.db=DatabaseManagement('Ensamble')
        #myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        #mydb=myclient.get_database('Ensamble')
        #collection=mydb.get_collection('Pipelines')
        #result=collection.find_one({'_id':id})
        result=self.db.findOneDocument('Pipelines',{'_id':id})
        self.classificatore=result['Classificatore']
        self.nome=result['Nome']
        self.prediction_set=result['Prediction_Set']



    def getId(self): return self.id
    def getClassificatore(self): return self.classificatore
    def getNome(self): return self.nome
    def getPredictionSet(self): return self.prediction_set
    def getPredictionSetCSV(self):
        dataframe=pd.read_csv(self.prediction_set)
        return dataframe

    def __str__(self):
        return '[Id:{}, Nome:{}, Classificatore:{},Prediction{}]'.format(self.id,self.nome,self.classificatore,self.prediction_set)