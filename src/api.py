from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import process_query

app = FastAPI(title="Nova - AI Function Executor")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/execute")
async def execute_query(request: QueryRequest):
    try:
        response = process_query(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

