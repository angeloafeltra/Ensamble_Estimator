import os
from os.path import exists
import re
import mlflow
import pandas as pd
from PipelinesDAO import PipelinesDAO
from PipelineBean import PipelineBean


if __name__ == "__main__":

    experiments_name=['Decision Tree','Random Forest','KNN','AdaBoost']
    pipelinesDao=PipelinesDAO()
    for exp in experiments_name:
        experiment=mlflow.get_experiment_by_name(exp)
        all_run=mlflow.search_runs(experiment_ids=[experiment.experiment_id]) #Ottengo tutte le run dell'esperimento
        if not all_run.empty:
            if not pipelinesDao.collectionExsist():
                pipelinesDao.createCollection()

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
                pipeline=PipelineBean()
                pipeline.setClassificatore(exp)
                pipeline.setNome(run_name)
                pipeline.setPredictionSet(test_set_path)
                pipelinesDao.insertPipeline(pipeline)




