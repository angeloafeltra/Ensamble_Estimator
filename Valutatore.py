import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from CombinazioniDAO import CombinazioniDAO
from PipelinesDAO import PipelinesDAO
from CombinazioneBean import CombinazioneBean
from PipelineBean import PipelineBean
from scipy import stats as st

if __name__ == "__main__":
    combinazioneDao=CombinazioniDAO()
    pipelineDao=PipelinesDAO()
    combinazione=combinazioneDao.getCombinazioneDaValutare()
    while not combinazione is None:
        print(combinazione.getId())
        pipelines=[]
        for pipeline in combinazione.getPipelineCombinate():
            pipeline=pipelineDao.getPipelineByID(pipeline)
            pipelines.append(pipeline)

        #Ottengo le predizioni delle pipeline combinate
        dataframe_predic=pd.DataFrame()
        for pipeline in pipelines:
            predict=pipeline.getPredictionSetCSV()
            dataframe_predic[pipeline.getId()]=predict['isFlakyPredict']

        tureLable=pipeline.getPredictionSetCSV()['isFlaky']
        arr=dataframe_predic.to_numpy()
        dataframe_predic['moda']=st.mode(arr,axis=1).mode
        combinazione.setPrecision(precision_score(y_true=tureLable, y_pred=dataframe_predic['moda']))
        combinazione.setRecall(recall_score(y_true=tureLable, y_pred=dataframe_predic['moda']))
        combinazione.setF1(f1_score(y_true=tureLable, y_pred=dataframe_predic['moda']))
        combinazione.setValutata('true')
        combinazioneDao.updateCombinazione(combinazione)
        combinazione=combinazioneDao.getCombinazioneDaValutare()

