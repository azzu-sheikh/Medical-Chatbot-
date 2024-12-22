import csv
import nltk
import warnings
import openai
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Ignore warnings
warnings.filterwarnings("ignore")

# Load necessary NLTK resources
nltk.download('punkt')  
nltk.download('wordnet')

# Set up your OpenAI API key securely from environment variables
openai.api_key = "your openai api key"

# Load and preprocess chatbot data
def load_chat_data():
    try:
        f = open('chatbot1.txt', 'r', errors='ignore')

        raw = f.read().lower()

        sent_tokens = nltk.sent_tokenize(raw)
        word_tokens = nltk.word_tokenize(raw)

        return sent_tokens, word_tokens
    except Exception as e:
        print(f"Error reading files: {e}")
        return [], []

sent_tokens, word_tokens = load_chat_data()

# Lemmatization and tokenization
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

# Initialize VADER analyzer
analyzer = SentimentIntensityAnalyzer()

# Sentiment analysis function
def analyze_sentiment(user_input):
    scores = analyzer.polarity_scores(user_input)
    compound = scores['compound']  # Compound score ranges from -1 to 1

    if compound > 0.05:
        return "positive"
    elif compound < -0.05:
        return "negative"
    else:
        return "neutral"

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Load the question-answer pairs for medicine from a CSV file
def load_medicine_data():
    medicine_data = []
    try:
        with open('medicine.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row

            for row in csv_reader:
                # Check if row has exactly two columns
                if len(row) == 2:
                    Basic_Q = row[0].strip().lower()
                    Basic_Ans = row[1].strip()
                    medicine_data.append((Basic_Q, Basic_Ans))
                else:
                    print(f"Skipping malformed row: {row}")

    except FileNotFoundError:
        print("Error: medicine.csv file not found.")
    
    return medicine_data

# Function to add a new entry to the medicine.csv file
def add_medicine_entry(user_input):
    if '=' in user_input:
        condition, medicine = user_input.split('=', 1)
        condition = condition.strip()
        medicine = medicine.strip()
        
        # Append the new entry to the CSV file
        try:
            with open('medicine.csv', mode='a', newline='\n') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([condition, medicine])
                return f"New entry added: '{condition}' = '{medicine}'"
        except Exception as e:
            return "There was an error saving the entry."
    else:
        return "Invalid format. Please use 'condition=medicine'."  

# Function for AI-generated responses via OpenAI
def ai_generated_response(user_input):
    try:
        if "ai." not in user_input:
            return "Please use the 'ai.' prefix to get an AI-generated response."

        prompt = user_input.split("ai.", 1)[1].strip()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if available and desired
            messages=[{"role": "system", "content": "You are an assistant providing information based on user input."},
                      {"role": "user", "content": prompt}],
            max_tokens=100  # Limit the response length
        )

        ai_response = response['choices'][0]['message']['content']
        return ai_response

    except Exception as e:
        return "Sorry, I couldn't get an AI response at the moment. Please try again later."

# Function to get a medicine suggestion based on user input
def get_medicine_suggestion(user_input, medicine_data):
    for Basic_Q, Basic_Ans in medicine_data:
        if Basic_Q.lower() in user_input.lower():
            return Basic_Ans
    return None

# Handle greetings and introductions
def greeting(sentence):
    GREETING_INPUTS = ("hello", "hiii", "hii", "hey", "greetings", "sup", "what's up")
    GREETING_RESPONSES = ["hi", "hey", "hii there" , "hello", "I am glad you are talking to me!"]
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def IntroduceMe(sentence):
    Introduce_Ans = [
        "My name is Sanjeevini Bot, your virtual medical assistant.",
        "I'm Sanjeevini Bot, here to assist with your medical inquiries.",
        "Hello! You can call me Sanjeevini Bot. I'm here to help with health-related questions."
    ]
    return random.choice(Introduce_Ans)
    
def process_negation(user_input):
    """
    Remove negated phrases (e.g., 'no cold', 'not a headache') 
    and focus on affirmative statements (e.g., 'I have a fever').
    """
    tokens = user_input.split()
    filtered_tokens = []
    skip_next = False

    for i, word in enumerate(tokens):
        # Check for negation and skip the next token
        if word in ["no", "not"] and i + 1 < len(tokens):
            skip_next = True
        elif skip_next:
            skip_next = False  # Skip the negated token
        else:
            filtered_tokens.append(word)

    return " ".join(filtered_tokens)

# Function to get basic answers from chatbot1.txt and predefined responses
def basic_response(user_input):
    # Tokenize and normalize the user input
    tokens = LemNormalize(user_input)
    
    # Check for a match in chatbot1.txt responses
    for sentence in sent_tokens:
        for token in tokens:
            if token in sentence:  # Match tokens to entries in chatbot1.txt
                return sentence
    
    # Check predefined greeting responses
    greeting_response = greeting(user_input)
    if greeting_response:
        return greeting_response
    
    # Check for introductions
    if "your name" in user_input:
        return IntroduceMe(user_input)
    
    return "I'm sorry, I don't understand. Could you rephrase your question?"


# Main chat function
def chat(user_response):
    user_response = user_response.lower()
    
    if user_response != 'bye':
        # Analyze sentiment
        sentiment = analyze_sentiment(user_response)

        # Handle sentiment-specific messages
        if sentiment == "positive":
            sentiment_message = "It's great to hear that! 😊"
        elif sentiment == "negative":
            sentiment_message = "I'm sorry you're feeling this way. Is there anything I can do to help? 😔"
        else:
            sentiment_message = "Got it. Let's see how I can assist you."

        # Check for "ai." prefix and provide AI-generated response
        if user_response.startswith("ai."):
            return ai_generated_response(user_response)    

        # Check for "med." prefix and retrieve medicine information
        if user_response.startswith("med."):
            condition = user_response.split("med.", 1)[1].strip().lower()
            medicine_suggestion = get_medicine_suggestion(condition, medicine_data)
            if medicine_suggestion:
                return medicine_suggestion
            else:
                return "Sorry, no medicine suggestions found for that condition."

        # Check for the format condition=medicine and add entry to CSV
        if '=' in user_response:
            return add_medicine_entry(user_response)
        
        # Retrieve basic responses from chatbot data
        return basic_response(user_response) + sentiment_message
        
    else:
        return "Bye! Take care."

# Load the medicine data at the start
medicine_data = load_medicine_data()
