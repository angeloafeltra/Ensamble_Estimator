import os
from os.path import exists
import re
import mlflow
import pandas as pd
import pymongo

class Pipelines_Extractor:


    def getPipelines(self,experiments_name):
        #myclient=pymongo.MongoClient("mongodb://localhost:27017")
        #mydb=myclient.get_database('Ensamble')
        myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        mydb=myclient.get_database('Ensamble')
        for exp in experiments_name:
            experiment=mlflow.get_experiment_by_name(exp)
            all_run=mlflow.search_runs(experiment_ids=[experiment.experiment_id]) #Ottengo tutte le run dell'esperimento
            if not all_run.empty:
                if not 'Pipelines' in mydb.list_collection_names():
                    mydb.create_collection('Pipelines')
                collection=mydb.get_collection('Pipelines')
                for artifact_uri,model_history,run_name in zip(all_run['artifact_uri'],all_run['tags.mlflow.log-model.history'],all_run['tags.mlflow.runName']):
                    model_artifact=re.search('\"artifact_path\": \"([A-Za-z0-9]+)\"',model_history).group(1) #Ottengo il nome del modello usato nella run
                    test_set_path=artifact_uri+'/'+model_artifact+' Prediction'+'/'+model_artifact+'.csv' #Path in cui e salvato il test_set del run
                    current_dir=os.getcwd()
                    if not exists(current_dir+'/Test_sets/{}'.format(model_artifact)):
                        os.mkdir(current_dir+'/Test_sets/{}'.format(model_artifact))
                    #Salvo il dataset di validation in una nuova cartella.
                    dataset=pd.read_csv(test_set_path)
                    test_set_path='Test_sets/{}/{}.csv'.format(model_artifact,run_name)
                    dataset.to_csv(test_set_path)
                    document={'Classificatore':exp,'Nome':run_name,'Prediction_Set':test_set_path}
                    collection.insert_one(document)





