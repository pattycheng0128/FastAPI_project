from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
# pydantic定義數據模型，然後使用這些模型來驗證和處理輸入的數據

app = FastAPI()
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    #繼承BaseModel
    id: Optional[int] # 及時沒傳入id，仍可自動生成這行
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

BOOKS = [
    Book(1, 'computer science', 'Tim', 'computer science description', 5),
    Book(2, 'math', 'Amy', 'math description', 5),
    Book(3, 'chinese', 'Lulu', 'chinese description', 5),
    Book(4, 'English', 'John', 'English description', 5),
    Book(5, 'physics', 'Linda', 'physics description', 5),
    Book(6, 'biology', 'Patty', 'biology description', 5)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create-book")
async def create_book(book_requset: BookRequest): #body會顯示預設內容
    new_book = Book(**book_requset.model_dump())
    BOOKS.append(find_book_id(new_book))
    # BOOKS.append(book_requset)
    # print(type(new_book)) #books2.Book
    # return BOOKS

def find_book_id(book: Book):
    #另一種寫法: book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id+1
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id+1
    else:
        book.id=1
    
    return book
