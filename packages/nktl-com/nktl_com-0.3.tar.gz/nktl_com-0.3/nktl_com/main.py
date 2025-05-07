def hello():
    print("""
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

#tokenize
sentence = "SASTRA University is a great place. It has amazing facilities!"
words=nltk.word_tokenize(sentence)
print(words)

#stopwords removal
stop_words = set(stopwords.words('english'))
words_1=[word for word in words if word not in stop_words]
print(words_1)

#punctuation removal
words_2= [word for word in words_1 if word not in string.punctuation]
print(words_2)

# stemming
stemmer = PorterStemmer()
words_3 = [stemmer.stem(word) for word in words_2]
print(words_3)

# lemmatization
lemmatizer = WordNetLemmatizer()
words_4 = [lemmatizer.lemmatize(word) for word in words_3]
print(words_4) 

text = "Barack Obama was the 44th President of the United States."
p_tag = pos_tag(word_tokenize(text))
p_tag

n_entity = ne_chunk(p_tag)
print(n_entity)

---------------------------------------------------------------------------------------------------------------------------------
Exp 2
import pandas as pd
import numpy as np
import math
from collections import Counter
          
df = pd.read_csv('exp2.csv', header = None)
df.head()
          
Sentences=df[0].values
Sentences[:5]
          
unigram = Counter()
bigrams = Counter()
          
for sent in Sentences:
  tokens = sent.lower().split()
  unigram.update(tokens)
  for i in range(len(tokens)-1):
    bigram = (tokens[i],tokens[i+1])
    bigrams[bigram] += 1

print(unigram)
print(bigrams)
          
word1 = 'Sastra'.lower()
word2 = 'University'.lower()
N = sum(unigram.values())
          
cw1 = unigram[word1]
cw2 = unigram[word2]
expected = cw1*cw2/N**2
variance = expected
observed = bigrams[(word1,word2)]/N
t = (observed - expected)/math.sqrt(variance/N)
t
          
c11 = c12 = c21 = c22 = 0
for unit in bigrams:
  if unit[0] == word1 and unit[1] == word2:
    c11 += 1
  if unit[0] == word1 and unit[1] != word2:
    c12 += 1
  if unit[0] != word1 and unit[1] == word2:
    c21 += 1
  if unit[0] != word1 and unit[1] != word2:
    c22 += 1

t13 = c11 + c12
t23 = c21 + c22
t31 = c11 + c21
t32 = c12 + c22
tot = t31 + t32

e11 = t13*t31/tot
e12 = t13*t32/tot
e21 = t23*t31/tot
e22 = t23*t32/tot

obs = [c11, c12, c21, c22]
exp = [e11, e12, e21, e22]

chi2 = 0

for i in range(4):
  chi2 += (obs[i]-exp[i])**2/exp[i]

print(chi2)
----------------------------------------------------------------------------------------------
EXP 3  WSD
           
import pandas as pd
import numpy as np
          
df = pd.read_csv("dataxx.csv")
df.head()
          
train_sent = df['context_sentence'].values
label = df['sense'].values

print(train_sent[:2])
print(label[:2])
          
sent_count = {

    'financial_institution': 0,
    'river_side': 0
}

word_count = {

    'financial_institution':{},
    'river_side': {}

}
vocab = set()
          
for sent,label in zip(train_sent, label):
  sent_count[label] += 1
  words = sent.lower().split()
  for word in words:
    vocab.add(word)
    word_count[label][word] = word_count[label].get(word,0) + 1


print(sent_count)
print(word_count)
          
import math
sent = "I went to the bank for paycheck"
          
log_probs = {
    'financial_institution': 0,
    'river_side': 0
}

for label in ['financial_institution', 'river_side']:
    log_probs[label] = math.log(sent_count[label] / sum(sent_count.values()))
    for word in test_sentence.lower().split():
        numerator = word_count[label].get(word, 0) + 1
        denominator = sent_count[label] + len(vocab)
        log_probs[label] += math.log(numerator / denominator)

print("\nLog probabilities:")
print(log_probs)

predicted_class = ('Financial institution' if log_probs['financial_institution'] > log_probs['river_side'] else 'River side')
print(f"\nPredicted sense: {predicted_class}")
          
""")
    
