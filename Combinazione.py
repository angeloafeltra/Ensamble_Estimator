import copy

import pandas as pd
import pymongo
from scipy import stats as st
from sklearn.metrics import precision_score, recall_score, f1_score
from Pipeline import Pipeline
from DatabaseManagement import DatabaseManagement

class Combinazione:

    def __init__(self):
        self.id=None
        self.pipeline_combinate=[]
        self.precision=None
        self.recall=None
        self.f1=None
        self.valutata='false'
        self.db=DatabaseManagement('Ensamble')

    def getId(self): return self.id
    def getPrecision(self): return self.precision
    def getRecall(self): return self.recall
    def getF1(self): return self.f1
    def isValutata(self): return self.valutata
    def getPipelineCombinate(self): return self.pipeline_combinate


    def setId(self,id): self.id=id
    def setPrecision(self,precision): self.precision=precision
    def setRecall(self,recall): self.recall=recall
    def setF1(self,f1): self.f1=f1
    def setValutata(self,valutata): self.valutata=valutata

    def addPipeline(self,p):
        if type(p) is Pipeline:
            self.pipeline_combinate.append(p)
        else:
            pipeline=Pipeline(p)
            self.pipeline_combinate.append(pipeline)

    def addPipeline2(self,p):
        self.pipeline_combinate.append(p)


    def populateByDic(self,dic):
        self.id=dic['_id']
        numero_pipeline_combinate=len(dic)-5
        for i in range(numero_pipeline_combinate):
            self.addPipeline(dic['Pipeline {}'.format(i+1)])
        self.precision=dic['Precision']
        self.recall=dic['Recall']
        self.f1=dic['F1']
        self.valutata=dic['Valutata']
        return self


    def valuta(self):
        #Ottengo le predizioni delle pipeline combinate
        dataframe_predic=pd.DataFrame()
        for pipeline in self.pipeline_combinate:
            predict=pipeline.getPredictionSetCSV()
            dataframe_predic[pipeline.getId()]=predict['isFlakyPredict']

        #Ottengo le reali lable dei campioni
        tureLable=pipeline.getPredictionSetCSV()['isFlaky']

        #Clacolo la moda
        print("Calcolo la moda")
        arr=dataframe_predic.to_numpy()
        dataframe_predic['moda']=st.mode(arr,axis=1).mode
        print("Termine calcolo moda")

        #Aggiorno la combinazione
        self.precision=precision_score(y_true=tureLable, y_pred=dataframe_predic['moda'])
        self.recall=recall_score(y_true=tureLable, y_pred=dataframe_predic['moda'])
        self.f1=f1_score(y_true=tureLable, y_pred=dataframe_predic['moda'])
        self.valutata='true'

        print("Aggiorno la combinazione")
        #myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        #mydb=myclient.get_database('Ensamble')
        #collection=mydb.get_collection('Combinazioni')
        #collection.update_one({'_id':self.id},{'$set':{'Precision':self.precision,
                                               #'Recall':self.recall,
                                               #'F1':self.f1,
                                               #'Valutata':self.valutata}})

        self.db.updateDocIntoCollection('Combinazioni',self.id,{'Precision':self.precision,'Recall':self.recall,'F1':self.f1,'Valutata':self.valutata})



    def __str__(self):
       strPipeline=''
       for pipeline in self.getPipelineCombinate():
           strPipeline+=pipeline.__str__()+'\n'
       strPipeline=strPipeline[:-1]
       return 'ID:{},\nPipeline Combinate:\n{},\nPrecision:{},\nRecall:{},\nF1:{}'.format(self.getId(),
                                                                                              strPipeline,
                                                                                              self.getPrecision(),
                                                                                              self.getRecall(),
                                                                                             self.getF1())

