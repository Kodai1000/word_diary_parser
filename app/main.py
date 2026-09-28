from fastapi import FastAPI
from pydantic import BaseModel
from sudachipy import Dictionary
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

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