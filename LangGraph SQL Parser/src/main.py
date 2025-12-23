import streamlit as st
from graph import build_graph
import pandas as pd 
# Configurazione pagina
st.set_page_config(
    page_title="SQL Query Assistant",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 SQL Query Assistant")
st.write("Fai una domanda in linguaggio naturale e genererò una query SQL per te.")

# Input utente
user_question = st.text_area(
    "La tua domanda:",
    placeholder="Es: Quante vendite abbiamo avuto oggi?",
    height=100
)

# Pulsante esegui
if st.button("🚀 Esegui Query", type="primary", use_container_width=True):
    if user_question:
        with st.spinner("Elaborazione in corso..."):
            # Stato iniziale
            initial_state = {
                "user_question": user_question,
                "table_schema": None,
                "sql_query": "",
                "query_result": None,
                "query_error": None,
                "retry_count": 0,
                "dataframe": None
            }
            
            # Esegui il grafo
            app = build_graph()
            final_state = app.invoke(initial_state)
            
            # Mostra SQL generato
            st.subheader("📝 Query SQL generata")
            st.code(final_state["sql_query"], language="sql")
            
            # Mostra numero tentativi se > 1
            if final_state["retry_count"] > 1 and final_state["query_error"] is None:
                st.info(f"ℹ️ Query corretta dopo {final_state['retry_count']} tentativi")
            
            # Visualizza risultati o errori
            if final_state["query_error"] is None:
                # Successo - Mostra il DataFrame
                st.success("✅ Query eseguita con successo!")
                
                df = pd.DataFrame(final_state["query_result"])
                print("main stampa df",df)
                if df is not None and not df.empty:
                    st.subheader("📊 Risultati")
                    st.write(f"**Righe trovate:** {len(df)}")
                    
                    # Mostra DataFrame interattivo
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Statistiche (se ci sono colonne numeriche)
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        with st.expander("📈 Statistiche"):
                            st.write(df[numeric_cols].describe())
                    
                    # Download CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Scarica CSV",
                        data=csv,
                        file_name="risultati.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("ℹ️ La query è stata eseguita ma non ha restituito risultati.")
            else:
                # Errore
                st.error("❌ Errore nell'esecuzione della query")
                
                with st.expander("🔍 Dettagli errore", expanded=True):
                    st.code(final_state['query_error'], language="text")
                
                if final_state['retry_count'] >= 3:
                    st.error("🚫 Numero massimo di tentativi raggiunto")
    else:
        st.warning("⚠️ Inserisci una domanda prima di procedere")

# Sidebar con info
with st.sidebar:
    st.header("ℹ️ Informazioni")
    st.write("""
    Questo tool utilizza LangGraph per:
    1. 🔄 Tradurre domande in SQL
    2. ✅ Validare ed eseguire query
    3. 🔁 Correggere errori automaticamente (max 3 tentativi)
    """)
    
    st.divider()
    
    st.subheader("📊 Statistiche Sessione")
    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0
    st.metric("Query eseguite", st.session_state.query_count)