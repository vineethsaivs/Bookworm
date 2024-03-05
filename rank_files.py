import glob
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertModel, BertTokenizer, BertForSequenceClassification
from html import escape

# Load the model and the tokenizer
model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased')
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

# Load the criteria
with open('criteria.txt', 'r') as file:
    criteria = file.read()

# Tokenize the criteria
criteria_encoding = tokenizer(criteria, truncation=True, max_length=256, return_tensors='pt')

# Get the list of text files
text_files = glob.glob('text_files/*.txt')

# Initialize a list to store the relevance scores
relevance_scores = []

# Loop over the text files
for text_file in text_files:
    # Load the text file
    with open(text_file, 'r') as file:
        text = file.read()

    # Tokenize the text
    file_encoding = tokenizer(text, truncation=True, max_length=256, return_tensors='pt')

    # Combine the criteria encoding and the file encoding
    combined_encoding = {key: torch.cat([criteria_encoding[key], file_encoding[key]], dim=1) for key in criteria_encoding}

    # Feed the combined encoding to the model
    with torch.no_grad():
        outputs = model(**combined_encoding)

    # Get the logits for the 'relevant' class (assuming it's class 1)
    logits = outputs.logits[:, 1]

    # Take the sigmoid to get the relevance score
    relevance_score = torch.sigmoid(logits).item()
    relevance_scores.append(relevance_score)

# Pair the filenames with their relevance scores and sort by score
ranked_files = sorted(zip(text_files, relevance_scores), key=lambda x: x[1], reverse=True)

# Select the top 3 files
top_files = ranked_files[:3]

# Print the filenames and relevance scores of the top 3 files
for filename, score in top_files:
    print(f"Filename: {filename}, Relevance Score: {score}")

# Load the model and the tokenizer for interpretation
# model = BertModel.from_pretrained('bert-base-uncased', output_attentions=True)
model = BertForSequenceClassification.from_pretrained('./my_model', output_attentions=True)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Initialize an HTML string
# Initialize an HTML string
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Top Files and Their Relevance Scores</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
    </style>
</head>
<body>
    <h1>Top Files and Their Relevance Scores</h1>
    <table>
        <tr>
            <th>Filename</th>
            <th>Relevance Score</th>
        </tr>
"""

# Add the filenames and their relevance scores to the HTML string
for filename, score in top_files:
    html += f"""
    <tr>
        <td>{escape(filename)}</td>
        <td>{score}</td>
    </tr>
    """

html += """
    </table>
    <h1>Top Words and Their Attention Weights</h1>
    <table>
        <tr>
            <th>Word</th>
            <th>Attention Weight</th>
        </tr>
"""

# # Add a section header for the top words and their attention weights
# html += """
# <h1>Top Words and Their Attention Weights</h1>
# """

# Loop over the top 3 files
for filename, score in top_files:

    # Add a section header for the file
    html += f"""
    <h2>{escape(filename)}</h2>
    <table>
    """


    # Load the text file
    with open(filename, 'r') as file:
        text = file.read()

    # Tokenize the text
    inputs = tokenizer(text, return_tensors='pt')

    # Feed the inputs to the model
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the attention weights
    attentions = outputs.attentions

    # Sum the attention weights across all heads
    summed_attentions = torch.sum(attentions[-1], dim=1)

    # Flatten the summed_attentions tensor
    flattened_attentions = summed_attentions.view(-1)

    # Get the indices of the top 10 most attended to tokens
    top_tokens = torch.topk(flattened_attentions, 10).indices

    # Get the values of the top 10 most attended to tokens
    top_values = torch.topk(flattened_attentions, 10).values

    # Decode the top tokens and their corresponding values
    top_words_and_values = [(tokenizer.convert_ids_to_tokens(token_id.item()), value.item()) for token_id, value in zip(top_tokens, top_values)]

    # Add the top words and their values to the HTML string
    for word, value in top_words_and_values:
        html += f"""
        <tr>
            <td>{escape(word)}</td>
            <td>{value}</td>
        </tr>
        """

    # Close the table
    html += """
    </table>
    """

# Close the HTML tags
html += """
    </table>
</body>
</html>
"""

# Write the HTML string to a file
with open('results.html', 'w') as file:
    file.write(html)


