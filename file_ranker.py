# # import os
# # import operator
# # import sys
# # from PyPDF2 import PdfReader
# # from jinja2 import Environment, FileSystemLoader

# # # Read the genre from the command-line arguments
# # genre = sys.argv[1]

# # # Loop through the folder containing the book files
# # folder_path = './books'
# # files = os.listdir(folder_path)

# # # Rank each book
# # rankings = {}
# # for file in files:
# #     with open(os.path.join(folder_path, file), 'rb') as f:
# #         pdf = PdfReader(f)
# #         content = pdf.pages[0].extract_text()
# #         score = 0
# #         if genre in content:
# #             score += 1
# #         rankings[file] = score

# # # Sort the books by score
# # sorted_files = sorted(rankings.items(), key=operator.itemgetter(1), reverse=True)

# # # Select the top 3 books
# # selected_books = sorted_files[:3]

# # # Set up Jinja2 environment
# # env = Environment(loader=FileSystemLoader('./'))
# # template = env.get_template('template.html')

# # # Generate HTML
# # output = template.render(books=selected_books)
# # with open('output.html', 'w') as f:
# #     f.write(output)


# # import sys
# # import requests
# # import operator

# # # Define the genres and the number of books to fetch for each genre
# # genres = ['philosophy', 'fiction', 'romance', 'comics', 'science fiction']
# # num_books_per_genre = 3

# # # Fetch the books
# # books = []
# # for genre in genres:
# #     response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults={num_books_per_genre}')
# #     books.extend(response.json()['items'])

# # # Read the target genre from the command-line arguments
# # target_genre = sys.argv[1]

# # # Rank each book
# # rankings = {}
# # for book in books:
# #     title = book['volumeInfo']['title']
# #     authors = ', '.join(book['volumeInfo'].get('authors', []))
# #     description = book['volumeInfo'].get('description', '')
# #     score = description.lower().count(target_genre.lower())
# #     rankings[(title, authors)] = score

# # # Sort the books by score
# # sorted_books = sorted(rankings.items(), key=operator.itemgetter(1), reverse=True)

# # # Select the top 3 books
# # selected_books = sorted_books[:3]

# # # Print the selected books and the reason for their selection
# # for book, score in selected_books:
# #     title, authors = book
# #     print(f'Title: {title}, Authors: {authors}, Score: {score}')
# #     print(f'Reason: The description of this book contains the word "{target_genre}" {score} times.')


# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import requests
# import operator

# router = APIRouter()
# templates = Jinja2Templates(directory="templates")

# from fastapi import Form

# from fastapi import Form

# @router.post("/rank", response_class=HTMLResponse)
# async def rank_books(request: Request, target_genre: str = Form(...)):
#     genres = ['philosophy', 'fiction', 'romance', 'comics', 'science fiction']
#     num_books_per_genre = 3
#     books = []
#     for genre in genres:
#         response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults={num_books_per_genre}')
#         books.extend(response.json()['items'])
#     rankings = {}
#     for book in books:
#         title = book['volumeInfo']['title']
#         authors = ', '.join(book['volumeInfo'].get('authors', []))
#         description = book['volumeInfo'].get('description', '')
#         score = description.lower().count(target_genre.lower())
#         rankings[(title, authors)] = score
#     sorted_books = sorted(rankings.items(), key=operator.itemgetter(1), reverse=True)
#     selected_books = sorted_books[:3]
#     return templates.TemplateResponse("index.html", {"request": request, "selected_books": selected_books})
