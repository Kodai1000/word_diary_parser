import re

from fastapi import FastAPI
from pydantic import BaseModel
from sudachipy import Dictionary
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# SudachiのTokenizerを初期化
tokenizer = Dictionary().create()


class TextRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/analyze")
def analyze(request: TextRequest):
    # 空白・改行を保持したまま分割
    # \u3000 = 全角空白
    # \u0020 = 半角空白
    # \n = 改行
    parts = re.split(r'([ \u3000\n])', request.text)

    result = []

    for part in parts:
        if part == "":
            continue

        # 全角空白
        if part == "\u3000":
            result.append({
                "surface": part,
                "dictionary_form": "[全角空白]",
                "pos": "#記号"
            })

        # 半角空白
        elif part == " ":
            result.append({
                "surface": part,
                "dictionary_form": "[半角空白]",
                "pos": "#記号"
            })

        # 改行
        elif part == "\n":
            result.append({
                "surface": part,
                "dictionary_form": "[改行]",
                "pos": "#記号"
            })

        # 通常の文字列
        else:
            tokens = tokenizer.tokenize(part)

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