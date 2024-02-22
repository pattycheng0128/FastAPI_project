from fastapi import FastAPI

app = FastAPI()

@app.get("/api-endpoint")
async def first_api():
    return {"message": "Hello Patty!"}

# How to run: uvicorn books:app --reload
