import copy
import itertools
from PipelinesDAO import PipelinesDAO
from CombinazioniDAO import CombinazioniDAO
from CombinazioneBean import CombinazioneBean
from tqdm import tqdm


def combinazioni1(daCombinare):
    combinazioni=[]
    for element in itertools.product(*daCombinare):
        combinazione = CombinazioneBean()
        combinazione.addPipeline(element[0])
        combinazione.addPipeline(element[1])
        combinazione.addPipeline(element[2])
        combinazione.addPipeline(element[3])
        combinazioni.append(combinazione)
    return combinazioni

def combinazioni2(daCombinare,numEsperimenti):
    combinazioni=[]
    for i in range(0,numEsperimenti):
        copia=copy.copy(daCombinare)
        copia.pop(i)
        for element in itertools.product(*copia):
            combinazione=CombinazioneBean()
            combinazione.addPipeline(element[0])
            combinazione.addPipeline(element[1])
            combinazione.addPipeline(element[2])
            combinazioni.append(combinazione)
    return combinazioni

def combinazioni3(daCombinare,numEsperimenti):
    i=0
    combinazioni=[]
    while(i<numEsperimenti-1):
        j=i+1
        while(j<numEsperimenti):
            for element in itertools.product(*[daCombinare[i],daCombinare[j]]):
                combinazione=CombinazioneBean()
                combinazione.addPipeline(element[0])
                combinazione.addPipeline(element[1])
                combinazioni.append(combinazione)
            j+=1
        i+=1
    return combinazioni


if __name__ == "__main__":

    experiments_name=['Decision Tree','Random Forest','KNN','AdaBoost']
    pipelinesDao=PipelinesDAO()
    combinazioniDao=CombinazioniDAO()

    pipelinesForExperiments=[]
    for experiment in experiments_name:
        lista_id=pipelinesDao.getDisinctPipIdByClassificatore(experiment)
        pipelinesForExperiments.append(lista_id)

    print("Genero le Combinazioni")
    combinazioni=[]
    #Combinazioni1
    combinazioni=combinazioni1(pipelinesForExperiments)
    #Combinazione 2
    combinazioni+=combinazioni2(pipelinesForExperiments,len(experiments_name))
    #Combinazioni 3
    combinazioni+=combinazioni3(pipelinesForExperiments,len(experiments_name))


    print("Salvo le combinazioni")
    if combinazioniDao.collectionExsist():
        combinazioniDao.dropCollection()
    combinazioniDao.createCollection()
    progressBar=tqdm(total=len(combinazioni))
    for combinazione in combinazioni:
        combinazioniDao.insertCombinazione(combinazione)
        progressBar.update(1)



