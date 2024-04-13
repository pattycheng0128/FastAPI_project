from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status
# Path用於定義路徑參數, Query 用於定義查詢參數
from pydantic import BaseModel, Field
# pydantic定義數據模型，然後使用這些模型來驗證和處理輸入的數據

# 加了published_date後開始異常

app = FastAPI()
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published_date

class BookRequest(BaseModel):
    #繼承BaseModel
    id: Optional[int] = Field(title = "id is not needed") #沒傳入id，仍可自動生成這行，文字出不來
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6) # 0~5分，大於0小於6
    published_date: int = Field(gt=1999, lt=2031)
    # gt means greater than(大於)
    # lt means less than(小於)

    class Config:
        json_schema_extra = {
            "example": {
               'title': 'A new book',
               'author': 'codingwithruby',
               'description': 'computer science description',
               'rating': 5,
               'published_date': 2022
            }
        }

BOOKS = [
    Book(1, 'computer science', 'Tim', 'computer science description', 5, 2011),
    Book(2, 'math', 'Amy', 'math description', 5, 2022),
    Book(3, 'chinese', 'Lulu', 'chinese description', 3, 2011),
    Book(4, 'English', 'John', 'English description', 2, 2000),
    Book(5, 'physics', 'Linda', 'physics description', 1, 2003),
    Book(6, 'biology', 'Patty', 'biology description', 5, 2004)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# 輸入book_id，會回傳該書。Path的目的是限制book_id必須大於0
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")
        
# 輸入幾顆星，會回傳該顆星以上的書
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

# 書的出版日期
@app.get("/books/publish/")
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published == published_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book")
async def create_book(book_requset: BookRequest): #body會顯示預設內容
    new_book = Book(**book_requset.model_dump())
    BOOKS.append(find_book_id(new_book))
    # BOOKS.append(book_requset)
    # print(type(new_book)) #books2.Book
    # return BOOKS

def find_book_id(book: Book):
    #另一種寫法-三元運算式: book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id+1
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id+1
    else:
        book.id=1
    
    return book

# 壞掉了
@app.put('/books/update_book/', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    # book_changed = False # 是否有修改
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            # book_changed = True # 有修改
    # if not book_changed:
    #     raise HTTPException(status_code=404, detail="Item not found")

# Path的目的是限制book_id必須大於0
@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False # 是否有修改
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True # 有修改
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")