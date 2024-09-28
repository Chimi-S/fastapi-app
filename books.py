from fastapi import FastAPI, Body
app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/books")
async def get_books():
    return BOOKS

@app.get("/book/{book_title}")
async def get_book(param:str):
 book = [book for book in BOOKS if book.get('title').casefold() == param.casefold()]
 return book

@app.get("/books/{book_author}/")
async def get_books_by_category(book_author:str, category:str):
    books = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold() and book.get('author').casefold() == book_author.casefold():
            books.append(book)
    return books

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            del BOOKS[i]
            break
