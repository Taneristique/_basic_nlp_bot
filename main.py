# This is an educational project which is done to understand the nlp based ai systems
from typing import final

import spacy
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from spacy import tokenizer
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer

Token:final=os.getenv('Token')
BOT_USERNAME=os.getenv('botUserName')
nlp = spacy.load('en_core_web_sm')
stopwords = spacy.lang.en.stop_words.STOP_WORDS

information: str = ("Command parameters\n"
                    "1. edu parameters: \nbag of words\nstopwords\nlemmatation\n "
                    "Commands:\n"
                    "/start meet with bot"
                    "/help shows help menu \n "
                    "/edu params takes one of the options given in edu parameters and explains it\n"
                    "/bow takes bag of words and a corpus in english than converts them to vectors\n"
                    "/stopw takes a text in english and removes stopwords in the text\n"
                    "/lemma lemmatates given input by user however input should be in english\n"

                    )
bow_description = """
Bag of Words (BoW) Model Description:

The Bag of Words model is a common technique in Natural Language Processing (NLP). It represents a document as an unordered set of words, disregarding grammar and word order but keeping track of word frequency.

Example sentences:
- "I love natural language processing."
- "Natural language processing is fascinating."

Step 1: Tokenization
Break down each sentence into individual words or tokens.

Step 2: Vocabulary Creation
Create a unique set of words from the entire collection of documents. This set forms the vocabulary of the model.

Step 3: Feature Extraction
Represent each document as a vector, where each element corresponds to the frequency of a word in the vocabulary.

Important Considerations:
- Word Order is ignored.
- Sparse Representation: Vectors are often sparse, with most elements being zero.
- Frequency Information is retained, but sequence information is lost.

The Bag of Words model is a foundational concept used in text analysis tasks such as sentiment analysis, text classification, and document clustering.
"""
stopwords_description = """
Stopwords are common words in a language that are often removed from text during natural language processing to focus on more meaningful words. These words, such as 'the,' 'and,' and 'is,' carry little semantic value on their own and don't contribute significantly to the meaning of a sentence. By filtering out stopwords, we can highlight the essential content and improve the efficiency of text analysis algorithms. In your Telegram bot, recognizing and handling stopwords can enhance the accuracy and relevance of language-based tasks.
"""
lemmatization_description = """
Lemmatization is a linguistic process used in Natural Language Processing (NLP) to reduce words to their base or root form, known as the lemma. Unlike stemming, which simply chops off prefixes or suffixes, lemmatization considers the context and meaning of a word. 

For example, the lemma of 'running' is 'run,' and the lemma of 'better' is 'good.' Lemmatization helps standardize words, making it easier to analyze and understand text by treating different forms of a word as the same. In your Python project, incorporating lemmatization can enhance the accuracy of language-based tasks such as text classification and sentiment analysis.
"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'Hi there,my name is {BOT_USERNAME} and I am here to help you on nlp related topics 😊')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Help Menu: \n {information}')


async def lemmatation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = text.lower()
    doc = nlp(text.replace('/lemma', ''))
    lemmas = [token.lemma_ for token in doc if token.text.isalpha() and token not in stopwords]
    processed_output = str([lemmas[i] for i in range(1, len(lemmas))])
    await update.effective_message.reply_text(processed_output)


async def remove_stopwords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = text.lower()
    doc = nlp(text.replace('/stopw', ''))
    tokens = [tokens.text for tokens in doc if tokens.text.isalpha() and tokens not in stopwords]
    await update.effective_message.reply_text(tokens)


async def bag_of_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = text.replace('/bow', '')
    text = text.lower()
    text1 = []
    text2 = []
    if len(text) > 30:
        print(text)
        doc = nlp(text)
        tokens = [token.text for token in doc if token.text.isalpha() and token not in stopwords]
        corpus = createCorpus(text)
        text1 = [tokens[i] for i in range(0, 30)]
        count = 0
        bow = []
        for i in range(len(corpus)):
            for j in range(len(text1)):
                if corpus[i] == tokens[j]:
                    count += 1
            bow.append(count)
            count = 0
        bow2 = []
        count1 = 0
        text2 = [tokens[i] for i in range(30, len(tokens))]
        for i in range(len(corpus)):
            for j in range(len(text2)):
                if corpus[i] == tokens[j]:
                    count1 += 1
            bow2.append(count1)
            count1 = 0
        await  update.effective_message.reply_text(
            f'User input : {text} \n first sentence : {text1} \n second input :{text2}\nCorpus : {corpus}\nMachine readable bow data for first sentence:{bow} \nMachine readable data for second sentence: {bow2}')
    else:
        await update.message.reply_text('Given text must contain more than 30 words to use this functionality')


def search(text, word):
    flag = False
    for t in text:
        if t == word:
            return True
        else:
            flag = False
    return flag


def createCorpus(text):
    corpus = []
    doc = nlp(text)
    vocabularies = [token.text for token in doc if token.text.isalpha() and token not in stopwords]
    print(vocabularies)
    for word in vocabularies:
        if search(text, word):
            continue
        else:
            corpus.append(word)
    return corpus


def education_params(txt: str):
    processed = txt.lower()
    if 'bag of words' in processed:
        return bow_description
    elif 'stopwords' in processed:
        return stopwords_description
    elif 'lemmatation' in processed:
        return lemmatization_description


async def education(update: Update, context: ContextTypes):
    txt = update.message.text
    response = education_params(txt)
    await update.effective_message.reply_text(response)


async def error(update: Update, context: ContextTypes):
    text = update.message.text
    await update.message.reply_text(f"Following Input '{text}' is caused an error : {context.error}")


if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(Token).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('edu', education))
    app.add_handler(CommandHandler('lemma', lemmatation))
    app.add_handler(CommandHandler('stopw', remove_stopwords))
    app.add_handler(CommandHandler('bow', bag_of_words))
    app.add_error_handler(error)
    app.run_polling(poll_interval=1)

