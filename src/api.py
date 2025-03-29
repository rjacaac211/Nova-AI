from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from src.agent import run_agent, clear_session

app = FastAPI(title="Nova - AI Function Executor")

class QueryRequest(BaseModel):
    prompt: str
    session_id: str = "default_session"

@app.post("/execute")
async def execute_query(request: QueryRequest):
    try:
        response = run_agent(request.session_id, request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear_session")
async def clear_session_endpoint(session_id: str = Query(..., description="Session ID to clear")):
    try:
        clear_session(session_id)
        return {"response": f"Session {session_id} cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

