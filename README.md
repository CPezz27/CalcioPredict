<h1>Obiettivo del progetto</h1>
Il progetto nasce con l'obiettivo di creare un programma che permette all'utente di predire il risultato di un match calcistico. 
Abbiamo creato una piccola piattaforma attraverso la quale l'utente può specificare le squadre che disputeranno il match tramite una semplice interfaccia grafica. 
Selezioniamo dunque le squadre, prestando attenzione a quella che disputerà il match in casa e a quella che lo disputerà in trasferta, così da ottenere un risultato 
più accurato (dato che il fattore casa è un elemento importante per la predizione del risultato della partita, come specificheremo successivamente.

<h1>Come replicare fedelmente</h1>
La soluzione adottata ci permette di utilizzare la classificazione per trovarei risultati più probabili per la partita che si deve considerare. 
Nello specifico, utilizziamo tre classificatori: <br>
• RandomForestClassifier <br>
• LogisticRegression <br>
• SVC <br>

La soluzione adottata consiste nel caricamento di uno dei dataset messi a disposizione che vengono selezionati specificando la lega che si vuole prendere in 
considerazione e la stagione calcistica (evidenziando le ultime due cifre dell’anno in cui si disputa la stagione, es. stagione calcistica 2023/2024 sarà 2324).
A questo punto viene verificata l’esistenza del file e, una volta appurato che sia aggiornato alla data odierna, vengono selezionate alcune colonne dei dati nel dataset; 
in particolare: <br>
• Date <br> 
• HomeTeam <br>
• AwayTeam <br>
• FTHG <br>
• FTAG <br>
• FTR <br>
• HTHG <br>
• HTAG <br>
• HTR <br>
• HS <br>
• AS <br>
• HST <br>
• AST <br>
• HF <br>
• AF <br>
• HC <br>
• AC <br>
• HY <br>
• AY <br>
• HR <br>
• AR <br>
Le colonne selezionate ci permettono di prendere in considerazione solo i dati che ci interessano per la risouzione del problema. 
Estraiamo dunque l’elenco delle squadre che hanno almeno un match disputato (che sia in casa o fuori) e lo salviamo in un array con valori unici, 
così da evitare che una squadra si trovi con più record.
Per ogni squadra nell’array calcoliamo quindi una serie di statistiche; in particolare registriamo i punti totalizzati e calcoliamo le seguenti statistiche sia
per le partite giocate in casa che per quelle giocate in trasferta:  <br>
• Match giocati <br>
• Vittorie <br>
• Pareggi <br>
• Sconfitte <br>
• Goal segnati <br>
• Goal concessi <br>
• Tiri totali <br>
• Tiri in porta <br>
• Falli commessi <br>
• Angoli totali <br>
• Cartellini gialli <br>
• Cartellini rossi <br>
• Media goal <br>
Aggiungiamo dunque la squadra alla lista che ci permetterà poi di visualizzarla in maniera corretta. 
Queste statistiche verranno utilizzate a fini statistici Creiamo a questo punto un nuovo DataFrame costituito dalle colonne dei dati che servono al modello. 
Le colonne verranno riempite con le somme cumulative che ci serviranno per i modelli che interverranno successivamente.
Iteriamo dunque ogni partita del dataset precedente e troviamo le somme cumulative delle statistiche utili per entrambe le squadre coinvolte nella partita.
Inoltre, converitamo il risultato di ogni partita in una stringa:  <br>
• 001 equivale alla vittoria squadra casa  <br>
• 010 equivale al pareggio <br>
• 100 equivale alla vittoria squadra ospite <br>
A questo punto creiamo una nuova riga in cui inseriamo i valori calcolati così da ottenere un record pronto ad essere inserito nel DataFrame contenente
le statistiche aggregate per ogni partita, operazione eseguita al termine di ogni iterazione. 
Selezioniamo dunque quali colonne utilizzare come input (tutte le colonne relative alle statistiche delle squadre di casa e della squadra ospite, che
denominiamo con ’X’) e quali colonne come output (il risultato della partita, che denomiamo con ’Y’).
Dunque, arrivati in questa fase, inizializziamo una serie di variabili necessarie per tenere traccia del seed migliore del classificatore e definiamo poi i tre
classificatori: <br>
• clf1 : RandomForestClassifier con dei paramteri specificati come profondità massima dell’albero, numero massimo di funzionalità. <br>
• clf2 : LogisticRegression con numero di iterazioni specificate <br>
• clf3 : SVC con parametri specificati come regolarizzazione e kernel gamma <br>
Creaiamo un voting classifier (eclf ) che combina i tre classificatori definiti precedentemente usando un metodo ”hard” così che tutti i classificatori abbiano un
voto uguale nel determinare il risultato finale (viene in pratica effettuata una media). 
Vengono poi addestrati i classificatore, in particolare viene avviato un ciclo for per testare diversi seed. In ogni iterazione si calcola l’accutatezza del
seed tramite la funzione ”calculate voting classifier accuracy” e si aggiorna il parametro best voting seed qualora l’accuratezza del ottenuta dal seed corrente
sia migliore di quella registrata fino a quel momento.
A questo punto implementiamo diverse funzioni:  <br>
• home: visualizza la home della piattaforma e gli passa la lista delle squadre <br>
• match: gestisce i dati ottenunti utilizzando altre funzioni e mostra i risultati nella pagina apposita <br>
• strengthPredictor : per ottenere la previsione basandosi sulla forza della squadra <br>
• votingClassifier : per ottenere la previsione basandosi sulla classificazione a voto <br>
• matchProbs: per calcolare in maniera statistica le possibilità di vittoria casa, vittoria trasferta e pareggio
