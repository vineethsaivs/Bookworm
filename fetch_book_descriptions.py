# import requests
# import os

# # Define the base URL for the Google Books API
# base_url = "https://www.googleapis.com/books/v1/volumes"

# # Define the search parameters
# params = {
#     "q": "intitle:philosophy",
#     "maxResults": 15
# }

# # Send a GET request to the Google Books API
# response = requests.get(base_url, params=params)

# # Parse the response as JSON
# data = response.json()

# # Create the text_files directory if it doesn't exist
# if not os.path.exists('text_files'):
#     os.makedirs('text_files')

# # Loop over the items in the data
# for item in data['items']:
#     try:
#         # Get the title and description
#         title = item['volumeInfo']['title']
#         description = item['volumeInfo']['description']

#         # Save the description as a text file
#         with open(f'text_files/{title}.txt', 'w') as file:
#             file.write(description)
#     except KeyError:
#         continue


import requests
import os

# Define the base URL for the Google Books API
base_url = "https://www.googleapis.com/books/v1/volumes"

# Define the genres
genres = ["philosophy", "history", "science", "literature", "art"]

# Create the text_files directory if it doesn't exist
if not os.path.exists('text_files'):
    os.makedirs('text_files')

# Loop over the genres
for genre in genres:
    # Define the search parameters
    params = {
        "q": f"intitle:{genre}",
        "maxResults": 3
    }

    # Send a GET request to the Google Books API
    response = requests.get(base_url, params=params)

    # Parse the response as JSON
    data = response.json()

    # Loop over the items in the data
    for item in data['items']:
        try:
            # Get the title and description
            title = item['volumeInfo']['title']
            description = item['volumeInfo']['description']

            # Save the description as a text file
            with open(f'text_files/{title}.txt', 'w') as file:
                file.write(description)
        except KeyError:
            continue


