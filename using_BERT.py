import requests
import pandas as pd
import torch
from transformers import BertTokenizerFast, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyA3J7SOTWbxxhxnUCgrX3PbGSwP3KadgmA'

# Define the search query
query = "philosophy"

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
        categories = item['volumeInfo']['categories'][0]  # Take the first category
        books.append([title, description, categories])
    except KeyError:
        continue

# Convert the list of books to a DataFrame
df = pd.DataFrame(books, columns=['Title', 'Description', 'Category'])

# Combine the Title and Description into a single text feature
df['text'] = df['Title'] + " " + df['Description']

# Encode the Category labels to integers
le = LabelEncoder()
df['Category'] = le.fit_transform(df['Category'])

# Load the BERT tokenizer and model
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(df['Category'].unique()))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['Category'], test_size=0.2, random_state=42)

# Tokenize the text data
train_encodings = tokenizer(list(X_train), truncation=True, padding=True, max_length=512)
test_encodings = tokenizer(list(X_test), truncation=True, padding=True, max_length=512)

# Create a custom dataset
class BookDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = BookDataset(train_encodings, list(y_train))
test_dataset = BookDataset(test_encodings, list(y_test))

# Initialize the optimizer
# optimizer = AdamW(model.parameters(), lr=1e-5)

# To this
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

# Train the model
from torch.utils.data import DataLoader

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=True)

# Train the model
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)
model.train()

for epoch in range(3):  # number of epochs
    for batch in train_loader:
        # Move the batch tensors to the right device
        batch = {k: v.to(device) for k, v in batch.items()}
        
        # Perform a forward pass
        outputs = model(**batch)
        
        # Compute the loss
        loss = outputs.loss
        
        # Perform a backward pass
        loss.backward()
        
        # Update the weights
        optimizer.step()
        
        # Reset the gradients
        optimizer.zero_grad()

model.save_pretrained('./my_model')
