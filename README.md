# Ensamble_Estimator
Ensamble Estimatore è un progetto che date una serie di run di ML registrate su mlflow, genera delle combinazioni di ensamble e valuta tali combinazioni.
Tuttavia risulta essere funzionante solamente se tali run hanno gli stessi campioni nel test_set.

## Run
1. Eseguire lo script Pipeline Extractor.py
2. Eseguire lo script Generatore Combinazioni.py
3. Valutatore.py

## Info
Pipeline Extractor e Generazione Combinazioni, vanno eseguiti sulla macchina in cui si trovano gli esperimenti di mlflow.
Essi estraggono le run da mlflow e generano delle combinazioni.
Valutatore pùo essere eseguito su qualsiasi macchina, ha il semplice compito di valutare le varie combinazioni
