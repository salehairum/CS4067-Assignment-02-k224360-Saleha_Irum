from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}

# Run the server with: uvicorn main:app --reload