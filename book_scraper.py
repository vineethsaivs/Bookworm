import requests
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'YOUR_API_KEY'

# Define the search query
query = "science fiction"

# Define the URL
url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"

# Send a GET request to the API
response = requests.get(url)

# Convert the response to JSON
data = response.json()

# Extract the necessary information from the data
books = []
for item in data['items']:
    try:
        title = item['volumeInfo']['title']
        description = item['volumeInfo']['description']
        categories = item['volumeInfo']['categories']
        books.append([title, description, categories])
    except KeyError:
        continue

# Convert the list of books to a DataFrame
df = pd.DataFrame(books, columns=['Title', 'Description', 'Categories'])



from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re

# Download the necessary NLTK data
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Define the stop words
stop_words = set(stopwords.words('english'))

# Define the lemmatizer
lemmatizer = WordNetLemmatizer()

# Define a function to preprocess the text
def preprocess_text(text):
    # Convert the text to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize the text
    words = word_tokenize(text)
    # Remove stop words and lemmatize the words
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    # Join the words back into a string
    text = ' '.join(words)
    return text

# Preprocess the descriptions
df['Description'] = df['Description'].apply(preprocess_text)



