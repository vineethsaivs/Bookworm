Documentation


using_BERT.py:

A step-by-step explanation of the code:

1. The script imports necessary modules. `requests` for making HTTP requests, `pandas` for data manipulation, `torch` for tensor computations, `transformers` for loading pre-trained models and tokenizers, `sklearn` for data splitting and label encoding.

2. It defines an API key, a search query, and a URL for the Google Books API.

3. It sends a GET request to the Google Books API and converts the response to JSON.

4. It extracts the title, description, and first category of each book in the response data and appends them to a list.

5. It converts the list of books to a DataFrame and combines the title and description into a single text feature.

6. It encodes the category labels to integers using a LabelEncoder.

7. It loads a pre-trained BERT tokenizer and model from the transformers library. The number of labels in the model is set to the number of unique categories in the data.

8. It splits the data into training and testing sets.

9. It tokenizes the text data and pads or truncates it to a maximum length of 512 tokens.

10. It defines a custom dataset class that inherits from `torch.utils.data.Dataset`. The class takes the tokenized encodings and labels as input and returns a dictionary of tensors for each item.

11. It creates instances of the custom dataset class for the training and testing data.

12. It initializes an optimizer.

13. It creates data loaders for the training and testing datasets.

14. It checks if a GPU is available and moves the model to the GPU if it is. It then sets the model to training mode.

15. It trains the model for a specified number of epochs. For each batch in the training data, it moves the batch tensors to the right device, performs a forward pass, computes the loss, performs a backward pass, updates the weights, and resets the gradients.

16. After training, it saves the trained model to a directory named 'my_model'.




fetch_book_descriptions.py

This script is used to fetch book descriptions from the Google Books API for different genres and save them as text files. Here's a step-by-step explanation:

1. The `requests` and `os` modules are imported. `requests` is used for making HTTP requests, and `os` is used for interacting with the operating system.

2. The base URL for the Google Books API is defined.

3. A list of book genres is defined.

4. The script checks if a directory named 'text_files' exists. If it doesn't, the script creates it. This directory is where the book descriptions will be saved.

5. The script then loops over each genre in the list of genres.

6. For each genre, it defines search parameters for the Google Books API. It's searching for books with the genre in the title and limits the results to 3 books.

7. It sends a GET request to the Google Books API with these parameters.

8. The response from the API is parsed as JSON.

9. The script then loops over each item in the response data. Each item represents a book.

10. For each book, it tries to get the title and description from the 'volumeInfo' field.

11. It then saves the description as a text file in the 'text_files' directory. The filename is the title of the book.

12. If the 'volumeInfo' field does not contain a 'title' or 'description' key, the script catches the KeyError and continues with the next book.

In summary, this script fetches book descriptions from the Google Books API for a list of genres and saves each description as a text file.




rank_files.py

A step-by-step explanation of the code:

1. The `glob`, `torch`, `transformers`, and `html` modules are imported. `glob` is used for file path manipulation, `torch` is used for tensor computations, `transformers` is used for loading pre-trained models and tokenizers, and `html` is used for escaping HTML characters.

2. The script loads a pre-trained BERT model for sequence classification and its corresponding tokenizer from the transformers library.

3. It opens a file named 'criteria.txt', reads its content, and stores it in the variable `criteria`.

4. The `criteria` text is tokenized using the loaded tokenizer. The tokenized criteria is truncated to a maximum length of 256 tokens and converted into PyTorch tensors.

5. The script uses `glob` to get a list of all text files in the 'text_files' directory and stores it in the variable `text_files`.

6. It initializes an empty list `relevance_scores` to store the relevance scores of the text files.

7. The script then loops over each text file in `text_files`.

8. For each text file, it opens the file, reads its content, and stores it in the variable `text`.

9. The `text` is then tokenized using the same tokenizer as before. The tokenized text is truncated to a maximum length of 256 tokens and converted into PyTorch tensors.

The cursor is currently at line 18, which is the start of the loop that processes each text file. The next steps would involve combining the tokenized criteria and text, feeding them to the model, and computing the relevance scores.



