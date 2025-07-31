# COMPOSER
Per ora il progetto è molto work in progress, più che altro
per sistemare ogni bug e rendere tutto più leggibile,
ma per ora:

## Files:
- ADAMusicGen2.py: contiene quello che è il cuore della trascrizione
da stringhe a midi e program synthesis, usando funzione importate da
- midigen_.py: che contiene le funzioni di base per trascrizione midi, e per arrangiare le progressioni
- models.py: contiene SCM() e DeepSCM() che sono i due modelli, entrambi costruiscono una matrice di correlazione
solo che il secondo può dare più o meno peso ad altre relazioni in base alla distanza: DeepSCM(1) equivale ad una SCM()
- P3RLA_BeatMaker.py: Raggruppa tutto ciò che il framework può fare generando nella cartella songs, una cartella contente 
tutti i file midi, pronti per sintetizzare un pezzo trap. Invito ad eseguire questo file
- 
## Directories:
- datas contiene ogni file con cui vengono addestrati i singoli modelli
- Examples contiene qualche esempio di utilizzo del framework, ogni file se eseguito traina un modello e fa inferenza su 
dei dati. 
- songs contiene le cartelle delle canzoni generate da P3RLA_BeatMaker.py