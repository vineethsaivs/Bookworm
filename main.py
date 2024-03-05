# pip install fastapi
from fastapi import FastAPI, Request, HTTPException, Response, Depends, status, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import httpx
from elasticsearch import Elasticsearch
from typing import Optional
import requests
import matplotlib.pyplot as plt
from io import BytesIO

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

import jwt

import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import List

# from file_ranker import router as file_ranker_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

GOOGLE_BOOKS_API_KEY = "AIzaSyA3J7SOTWbxxhxnUCgrX3PbGSwP3KadgmA"
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
# GOOGLE_BOOKS_API_URL = f"https://www.googleapis.com/books/v1/volumes?key=AIzaSyA3J7SOTWbxxhxnUCgrX3PbGSwP3KadgmA"

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class Book(BaseModel):
    id: str
    volumeInfo: dict

def fetch_books_by_genre(genre, num_books):
    params = {
        'q': f'subject:{genre}',
        'key': GOOGLE_BOOKS_API_KEY,
        'maxResults': num_books
    }
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()  # Raise an exception if the request failed
        data = response.json()
        return data['items']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
    except KeyError:
        print(f"Key 'items' not found in the response data: {data}")
        return []

@app.on_event("startup")
async def startup_event():
    global books
    books = {genre: fetch_books_by_genre(genre, 3) for genre in ['philosophy', 'fiction', 'romance', 'comics', 'sci-fi']}

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/books", response_class=HTMLResponse)
async def get_form(request: Request):
    all_books = [book for genre_books in books.values() for book in genre_books]
    return templates.TemplateResponse("form.html", {"request": request, "all_books": all_books})

@app.post("/books/results", response_class=HTMLResponse)
async def get_results(request: Request, genre: str = Form(...)):
    all_books = [book for genre_books in books.values() for book in genre_books]
    selected_genre_books = books.get(genre.lower(), [])
    return templates.TemplateResponse("results.html", {"request": request, "all_books": all_books, "selected_genre_books": selected_genre_books})

@app.get("/books/{genre}", response_model=List[Book])
async def get_books_by_genre(genre: str):
    return books.get(genre, [])


# Books Endpoint

@app.get("/books/", response_class=HTMLResponse)
async def list_books(request: Request, q: str = "python"):
    params = {"q": q} if q else {}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        print(response.text)
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    data = response.json()
    print(data)

    books = data.get("items", [])
    print(books)

    for book in books:
        book["volumeInfo"]["link"] = f"https://books.google.com/books?id={book['id']}"

    print({"request": request, "books_data": books, "query": q})

    return templates.TemplateResponse("books.html", {"request": request, "books_data": books, "query": q})

# Book Details Endpoint

@app.get("/books/{book_id}", response_class=HTMLResponse)
async def get_book_details(request: Request, book_id: str):
    params = {"key": "AIzaSyA3J7SOTWbxxhxnUCgrX3PbGSwP3KadgmA"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GOOGLE_BOOKS_API_URL}/{book_id}", params=params)

    if response.status_code != 200:
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    book = response.json()

    book["volumeInfo"]["link"] = f"https://books.google.com/books?id={book_id}"

    return templates.TemplateResponse("book_details.html", {"request": request, "book": book})