def hello2():
    print("""
    hinddle  rooth 
          
          from collections import Counter
          import pandas as pd
import numpy as np
import math
from collections import Counter
          
df = pd.read_csv('exp2.csv', header = None)
df.head()
          
Sentences=df[0].values
Sentences[:5]
          unigram = Counter()
bigrams = Counter()
          
          for sent in sentences:
  token = sent.lower().split()
  unigram.update(token)
  for i in range(len(token)-1):
    bigram = (token[i], token[i+1])
    bigrams[bigram] += 1
print(unigram)
print(bigrams)
          
          noun = "her".lower()
verb = "running".lower()
prep = "with".lower()
          
p_noun_prep = bigram_dict[(noun, prep)] / unigram_dict[noun] if unigram_dict[noun] != 0 else 0
p_verb_prep = bigram_dict[(verb, prep)] / unigram_dict[verb] if unigram_dict[verb] != 0 else 0
p_0_n = 1 - p_noun_prep
          
          if p_noun_prep > 0:
    if lam>0:
    print("verb")
  if lam<0:
    print("noun")

else:
    print("No valid attachments.")
          
-----------------------------------------------------------------------------------------------------------
          exp HMM

          import numpy as np
Tp = {
    'Sunny': {'Sunny': 0.7, 'Rainy': 0.3},  # Probabilities from Sunny
    'Rainy': {'Sunny': 0.5, 'Rainy': 0.5}   # Probabilities from Rainy
}

Ep = {
    'Sunny': {'Walk': 0.6, 'Shop': 0.1, 'Clean': 0.3},  # Probabilities of observations from Sunny
    'Rainy': {'Walk': 0.1, 'Shop': 0.7, 'Clean': 0.2}   # Probabilities of observations from Rainy
}

observations = ['Clean', 'Shop','Walk']

Initial_prob = [1, 0]
          
           #FORWARD PROCEDURE

alpha = np.zeros((len(Tp), len(observations)+1))
alpha[:,0] = Initial_prob

for i in range(1, len(observations)+1):
  alpha[0][i] = alpha[0][i-1]*Tp['Sunny']['Sunny']*Ep['Sunny'][observations[i-1]] + alpha[1][i-1]*Tp['Rainy']['Sunny']*Ep['Rainy'][observations[i-1]]
  alpha[1][i] = alpha[1][i-1]*Tp['Rainy']['Rainy']*Ep['Rainy'][observations[i-1]] + alpha[0][i-1]*Tp['Sunny']['Rainy']*Ep['Sunny'][observations[i-1]]

alpha
#BACKWARD PROCEDURE

beta = np.zeros((len(Tp), len(observations)+1))
beta[:,len(observations)] = [1,1]

for i in range(len(observations)-1, -1, -1):
  beta[0][i] = beta[0][i+1]*Tp['Sunny']['Sunny']*Ep['Sunny'][observations[i]] + beta[1][i+1]*Tp['Sunny']['Rainy']*Ep['Sunny'][observations[i]]
  beta[1][i] = beta[1][i+1]*Tp['Rainy']['Rainy']*Ep['Rainy'][observations[i]] + beta[0][i+1]*Tp['Rainy']['Sunny']*Ep['Rainy'][observations[i]]

beta
          
          #VITERBI

delta = np.zeros((len(Tp), len(observations)+1))
delta[:,0] = Initial_prob
Best_state1 = []
Best_state2 = []

for i in range(1, len(observations)+1):
  s_s = delta[0][i-1]*Tp['Sunny']['Sunny']*Ep['Sunny'][observations[i-1]]
  r_s = delta[1][i-1]*Tp['Rainy']['Sunny']*Ep['Rainy'][observations[i-1]]
  Best_state1.append("Sunny" if s_s>= r_s else "Rainy")
  delta[0][i] = max(s_s , r_s)
  r_r = delta[1][i-1]*Tp['Rainy']['Rainy']*Ep['Rainy'][observations[i-1]]
  s_r = delta[0][i-1]*Tp['Sunny']['Rainy']*Ep['Sunny'][observations[i-1]]
  Best_state2.append("Rainy" if r_r>= s_r else "Sunny")
  delta[1][i] = max(r_r , s_r)

Best_state_sequence = [Best_state1,Best_state2]
delta
          

          print(Best_state_sequence)

----------------------------------------------------------------------------------
          PCFG

          from nltk import PCFG, InsideChartParser
grammar = PCFG.fromstring(""S -> NP VP [1.0]
NP -> NP PP [0.4] | 'he' [0.1] | 'dessert' [0.3] | 'lunch' [0.1] | 'saw' [0.1]
"")
parser = InsideChartParser(grammar)
tokens = "he saw lunch with dessert".split()
for tree in parser.parse(tokens):
    tree.pretty_print()
    print("PROBABILITY: ",tree.prob())
    tree.draw()

          
          def cyk_parse(sentence, grammar):
    n = len(sentence)
    table =np.empty((n, n), dtype=object) 
    for i, word in enumerate(sentence): 
        table[i, i] = [(p.lhs(), p.prob()) for p in grammar.productions() if len(p.rhs()) == 1 and p.rhs()[0] == word] 
    for span in range(2, n + 1): 
        for i in range(n - span + 1): 
            table[i, i + span - 1] = [(p.lhs(), lp * rp * p.prob()) for k in range(i, i + span - 1) 
                for l, lp in (table[i, k] or []) for r, rp in (table[k + 1, i + span - 1] or []) 
                for p in grammar.productions() if len(p.rhs()) == 2 and (l, r) == p.rhs()] 
    return table
table = cyk_parse(sentence,cnf_grammar)
r,p=table[0][2][0]
if str(r)=='S': print("Accepted -",p)
else: print("Not Accepted -",p)
          
    """)


