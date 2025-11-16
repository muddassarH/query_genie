import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
# function imports
from db_connection import get_db_connection
from agents import query_ollama
from helpers import extract_sql_query, sql_parser
from prompts import SQL_PROMPT
load_dotenv()

app = FastAPI()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")


@app.post("/query_db")
def query_db(sql: str):
    conn = get_db_connection(db_name, db_user, db_pass)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        if cur.description:
            result = cur.fetchall()
        else:
            conn.commit()
            result = {"status": True, "result": sql}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"result": sql, "status": "success" if result else "Something went wrong"}

@app.post("/ask")
def ask(prompt: str):
    # Example: let Ollama decide SQL query
    sql_prompt = f"{SQL_PROMPT} {prompt}"
    # getting response from ollama/Chatgpt model.
    raw_model_response = query_ollama(sql_prompt)
    if not raw_model_response:
        return {"status": "error", "result": raw_model_response}
    # getting sql query from model response
    sql_query = extract_sql_query(raw_model_response)
    # checking in query in safe sandbox in postgresql for validation.
    # parsed_sql_query = sql_parser(sql_query,db_name, db_user, db_pass)
    # if not parsed_sql_query:
    #     return {"status": "Error", "result" :f"Something is wrong with generated query: {sql_query}"}
    # return query_db(sql_query)
    # just returning the query without validate and executing it.
    return {"status": "success", "result": sql_query}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, factory=False )