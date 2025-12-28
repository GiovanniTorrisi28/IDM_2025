## Descrizione del Progetto

**eVTranslator** è un *multi-agent SQL parser* sviluppato utilizzando **LangGraph**, il cui obiettivo è tradurre query espresse in **linguaggio naturale** in **query SQL** corrette ed eseguibili.

Il contesto applicativo per cui è stato sviluppato **eVTranslator** riguarda i dati di **eVision**, un’azienda specializzata nello sviluppo di soluzioni software per aziende della **Grande Distribuzione Organizzata (GDO)**. In questo scenario, il sistema consente di interrogare in modo intuitivo grandi volumi di dati aziendali, migliorando accessibilità e velocità di analisi.

-----------------------  
## Requisiti

Per eseguire correttamente il progetto è necessario disporre dei seguenti requisiti:

- **Python** installato sul sistema
- **Credenziali di accesso** al database ClickHouse (host, porta, username, password)
- **Api Key** per l'accesso a un Large Language Model (LLM)

------------------------
## Istruzioni per l'esecuzione

Clonare il repository GitHub in una directory locale:

```bash
git clone <URL_DEL_REPOSITORY>
cd eVTranslator
```

Creare un ambiente virtuale Python:

```bash
python -m venv venv
```
Attivare l'ambiente virtuale:
```bash
.\venv\Scripts\activate.bat        # su windows
source venv/bin/activate           # su macOS/Linux

```
Installare tutte le dipendenze:
```bash
pip install -r requirements.txt
```

Rinominare il file delle variabili d'ambiente e configurarlo con i valori corretti.  
(N.B per i valori stringa non è necessario includerli tra apici o virgolette)
```bash
mv .env.example .env            
```

Avviare l'applicazione:
```bash
streamlit run src/main.py          
```

## Struttura del repository

- `documentation/`- Cartella contenente la documentazione del progetto.
   - `project_report.pdf` - Relazione finale.
- `src/` – Cartella dei file sorgenti.
  - `nodes` - Sottocartella dei nodi del grafo.
    - `executor.py`- Nodo Agente che esegue il codice SQL.
    - `generator.py` - Nodo Agente che genera il codice SQL.
    - `guard.py` - Nodo Agente che filtra le richieste utente rilevanti.
    - `load_schema.py`- Nodo che interroga il database per ottenere lo schema della tabella.
    - `result_handler.py` - Nodo Agente che elabora i risultati.
  - `router` - Sottocartella delle funzioni di instradamento.
      - `choose_if_continue.py`- Funzione di routing per l'instradamento dopo il filtro.
      - `choose_if_retry.py` - Funzione di routing per l'instradamento dopo l'esecuzione della query.
  - `graph.py` - Funzione per la costruzione del grafo.
  - `main.py` - Punto di accesso del progetto. Definizione dell' UI.
  - `state.py` - Classe che rappresenta lo stato del grafo.
  - `utils.py` - Insieme di funzioni di utilità.
- `.env.example` - File template di configurazione delle variabili di ambiente.
- `requirements.txt` - Elenco dei pacchetti Python necessari per far funzionare il progetto.

---

## Framework principali utilizzati

### **Streamlite**
Framework python per creare web app interattive.

### **LangGraph**
Framework python basato su LangChain per costruire workflow e agenti LLM a stati e grafi.
