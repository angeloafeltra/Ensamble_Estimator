import pymongo
from CombinazioneBean import CombinazioneBean

class CombinazioniDAO:

    def __init__(self):
        #myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        #self.mydb=myclient.get_database('Ensamble')
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        self.mydb=myclient.get_database('Ensamble')
        self.collectionName='Combinazioni'

    def getCombinazioneByID(self,id):
        collection=self.mydb.get_collection(self.collectionName)
        result=collection.find_one({'_id':id})
        combinazione=CombinazioneBean()
        combinazione=combinazione.populateByDic(result)
        return combinazione

    def insertCombinazione(self,combinazione):
        collection=self.mydb.get_collection(self.collectionName)
        dic=combinazione.toDic()
        collection.insert_one(dic)

    def updateCombinazione(self,combinazione):
        collection=self.mydb.get_collection(self.collectionName)
        collection.update_one({'_id':combinazione.getId()},{'$set':combinazione.toDic()})

    def createCollection(self):
        self.mydb.create_collection(self.collectionName)

    def dropCollection(self):
        self.mydb.drop_collection(self.collectionName)

    def collectionExsist(self):
        return self.collectionName in self.mydb.list_collection_names()

    def getCombinazioneDaValutare(self):
        collection=self.mydb.get_collection(self.collectionName)
        result=collection.find_one({'Valutata': 'false'})
        if not result is None:
            collection.update_one({'_id':result['_id']},{'$set':{'Valutata':'inValutazione'}})
            combinazione=CombinazioneBean()
            combinazione=combinazione.populateByDic(result)
            return combinazione
        else:
            return None

    def getCombinazioneInValutazione(self):
        collection=self.mydb.get_collection(self.collectionName)
        result=collection.find_one({'Valutata': 'inValutazione'})
        if not result is None:
            combinazione=CombinazioneBean()
            combinazione=combinazione.populateByDic(result)
            return combinazione
        else:
            return None


