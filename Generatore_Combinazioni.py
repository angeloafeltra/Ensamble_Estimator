import copy
import os
from os.path import exists
import pymongo
from Pipelines_Extractor import Pipelines_Extractor
import pandas as pd
import itertools
from Combinazione import Combinazione
from tqdm import tqdm
from Pipeline import Pipeline

class Generatore_Combinazioni:


    def __init__(self,experiments):
        self.list_experiments=experiments


    def getNextCombinazioniNonValutata(self):
        myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        mydb=myclient.get_database('Ensamble')
        collection=mydb.get_collection('Combinazioni')
        c=collection.find_one({'Valutata': False})
        if not c is None:
            combinazione=Combinazione()
            combinazione=combinazione.populateByDic(c)
            return combinazione
        else:
            return None



    def generaCombinazioni(self):
        myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        mydb=myclient.get_database('Ensamble')
        pipelinesForExperiments=[]
        collection=mydb.get_collection('Pipelines')
        for experiment in self.list_experiments:
            lista_id=collection.find({'Classificatore':experiment}).distinct('_id')
            pipelinesForExperiments.append(lista_id)


        print("Genero le Combinazioni")
        #Inizio la generazione delle combinazioni
        #Combinazioni1
        combinazioni=self.__combinazioni1(pipelinesForExperiments)
        #Combinazione 2
        combinazioni+=self.__combinazioni2(pipelinesForExperiments)
        #Combinazioni 3
        combinazioni+=self.__combinazioni3(pipelinesForExperiments)

        print("Salvo le combinazioni")
        #Salvo le combinazioni nel db
        if 'Combinazioni' in mydb.list_collection_names():
            mydb.drop_collection('Combinazioni')
        mydb.create_collection('Combinazioni')
        collection=mydb.get_collection('Combinazioni')


        for combinazione in combinazioni:
            pipeline_combinate=combinazione.getPipelineCombinate()
            document={}
            for pipeline,i in zip(pipeline_combinate,range(len(pipeline_combinate))):
                document['Pipeline {}'.format(i+1)]=pipeline
            document['Precision']=None
            document['Recall']=None
            document['F1']=None
            document['Valutata']=False
            collection.insert_one(document)


    def deleteSetCombinazioni(self):
        myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        mydb=myclient.get_database('Ensamble')
        if 'Combinazioni' in mydb.list_collection_names():
            mydb.drop_collection('Combinazioni')

    def getBestCombinazione(self,criterio):
        myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        mydb=myclient.get_database('Ensamble')
        collection=mydb.get_collection('Combinazioni')
        bests=collection.find().sort(criterio,-1).limit(1)
        return Combinazione().populateByDic(bests[0])


    def __combinazioni1(self,daCombinare):
        combinazioni=[]
        for element in itertools.product(*daCombinare):
            combinazione=Combinazione()
            combinazione.addPipeline2(element[0])
            combinazione.addPipeline2(element[1])
            combinazione.addPipeline2(element[2])
            combinazione.addPipeline2(element[3])
            combinazioni.append(combinazione)
        return combinazioni

    def __combinazioni2(self,daCombinare):
        combinazioni=[]
        for i in range(0,len(self.list_experiments)):
            copia=copy.copy(daCombinare)
            copia.pop(i)
            for element in itertools.product(*copia):
                combinazione=Combinazione()
                combinazione.addPipeline2(element[0])
                combinazione.addPipeline2(element[1])
                combinazione.addPipeline2(element[2])
                combinazioni.append(combinazione)

        return combinazioni

    def __combinazioni3(self,daCombinare):
        i=0
        combinazioni=[]
        while(i<len(self.list_experiments)-1):
            j=i+1
            while(j<len(self.list_experiments)):
                for element in itertools.product(*[daCombinare[i],daCombinare[j]]):
                    combinazione=Combinazione()
                    combinazione.addPipeline2(element[0])
                    combinazione.addPipeline2(element[1])
                    combinazioni.append(combinazione)
                j+=1
            i+=1
        return combinazioni