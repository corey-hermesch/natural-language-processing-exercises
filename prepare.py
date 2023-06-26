## IMPORTS
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import numpy as np
import pandas as pd

import acquire as a

np.random.seed(42)

## FUNCTIONS
def basic_clean(article):
    """
    This function will perform basic text cleaning on the given article.
    
    Args:
        article (str): The text to be cleaned.

    Returns:
        str: The cleaned article.

    The function applies the following steps to clean the text:
    1. Converts the article to lowercase.
    2. Normalizes the text by removing inconsistencies in unicode character encoding.
    3. Converts all characters to ASCII characters, dropping any characters that cannot be converted.
    4. Removes any characters that are not letters, numbers, whitespace, or a single quote.

    Example:
        article = "Hello, World! This is an example article."
        cleaned_article = basic_clean(article)
        print(cleaned_article)
        # Output: "hello world this is an example article"
    """
    # make all text lower case
    article = article.lower()
    # ensure text is "normalized" (remove inconsistincies in unicode character encoding)
    # AND make all characters ASCII characters, ignoring any errors in conversion (i.e. drop those chars)
    article = unicodedata.normalize('NFKD', article).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    # making hyphenated words into two words separated by a space, using positive look behind and pos look ahead
    article = re.sub(r'(?<=\w)-(?=\w)', ' ', article)
    # drop anything that is not a letter, number, whitespace, or a single quote
    article = re.sub(r"[^a-z0-9\s']", '', article)

    return article

#defining a function to perorm tokenization of the passed string value, article
def tokenize (article):
    """
    This function will
    - accept a string, article which has been processed with basic_clean
    - use nltk.tokenize.ToktokTokenizer to break words and any punctuation left over into discrete units
    - returns processed string
    """
    # make the tokenizer object
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # use tokenizer object to tokenize the article
    article = tokenizer.tokenize(article, return_str=True)
    # return tokenized article
    return article

# defining a function to return stems of words utilizing nltk.porter.PorterStemmer
def stem(article):
    """
    This function will
    - accept a string, article that has been processed with basic_clean and tokenize
    - get word stems for each word
    - joins the word stems back together in one string and returns that string
    """
    # create the nltk stemmer object
    ps = nltk.porter.PorterStemmer()
    # use ps to get stems of words
    stems = [ps.stem(word) for word in article.split(' ')]
    # join those words back together and return the string
    return ' '.join(stems)

# defining a function to return roots of words utilizing nltk.stem.WordNetLemmatizer
def lemmatize(article):
    """
    This function will
    - accept a string, article that has been processed with basic_clean and tokenize
    - get word roots for each word using nltk.stem.WordNetLemmatizer
    - joins the word roots back together in one string and returns that string
"""
    # create the wnl lemmatizer object
    wnl = nltk.stem.WordNetLemmatizer()
    # use wnl to get stems of words
    lemmas = [wnl.lemmatize(word) for word in article.split(' ')]
    # join those words back together and return the string
    return ' '.join(lemmas)

# defining a function to remove stopwords
def remove_stopwords(article, extra_words=[], exclude_words=[]):
    """
    This function will
    - accept a string, article
    - accept two optional lists, extra_words and exclude_words
    - remove the stopwords from the string (ex: 'a', 'an', 'the', etc.)
        - however, it will specifically not remove words that are in exclude_words, even if those words are in the 
          default stopwords list
        - additionally, it will also remove any words in extra_words
    - returns the string of non-stopwords
    """
    # get a list of stopwords
    stopword_list = stopwords.words('english')
    # add in the extra words to remove, use | instead of +
    stopword_list = list( set(stopword_list) | set(extra_words) )
    # subtract out the words we don't want to remove
    stopword_list = list( set(stopword_list) - set(exclude_words) )
    # make a list of words in article to iterate on
    words = article.split(' ')
    # only keep words not in stopword_list
    filtered_words = [word for word in words if word not in stopword_list]
    # print (f'Removed {len(words) - len(filtered_words)} stopwords.')
    # join the filtered words back into one string and return it
    return ' '.join(filtered_words)

# FUNCTIIONS to add columns to df containing 'original' content

# defining a function to add a column of text that has been processed by basic_clean
def get_clean_column(df):
    """
    This function will
    - accept a df with at least one column (named 'original') of text to process
    - process the text in each row of that column with the basic_clean function
    - add a column, named 'clean', to the df with processed text
    - return the new df
    """
    df['clean'] = pd.Series([basic_clean(s) for s in df.original])
    df['clean'] = pd.Series([tokenize(s) for s in df.clean])
    df['clean'] = pd.Series([remove_stopwords(s) for s in df.clean])
    
    return df

# defining a function to add a column of text that has been processed by stem
def get_stemmed_column(df):
    """
    This function will
    - accept a df with at least one column (named 'clean') of text to process
    - process the text in each row of that column with the stem function
    - add a column named 'stemmed' to the df with processed text
    - return the new df
    """
    df['stemmed'] = pd.Series([stem(s) for s in df.clean])
    
    return df

# defining a function to add a column of text that has been processed by lemmatize
def get_lemmatized_column(df):
    """
    This function will
    - accept a df with at least one column (named 'clean') of text to process
    - process the text in each row of that column with the lemmatize function
    - add a column named 'lemmatized' to the df with processed text
    - return the new df
    """
    df['lemmatized'] = pd.Series([lemmatize(s) for s in df.clean])
    
    return df