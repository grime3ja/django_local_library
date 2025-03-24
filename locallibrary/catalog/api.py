from typing import List
import uuid
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from ninja import NinjaAPI, Schema
from .models import Author, Genre, Book, BookInstance
from datetime import date

api = NinjaAPI()

class HelloSchema(Schema):
    name: str = "world"

class AuthorSchema(Schema):
    first_name: str
    last_name: str
    date_of_birth: date
    date_of_death: date

class GenreSchema(Schema):
    name: str

class BookSchema(Schema):
    title: str
    author: AuthorSchema = None
    summary: str
    isbn: str
    genre: GenreSchema = None

class BookInstanceSchema(Schema):
    book: BookSchema = None
    imprint: str
    due_back: date
    borrower: str
    status: str


@api.post("/hello")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"

@api.get("/math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}

@api.post("/author/create")
def author_create(request, payload: AuthorSchema):
    author = Author.objects.create(**payload.dict())
    return author.__str__()

@api.get("/author/", response=List[AuthorSchema])
def author_get(request, last_name):
    author = get_list_or_404(Author, last_name=last_name)
    return author

@api.put("/author/{last_name}")
def author_update(request, last_name: str, payload: AuthorSchema):
    author = get_object_or_404(Author, last_name=last_name)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return {"success": True}

@api.delete("/author/{last_name}")
def author_delete(request, last_name: str):
    author = get_object_or_404(Author, last_name=last_name)
    author.delete()
    return {"success": True}

@api.post("/genre/create")
def genre_create(request, payload: GenreSchema):
    genre = Genre.objects.create(**payload.dict())
    return genre.__str__()

@api.get("/genre/", response=List[GenreSchema])
def genre_get(request, name):
    genre = get_list_or_404(Genre, name=name)
    return genre

@api.put("/genre/{name}")
def genre_update(request, name: str, payload: GenreSchema):
    genre = get_object_or_404(Genre, name=name)
    for attr, value in payload.dict().items():
        setattr(genre, attr, value)
    genre.save()
    return {"success": True}

@api.delete("/genre/{name}")
def genre_delete(request, name: str):
    genre = get_object_or_404(Genre, name=name)
    genre.delete()
    return {"success": True}

@api.post("/book/create")
def book_create(request, payload: BookSchema):
    book = {
        "title": payload.title,
        "author": Author.objects.get_or_create(**payload.author.dict())[0],
        "summary": payload.summary,
        "isbn": payload.isbn,
    }
    book_object = Book.objects.create(**book)
    book_object.genre.set([Genre.objects.get_or_create(**payload.genre.dict())[0]])
    return book_object

@api.get("/book/", response=List[BookSchema])
def book_get(request, title):
    book = get_list_or_404(Book, title=title)
    return book

@api.put("/book/{isbn}")
def book_update(request, isbn: str, payload: BookSchema):
    book = get_object_or_404(Book, isbn=isbn)
    setattr(book, "title", payload.title)
    setattr(book, "author", Author.objects.get_or_create(**payload.author.dict())[0])
    setattr(book, "summary", payload.summary)
    book.genre.set([Genre.objects.get_or_create(**payload.genre.dict())[0]])
    book.save()
    return {"success": True}

@api.delete("/book/{isbn}")
def book_delete(request, isbn: str):
    book = get_object_or_404(Book, isbn=isbn)
    book.delete()
    return {"success": True}

@api.post("/book_instance/create")
def book_instance_create(request, payload: BookInstanceSchema):
    book = book_create(None, payload.book)
    book_instance = {
        "book": book,
        "imprint": payload.imprint,
        "due_back": payload.due_back,
        "borrower": get_user_model().objects.get(username=payload.borrower),
        "status": payload.status,
    }
    BookInstance.objects.create(**book_instance)
    return book_instance.__str__()

@api.get("/book_instance/", response=List[BookInstanceSchema])
def book_instance_get(request, id):
    book_instance = get_list_or_404(BookInstance, id=id)
    return book_instance

@api.put("/book_instance/{id}")
def book_instance_update(request, id: str, payload: BookInstanceSchema):
    book_instance = get_object_or_404(BookInstance, id=id)
    # for attr, value in payload.dict().items():
    #     setattr(book_instance, attr, value)
    book = book_create(None, payload.book)
    setattr(book_instance, "book", book)
    setattr(book_instance, "imprint", payload.imprint)
    setattr(book_instance, "due_back", payload.due_back)
    setattr(book_instance, "borrower", get_user_model().objects.get(username=payload.borrower))
    setattr(book_instance, "status", payload.status)
    book_instance.save()
    return {"success": True}

@api.delete("/book_instance/{id}")
def book_instance_delete(request, id: str):
    book_instance = get_object_or_404(BookInstance, id=id)
    book_instance.delete()
    return {"success": True}