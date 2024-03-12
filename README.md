Documentation


**using_BERT.py**

This script uses the BERT model to classify books into categories based on their title and description.

1. **Imports and API Key**: The script imports necessary modules and defines the API key for the Google Books API.

2. **Data Fetching**: The script sends a GET request to the Google Books API with a search query, converts the response to JSON, and extracts the title, description, and category of each book.

3. **Data Processing**: The script converts the list of books to a DataFrame, combines the title and description into a single text feature, and encodes the category labels to integers.

4. **Model and Tokenizer Loading**: The script loads a pre-trained BERT model and tokenizer.

5. **Data Splitting**: The script splits the data into training and testing sets.

6. **Data Tokenization**: The script tokenizes the text data for both the training and testing sets.

7. **Custom Dataset Creation**: The script defines a custom dataset class that takes in the encodings and labels, and creates instances of this class for the training and testing sets.

8. **Optimizer Initialization**: The script initializes the AdamW optimizer with the model parameters.

9. **Model Training**: The script creates data loaders for the training and testing sets, moves the model to the GPU if available, sets the model to training mode, and trains the model for a certain number of epochs. In each epoch, it moves the batch tensors to the right device, performs a forward pass, computes the loss, performs a backward pass, updates the weights, and resets the gradients.

10. **Model Saving**: The script saves the trained model.

This script is crucial for training a BERT model to classify books into categories based on their title and description.




fetch_book_descriptions.py

Here's a high-level documentation for `fetch_book_descriptions.py`:

**fetch_book_descriptions.py**

This script fetches book descriptions from the Google Books API for different genres and saves them as text files.

1. **Imports and Constants**: The script imports necessary modules for HTTP requests and file system operations. It also defines the base URL for the Google Books API and a list of genres.

2. **Directory Creation**: The script checks if a directory named 'text_files' exists, and creates it if it doesn't.

3. **Data Fetching and Saving**: The script loops over the genres, sends a GET request to the Google Books API for each genre, and parses the response as JSON. It then loops over the items in the response data, extracts the title and description of each book, and saves the description as a text file in the 'text_files' directory. The filename is the title of the book.

This script is crucial for gathering the data that will be used for training the BERT model.




**rank_files.py**

This script ranks text files based on their relevance to a given criteria using a BERT model, and generates an HTML report of the results.

1. **Imports and Model Loading**: The script imports necessary modules and loads a pre-trained BERT model and tokenizer.

2. **Criteria Loading and Tokenization**: The script loads a criteria from a text file, tokenizes it, and stores the encoding.

3. **Text Files Loading and Relevance Scoring**: The script gets a list of text files, loads each file, tokenizes the text, combines the criteria encoding and the file encoding, feeds the combined encoding to the model, gets the logits for the 'relevant' class, takes the sigmoid to get the relevance score, and stores the score.

4. **Files Ranking**: The script pairs the filenames with their relevance scores, sorts them by score in descending order, and selects the top 3 files.

5. **HTML Report Generation**: The script initializes an HTML string, adds the filenames and their relevance scores to the string, loops over the top 3 files, loads each file, tokenizes the text, feeds the inputs to the model, gets the attention weights, sums the attention weights across all heads, flattens the summed attentions tensor, gets the indices and values of the top 10 most attended to tokens, decodes the top tokens and their corresponding values, adds the top words and their values to the HTML string, and writes the HTML string to a file.

This script is crucial for understanding which files are most relevant to the given criteria and why, as it not only ranks the files but also identifies the top words in each file that the model paid most attention to when making its decisions.





**Inisights**

# Book Analysis and Library Locator

This repository contains Python scripts for analyzing book reviews, genre trends, author popularity, and language usage, as well as a script for locating the nearest libraries using the Google Maps API.

## Book Reviews Analysis

The `book_reviews_analysis.py` script fetches book data from the Google Books API based on user-provided queries. It then analyzes the average rating and total rating count for each book and plots these data on a bar chart. The top 10 books with the highest average rating and total rating count are displayed.

## Genre Trends Analysis

The `genre_trends_analysis.py` script fetches book data from the Google Books API based on user-provided genre queries. It then calculates the number of books and average rating for each genre and plots these data on a bar chart.

## Author Popularity Analysis

The `author_popularity_analysis.py` script fetches book data from the Google Books API based on user-provided author queries. It then calculates the number of books and average rating for each author and plots these data on a bar chart.

## Language Analysis

The `language_analysis.py` script fetches book data from the Google Books API based on user-provided language codes. It then calculates the number of books for each language and plots these data on a bar chart.

## Usage

To run these scripts, you need Python installed on your machine. You can run a script by navigating to the directory containing the script and running the following command in your terminal:




## Library Locator

The library locator script uses the Google Maps API to show the nearest libraries to a given location.

## Usage

To run these scripts, you need Python installed on your machine. You can run a script by navigating to the directory containing the script and running the following command in your terminal:

