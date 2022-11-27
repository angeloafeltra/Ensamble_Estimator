import warnings
from Combinazione import Combinazione
from Generatore_Combinazioni import Generatore_Combinazioni
from Pipeline import Pipeline
from Pipelines_Extractor import Pipelines_Extractor

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    experiments_name=['Decision Tree','Random Forest','KNN','AdaBoost']
    '''
    #Eseguire queste operazioni solamente sulla macchina dove sono stati effettuati gli esperimenti con mlflow
    extractor=Pipelines_Extractor()
    extractor.getPipelines(experiments_name)
    '''

    generatore=Generatore_Combinazioni(experiments_name)
    generatore.generaCombinazioni()



    combinazione=generatore.getNextCombinazioniNonValutata()
    while not combinazione is None:
        print(combinazione.getId())
        combinazione.valuta()
        combinazione=generatore.getNextCombinazioniNonValutata()



