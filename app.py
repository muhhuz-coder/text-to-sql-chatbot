import streamlit as st
import requests

API_URL = "http://localhost:8000/query"

st.set_page_config(page_title="RAG Text→SQL Demo", layout="centered")
st.title("RAG Text → SQL (SQLite replica)")

with st.form("query_form"):
    question = st.text_input(
        "Ask a natural language question (about the DB)",
        value="Show total orders per customer"
    )
    show_sql = st.checkbox("Show generated SQL", value=True)
    submitted = st.form_submit_button("Submit")

if submitted:
    question = str(question).strip()
    show_sql = bool(show_sql)
    if not question:
        st.warning("Please enter a question.")
    else:
        payload = {"question": question, "show_sql": show_sql}
        with st.spinner("Querying..."):
            try:
                resp = requests.post(API_URL, json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                if show_sql:
                    st.subheader("🧠 Generated SQL")
                    st.code(data.get("sql", ""), language="sql")
                st.subheader("📊 Query Results")
                rows = data.get("rows", [])
                if rows:
                    st.dataframe(rows)
                else:
                    st.info("No rows returned for this query.")
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred: {http_err} - {resp.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API. Make sure FastAPI is running on localhost:8000.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Try again later.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")