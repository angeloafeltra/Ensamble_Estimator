import pymongo
from PipelineBean import PipelineBean

class PipelinesDAO:

    def __init__(self):
        #myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        #self.mydb=myclient.get_database('Ensamble')
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        self.mydb=myclient.get_database('Ensamble')
        self.collectionName='Pipelines'

    def getPipelineByID(self,id):
        collection=self.mydb.get_collection(self.collectionName)
        result=collection.find_one({'_id':id})
        pipeline=PipelineBean()
        pipeline=pipeline.populateByDic(result)
        return pipeline

    def insertPipeline(self,pipeline):
        collection=self.mydb.get_collection(self.collectionName)
        dic=pipeline.toDic()
        collection.insert_one(dic)

    def updatePipeline(self,pipeline):
        collection=self.mydb.get_collection(self.collectionName)
        collection.update_one({'_id':pipeline.getId()},{'$set':pipeline.toDic()})

    def createCollection(self):
        self.mydb.create_collection(self.collectionName)

    def dropCollection(self):
        self.mydb.drop_collection(self.collectionName)

    def getDisinctPipIdByClassificatore(self,classificatore):
        collection=self.mydb.get_collection(self.collectionName)
        return collection.find({'Classificatore':classificatore}).distinct('_id')

    def collectionExsist(self):
        return self.collectionName in self.mydb.list_collection_names()

