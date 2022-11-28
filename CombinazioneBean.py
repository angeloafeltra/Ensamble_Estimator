import PipelineBean


class CombinazioneBean:


    def __init__(self):
        self.id=None
        self.pipeline_combinate=[]
        self.precision=None
        self.recall=None
        self.f1=None
        self.valutata='false'

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

    def toDic(self):
        dic={
            'Precision':self.precision,
            'Recall':self.recall,
            'F1':self.f1,
            'Valutata':self.valutata
        }
        num_pip_combinate=len(self.pipeline_combinate)
        for pipeline,i in zip(self.pipeline_combinate,range(num_pip_combinate)):
            if type(pipeline) is PipelineBean.PipelineBean:
                dic['Pipeline {}'.format(i+1)]=pipeline.getId()
            else:
                dic['Pipeline {}'.format(i+1)]=pipeline
        return dic

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

