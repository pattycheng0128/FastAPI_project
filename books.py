from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'math'},
    {'title': 'Title Two', 'author': 'Author One', 'category': 'chinese'},
    {'title': 'Title Three', 'author': 'Author One', 'category': 'English'},
    {'title': 'Title Four', 'author': 'Author One', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author One', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author One', 'category': 'math'},
]

# get request
@app.get("/books")
async def first_api():
    return BOOKS

# path parameters 動態參數
# @app.get("/books/{dynamic_param}")
# # 預設是整數
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_param': dynamic_param}

# %20代表space, casefold()將字串轉成小寫
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

# How to run: uvicorn books:app --reload
