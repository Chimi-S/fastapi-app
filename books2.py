from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

BOOKS = [
    Book(1, 'Computer Science Pro', 'john', 'A very nice book!', 5, 2033),
    Book(2, 'Be Fast with FastAPI', 'john', 'A great book!', 5, 2023),
    Book(3, 'Master Endpoints', 'john', 'A awesome book!', 5, 2023),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2022),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3,2002),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2000)
]

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="The id not need on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra" : {
            "example": {
                "title": "Book Title",
                "author": "<NAME>",
                "description": "Book Description",
                "rating": 5.0,
                "published_date": 2022
            }
        }
    }

@app.get("/books")
async def read_books():
    return BOOKS

@app.get("/book/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get("/books/")
async def read_book_by_rating(book_rating: float):
    books = []
    for book in BOOKS:
        if book_rating == book.rating:
            books.append(book)
    return books


@app.post("/create-book")
async def create_books(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/update-book/update_book")
async def update_book(book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


