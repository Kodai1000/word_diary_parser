from fastapi import FastAPI
from pydantic import BaseModel
from sudachipy import Dictionary

app = FastAPI()

# SudachiのTokenizerを初期化
tokenizer = Dictionary().create()

class TextRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message" : "Hello World"}

@app.post("/analyze")
def analyze(request: TextRequest):
    tokens = tokenizer.tokenize(request.text)

    result = []

    for token in tokens:
        result.append({
            "surface": token.surface(),
            "dictionary_form": token.dictionary_form(),
            "pos": token.part_of_speech(),
        })

    return {
        "text": request.text,
        "tokens": result
    }