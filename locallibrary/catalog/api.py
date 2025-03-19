from typing import List
from django.shortcuts import get_object_or_404, get_list_or_404
from ninja import NinjaAPI, Schema
from .models import Author, Genre
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
def author_update(request, l_name: str, payload: AuthorSchema):
    author = get_object_or_404(Author, last_name=l_name)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return {"success": True}

@api.delete("/author/{last_name}")
def author_delete(request, l_name: str):
    author = get_object_or_404(Author, last_name=l_name)
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