# recheck
@app.get("/books/{isbn}", response_class=HTMLResponse)
async def get_book(request: Request, isbn: str):
    params = {"q": f"isbn:{isbn}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    book_data = response.json()
    if not book_data["items"]:
        raise HTTPException(status_code=404, detail="Book not found")

    book = book_data["items"][0]

    book["volumeInfo"]["link"] = f"https://books.google.com/books?id={book['id']}"

    return templates.TemplateResponse("book_isbn_details.html", {"request": request, "book": book})
    # return templates.TemplateResponse("book_details.html", {"request": request, "book": book})

# Genres Endpoint

@app.get("/genres/{genre}", response_class=HTMLResponse)
async def list_books_by_genre(request: Request, genre: str):
    params = {"q": f"subject:{genre}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    print(response.text)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    books_data = response.json().get("items", [])
    # books_data = response.json().get("items", [])
    books_data = [{"bookId": book["id"], "title": book["volumeInfo"]["title"]} for book in books_data]
    print(books_data)
    return templates.TemplateResponse("genres.html", {"request": request, "books_data": books_data})

#recheck
@app.get("/authors/{author}", response_class=HTMLResponse)
async def list_books_by_author(request: Request, author: str):
    params = {"q": f"inauthor:{author}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    books = response.json().get("items", [])
    return templates.TemplateResponse("authors.html", {"request": request, "books": books})


# Authors Endpoint

import logging
@app.get("/authors/", response_class=HTMLResponse)
async def get_authors(request: Request):
    authors = ["J.K. Rowling", "Stephen King", "Agatha Christie", "Margaret Atwood", "George Orwell", "Ayn Rand", "Friedrick Nietzche", "William Shakespeare", "Charles Dickens", "Jane Austen", "Immanuel Kant", "Aristotle", "Plato", "Socrates", "Homer", "Virgil", "Dante Alighieri", "Geoffrey Chaucer", "Miguel de Cervantes", "Leo Tolstoy", "Fyodor Dostoevsky", "Anton Chekhov", "Nikolai Gogol", "Ivan Turgenev", "Alexander Pushkin", "Herman Melville", "Mark Twain", "Edgar Allan Poe", "Henry James", "Emily Dickinson", "Walt Whitman", "Ralph Waldo Emerson", "Nathaniel Hawthorne", "Herman Melville", "Louisa May Alcott", "Henry David Thoreau", "Harriet Beecher Stowe", "Frederick Douglass", "Walt Whitman", "Emily Dickinson", "Mark Twain", "Kate Chopin", "Charlotte Perkins Gilman", "Edith Wharton", "Willa Cather", "Zora Neale Hurston", "F. Scott Fitzgerald", "Ernest Hemingway", "William Faulkner", "John Steinbeck", "Ray Bradbury", "Kurt Vonnegut", "Toni Morrison", "Maya Angelou", "Alice Walker", "Sylvia Plath", "Flannery O'Connor", "Eudora Welty", "Carson McCullers", "Harper Lee", "Truman Capote", "Tennessee Williams", "Arthur Miller", "Eugene O'Neill", "Edward Albee", "Samuel Beckett", "William Shakespeare", "Christopher Marlowe", "Ben Jonson", "John Webster", "John Ford", "Thomas Middleton", "Thomas Kyd", "Thomas Dekker", "Francis Beaumont", "John Fletcher", "Philip Massinger", "John Ford", "James Shirley", "Richard Brome", "Thomas Heywood", "John Marston", "George Chapman", "Thomas Nashe", "Robert Greene", "Thomas Lodge", "John Lyly", "George Peele", "Thomas Kyd", "Christopher Marlowe", "William Shakespeare", "Ben Jonson", "John Webster", "John Ford", "Thomas Middleton", "Thomas Dekker", "Francis Beaumont", "John Fletcher", "Philip Massinger", "John Ford", "James Shirley", "Richard Brome"]

    return templates.TemplateResponse("authors_list.html", {"request": request, "authors": authors})

# Publishers Endpoint

@app.get("/publishers/{publisher}", response_class=HTMLResponse)
async def list_books_by_publisher(request: Request, publisher: str):
    params = {"q": f"inpublisher:{publisher}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    books = response.json().get("items", [])
    return templates.TemplateResponse("publishers.html", {"request": request, "books": books})


# Print Type Endpoint

@app.get("/printtype/{print_type}", response_class=HTMLResponse)
async def list_books_by_print_type(request: Request, print_type: str):
    params = {"q": "*", "printType": print_type}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    data = response.json()
    if "items" not in data:
        return JSONResponse(content={"detail": "No books found for this print type"}, status_code=404)

    books = data["items"]
    return templates.TemplateResponse("print_type.html", {"request": request, "books": books})


# Language Endpoint

@app.get("/language/{lang}", response_class=HTMLResponse)
async def list_books_by_language(request: Request, lang: str):
    params = {"q": "*", "langRestrict": lang}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    data = response.json()
    if "items" not in data:
        return JSONResponse(content={"detail": "No books found for this language"}, status_code=404)

    books = data["items"]
    return templates.TemplateResponse("language.html", {"request": request, "books": books})


# Sort and Search Endpoint


@app.get("/sort/{order}", response_class=HTMLResponse)
async def list_books_sorted(request: Request, order: str):
    params = {"q": "*", "orderBy": order}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    data = response.json()
    if "items" not in data:
        return JSONResponse(content={"detail": "No books found for this sort order"}, status_code=404)

    books = data["items"]
    return templates.TemplateResponse("sort.html", {"request": request, "books": books})


@app.get("/sort/{order}/{query}", response_class=HTMLResponse)
async def list_books_sorted(request: Request, order: str, query: str):
    params = {"q": query, "orderBy": order}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    data = response.json()
    if "items" not in data:
        return JSONResponse(content={"detail": "No books found for this sort order"}, status_code=404)

    books = data["items"]
    return templates.TemplateResponse("sort.html", {"request": request, "books": books})


# Publication Date Endpoint

years = []
@app.get("/pubdate/{query}", response_class=HTMLResponse)
async def list_books_by_pubdate(request: Request, query: str):
    global years
    params = {"q": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book data")

    data = response.json()
    if "items" not in data:
        return JSONResponse(content={"detail": "No books found for this query"}, status_code=404)

    books = data["items"]
    for book in books:
        if 'volumeInfo' in book and 'publishedDate' in book['volumeInfo']:
            year = book['volumeInfo']['publishedDate'][:4]
            if year.isdigit():
                years.append(int(year))

    return templates.TemplateResponse("pubdate.html", {"request": request, "books": books})


# Visualization with a Histogram

@app.get("/histogram", response_class=Response)
async def get_histogram():
    global years
    if not years:
        return JSONResponse(content={"detail": "No data available for histogram"}, status_code=404)
    plt.hist(years, bins=range(min(years), max(years) + 1), alpha=0.7, edgecolor='black')
    plt.title('Publication Years of Books')
    plt.xlabel('Year')
    plt.ylabel('Number of Books')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Response(buf.read(), media_type='image/png')



# Elastic search

es = Elasticsearch(hosts=["http://localhost:9200"])

async def fetch_books(query: str):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}')
    data = response.json()
    books = []
    for item in data['items']:
        book = {
            'id': item['id'],
            'title': item['volumeInfo']['title'],
            'authors': item['volumeInfo'].get('authors', []),
            'publishedDate': item['volumeInfo'].get('publishedDate', ''),
            'description': item['volumeInfo'].get('description', ''),
            'categories': item['volumeInfo'].get('categories', []),
            'averageRating': item['volumeInfo'].get('averageRating', ''),
            'ratingsCount': item['volumeInfo'].get('ratingsCount', ''),
            'imageLinks': item['volumeInfo'].get('imageLinks', {}),
        }
        books.append(book)
    return books

@app.get("/index/{query}")
async def index_books(query: str):
    if not es.indices.exists(index='books'):
        es.indices.create(index='books')
    data = await fetch_books(query)
    for book in data:
        es.index(index='books', body=book)
    return {"message": "Books indexed successfully"}



@app.get("/search/{query}", response_class=HTMLResponse)
async def search_books(query: str):
    response = es.search(index='books', body={'query': {'match': {'title': query}}})
    books = [hit['_source'] for hit in response['hits']['hits']]

    html_content = "<h1>Search Results</h1>"
    for book in books:
        html_content += f"<h2>{book['title']}</h2>"
        html_content += f"<h3>Authors: {', '.join(book['authors'])}</h3>"
        html_content += f"<p>Published Date: {book['publishedDate']}</p>"
        html_content += f"<p>{book['description']}</p>"
        html_content += "<hr>"

    return html_content


# JWT token Authentication

class Token(BaseModel):
    access_token: str
    token_type: str

# openssl rand -hex 32
SECRET_KEY = "06eba4a0480628effabed1c08d9712dafc3820a8e0181ac2306ba1e872fd6be1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "vineethsai": {
        "username": "vineethsai",
        "full_name": "Vineeth Sai",
        "email": "vineethsai@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class TokenData(BaseModel):
    username: Optional[str] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return user_dict

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return User(**user)

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# nltk.download('vader_lexicon')

# sentiment analysis

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

templates = Jinja2Templates(directory="templates")

@app.get("/sentiment/{book_id}", response_class=HTMLResponse)
async def get_book_sentiment(request: Request, book_id: str):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{book_id}')
    book_data = response.json()
    
    review = book_data.get('volumeInfo', {}).get('description', '')
    if not review:
        return {"error": "No description found for this book"}

    sentiment_scores = sid.polarity_scores(review)
    return templates.TemplateResponse("sentiment.html", {"request": request, "book_id": book_id, "review": review, "sentiment_scores": sentiment_scores})

# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
