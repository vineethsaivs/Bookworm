# Project Documentation

## Overview

The project, named "Bookworm", is a comprehensive book analysis and recommendation system. It uses several APIs, including the Google Books API, Geolocation API, Geocoding API, Places API, and Maps JavaScript API, to fetch and analyze book data, recommend books based on user input, and locate nearby libraries.

## Main Features

### Book Data Fetching

The main.py script provides several endpoints for fetching book data from the Google Books API. Users can fetch books based on various criteria, including keyword, book ID, ISBN, genre, author, publisher, print type, and language. Users can also sort the fetched books based on relevance, newest, and publishing date.

### Book Analysis

The project includes four Python scripts for analyzing book data:

1. **Book Reviews Analysis**: This script fetches book data based on user-provided queries and analyzes the average rating and total rating count for each book. The top 10 books with the highest average rating and total rating count are displayed on a bar chart.

2. **Genre Trends Analysis**: This script fetches book data based on user-provided genre queries. It calculates the number of books and average rating for each genre and displays these data on a bar chart.

3. **Author Analysis**: This script fetches book data based on user-provided author queries. It calculates the number of books and average rating for each author and displays these data on a bar chart.

4. **Language Analysis**: This script fetches book data based on user-provided language codes. It calculates the number of books for each language and displays these data on a bar chart.

### Book Recommendation

The project uses the BERT model to recommend books based on user input. The recommendation system returns the top 3 books that are most relevant to the genre mentioned in the criteria. For each of the top 3 books, it also returns the most important words that were considered to predict that the book belonged to the particular genre, along with their attention scores.

### Library Locator

The project uses the Google Maps APIs to locate the nearest libraries to a given location. The location is specified by latitude and longitude coordinates. The results are displayed on a Google Map with markers for each library.

### Chatbot

The project includes a chatbot named "ShelfAware" that recommends books based on user input. The chatbot uses the Google Books API to fetch relevant books.

## Usage

To run the project, you need Python installed on your machine. You can run a script by navigating to the directory containing the script and running the following command in your terminal:

```bash
python <script_name>.py
```

To use the library locator feature, navigate to the /libraries endpoint in your web browser and provide the latitude and longitude as query parameters. For example:

```bash
http://127.0.0.1:8000/libraries?latitude=37.706252&longitude=-122.441907
```

This will display a map of the nearest libraries to the coordinates 37.706252, -122.441907.

## Dependencies

The project depends on several Python libraries, including:

- fastapi
- requests
- json

You can install these libraries using pip:

```bash
pip install fastapi requests json
```

## Conclusion

The "Bookworm" project is a comprehensive tool for book lovers, providing a wide range of features from book data fetching and analysis to book recommendation and library location. It leverages several APIs and advanced machine learning models to provide accurate and relevant results.
