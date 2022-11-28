import pymongo
class DatabaseManagement():

    def __init__(self,databaseName):
        myclient = pymongo.MongoClient("mongodb+srv://angeloafeltra:angelo99@cluster0.mkntsnm.mongodb.net/?retryWrites=true&w=majority")
        self.mydb=myclient.get_database(databaseName)


    def getCollection(self,collectionName):
        return self.mydb.get_collection(collectionName)

    def findOneDocument(self,collectionName,queryDic):
        collection=self.mydb.get_collection(collectionName)
        return collection.find_one(queryDic)

    def getListaCollezioni(self):
        return self.mydb.list_collection_names()

    def createCollezione(self,collectionName):
        self.mydb.create_collection(collectionName)

    def insertOneIntoCollection(self,collectionName,document):
        collection=self.getCollection(collectionName)
        collection.insert_one(document)

    def updateDocIntoCollection(self,collectionName,idDoc,dicUpdate):
        collection=self.getCollection(collectionName)
        collection.update_one({'_id':idDoc},{'$set':dicUpdate})

    def getListIdByClassifcatore(self,collection,nomeClassificatore):
        collection=self.getCollection(collection)
        return collection.find({'Classificatore':nomeClassificatore}).distinct('_id')

    def deleteCollection(self,collectionName):
        self.mydb.drop_collection(collectionName)

    def getDocumentsByMaxValue(self,collection,criterio):
        collection=self.getCollection(collection)
        bests=collection.find().sort(criterio,-1).limit(1)
        return bests