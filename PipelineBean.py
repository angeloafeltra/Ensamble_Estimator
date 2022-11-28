import pandas as pd

class PipelineBean:

    def __init__(self):
        self.id=None
        self.classificatore=None
        self.nome=None
        self.prediction_set=None


    def getId(self): return self.id
    def getClassificatore(self): return self.classificatore
    def getNome(self): return self.nome
    def getPredictionSet(self): return self.prediction_set
    def getPredictionSetCSV(self):
        dataframe=pd.read_csv(self.prediction_set)
        return dataframe


    def setId(self,id): self.id=id
    def setClassificatore(self,classificatore): self.classificatore=classificatore
    def setNome(self,nome): self.nome=nome
    def setPredictionSet(self,prediction_set): self.prediction_set=prediction_set

    def populateByDic(self,dic):
        self.id=dic['_id']
        self.classificatore=dic['Classificatore']
        self.nome=dic['Nome']
        self.prediction_set=dic['Prediction_Set']
        return self

    def toDic(self):
        dic={
            'Classificatore':self.classificatore,
            'Nome':self.nome,
            'Prediction_Set':self.prediction_set
        }
        return dic

    def __str__(self):
        return '[Id:{}, Nome:{}, Classificatore:{},Prediction{}]'.format(self.id,self.nome,self.classificatore,self.prediction_set)