def hello3():
    print("""
    exp 8 bow tfidf
          # Import necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset with standard pd.read_csv()
try:
    df = pd.read_csv('TweetSentimentAnalysis.csv')
    print("Dataset loaded successfully. First 5 rows:")
    print(df.head())
except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
    exit()
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    exit()

# Data cleaning
print("\nChecking for missing values:")
print(df.isnull().sum())

# Drop rows with NaN values in 'text' column
df_cleaned = df.dropna(subset=['text'])
print(f"\nOriginal shape: {df.shape}, Cleaned shape: {df_cleaned.shape}")

# Separate features and target variable
X = df_cleaned['text']
y = df_cleaned['sentiment']

# Split the data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Maintain class distribution
)
print(f"\nTraining samples: {len(X_train)}, Test samples: {len(X_test)}")

def perform_text_analysis(X_train, X_test, y_train, y_test):
    ""Perform text analysis using BOW and TF-IDF approaches""
    
    # 1. Bag-of-Words (BOW) Implementation
    bow_vectorizer = CountVectorizer(
        max_features=5000,  # Limit vocabulary size
        stop_words='english'  # Remove common English words
    )
    X_train_bow = bow_vectorizer.fit_transform(X_train)
    X_test_bow = bow_vectorizer.transform(X_test)
    
    # BOW Model Training
    model_bow = MultinomialNB()
    model_bow.fit(X_train_bow, y_train)
    y_pred_bow = model_bow.predict(X_test_bow)
    accuracy_bow = accuracy_score(y_test, y_pred_bow)
    
    # 2. TF-IDF Implementation
    tfidf_vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2)  # Include bigrams
    )
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)
    
    # TF-IDF Model Training
    model_tfidf = MultinomialNB()
    model_tfidf.fit(X_train_tfidf, y_train)
    y_pred_tfidf = model_tfidf.predict(X_test_tfidf)
    accuracy_tfidf = accuracy_score(y_test, y_pred_tfidf)
    
    # Results Comparison
    print("\nModel Performance Comparison:")
    print(f"BOW Accuracy: {accuracy_bow:.4f}")
    print(f"TF-IDF Accuracy: {accuracy_tfidf:.4f}")
    
    # Detailed TF-IDF Report
    print("\nTF-IDF Classification Report:")
    print(classification_report(y_test, y_pred_tfidf, digits=4))
    
    # Confusion Matrix Visualization
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred_tfidf)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=model_tfidf.classes_,
                yticklabels=model_tfidf.classes_)
    plt.title("TF-IDF Model Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.show()

# Execute the analysis
perform_text_analysis(X_train, X_test, y_train, y_test)

--------------------------------------------------------------------------------------------
          w2vect
           # Import required libraries
from gensim.models import Word2Vec  
from nltk import word_tokenize      
import pandas as pd                 
import nltk                        
nltk.download('punkt')

df = pd.read_csv("datax.csv") 
df  

sentences = df['text'].to_list()

tokenized_sent = [word_tokenize(sent.lower()) for sent in sentences]  

tokenized_sent 

    # Initialize and train Word2Vec model
model = Word2Vec(
    sentences=tokenized_sent, 
    vector_size=100,        
    min_count=1,               # Ignore words with frequency < 1
    window=5,                  # Maximum distance between current and predicted word
    workers=4,                 # Number of CPU cores to use
)


print("Word vector for 'Python' (first 6 dimensions):")
print(model.wv['Python'][:6])  # wv = word vectors property


sim = model.wv.most_similar("Python", topn=5) 
print("\nMost similar words to 'Python':")
for word, similarity in sim:
    print(f"{word}: {similarity:.4f}") 

-----------------------------------------------------------------------------------------
          LSTM

          import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


df = pd.read_csv("dataset.csv")
headlines = df['headline'].values 
print("Sample headlines:", headlines[:5])

tokenizer = Tokenizer()
tokenizer.fit_on_texts(headlines)
total_words = len(tokenizer.word_index) + 1 

sequences = tokenizer.texts_to_sequences(headlines)
print("Sample sequences:", sequences[:5]) 

# Prepare training data (X = input sequences, y = next word to predict)
input_sent = [seq[:-1] for seq in sequences] 
y = [seq[-1] for seq in sequences] 


max_sequence_len = max(len(seq) for seq in input_sent)
X = pad_sequences(input_sent, maxlen=max_sequence_len)
y = np.array(y)

# Define LSTM model architecture
model = Sequential([
    # LSTM layer with 150 memory units
    LSTM(150, input_shape=(max_sequence_len, 1)),  

    Dense(total_words, activation="softmax")  
])


model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy', 
    metrics=['accuracy']
)

# Reshape input for LSTM (samples, timesteps, features) and train
model.fit(
    X.reshape(X.shape[0], X.shape[1], 1), 
    y, 
    epochs=30,
    verbose=1  # Show progress bar
)

# Text generation setup
num_words_to_generate = 5
seed_text = "The cat "
generated_text = seed_text

print(f"\nGenerating text starting with: '{seed_text}'")

# Generate words one at a time
for _ in range(num_words_to_generate):
    token_list = tokenizer.texts_to_sequences([generated_text])[0]
    padded_sequence = pad_sequences([token_list], maxlen=max_sequence_len)
    predicted = model.predict(padded_sequence.reshape(1, max_sequence_len, 1))
    predicted_word_idx = np.argmax(predicted)
    predicted_word = tokenizer.index_word[predicted_word_idx]
    generated_text += " " + predicted_word
    print(f"Generated so far: {generated_text}")

print("\nFinal generated text:", generated_text)

----------------------------------------------------------------------------------------------------------------
          RNN  translate

import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.optimizers import Adam
          
          english_sentences = ["hello how are you", "i love programming", "good morning", "thank you"]
french_sentences = ["bonjour comment allez vous", "j'aime la programmation", "bonjour", "merci"]

          # Tokenize
eng_tokenizer = Tokenizer()
fra_tokenizer = Tokenizer()
eng_tokenizer.fit_on_texts(english_sentences)
fra_tokenizer.fit_on_texts(french_sentences)
          
          X = pad_sequences(eng_tokenizer.texts_to_sequences(english_sentences))
y = pad_sequences(fra_tokenizer.texts_to_sequences(french_sentences))
          
          # Reshape X for RNN input
X = X.reshape(X.shape[0], X.shape[1], 1)
          
          model = Sequential([
    SimpleRNN(32, return_sequences=True, input_shape=(X.shape[1], 1)),
    Dense(len(fra_tokenizer.word_index) + 1, activation='softmax')
])
model.compile(optimizer=Adam(learning_rate=0.01), metrics=['accuracy'], loss='sparse_categorical_crossentropy')
model.fit(X, y, epochs=20)

          
          def translate(text):
    sequence = pad_sequences(eng_tokenizer.texts_to_sequences([text]), maxlen=X.shape[1])
    prediction = model.predict(sequence.reshape(1, X.shape[1], 1))[0]
    return ' '.join([fra_tokenizer.index_word[i] for i in np.argmax(prediction.reshape(-1, len(fra_tokenizer.word_index) + 1), axis=1) if i != 0])

# Test
print("\nTranslations:")
for text in ["hello how are you", "good morning"]:
    print(f"English: {text}")
    print(f"French: {translate(text)}\n")
          
""")