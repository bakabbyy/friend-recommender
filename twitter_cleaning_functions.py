
def clean_text_one(docs):
    """
    Cleans tweet text so that it is in a form suitable for topic modeling.
    ---
    :param docs: Series of documents to be processed.
    :return: Series of processed texts.
    """

    # remove URLs and hyperlinks
    text_nourl = lambda x: re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                                  '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', x)

    # remove @ names
    text_noname = lambda x: re.sub('(@[A-Za-z0-9_]+)', '', x)

    # remove hashtags
    text_nohash = lambda x: re.sub('(#[A-Za-z0-9_]+)', '', x)

    # remove numbers
    text_nonum = lambda x: re.sub(r'\d+', '', x)

    # remove the new line character
    text_nonewline = lambda x: re.sub('\n', '', x)

    # remove punctuation
    text_nopunct = lambda x: ''.join([char for char in x if char not in string.punctuation])

    # convert all letters to lowercase
    text_lower = lambda x: x.lower()

    # substitute multiple spaces with single space
    text_nospaces = lambda x: re.sub(r'\s+', ' ', x, flags=re.I)

    # remove all single characters
    text_single = lambda x: re.sub(r'\s+[a-zA-Z]\s+', ' ', x)

    # apply all cleaning functions to input text
    for clean_func in [text_nourl, text_noname, text_nohash, text_nonum, text_nonewline, \
                       text_nopunct, text_lower, text_nospaces, text_single]:
        docs = docs.map(clean_func)

    return docs


def clean_text_two(docs):
    """
    ---
    :param docs: Pandas series of texts to pre-process.
    :return: Pandas series of cleaned text.
    """

    # remove repeating letters
    counter = 0
    ascii_lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                      'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # replace 'aaaaaaaahhhhh' with 'aahh'
    for letter in ascii_lowercase:
        for row_idx, doc in enumerate(docs):
            for word_idx, word in enumerate(doc):
                original_word = word
                while word != word.replace(letter*3, letter*2):
                    word = word.replace(letter*3, letter*2)
                    docs[row_idx][word_idx] = word
    return docs


def clean_text_three(docs):
    """
    ---
    :param docs: Pandas series of texts to pre-process.
    :return: Pandas series of cleaned text.
    """
    # Setting standard english stopwords + custom stopwords
    STOPWORDS = set(stopwords.words('english'))
    STOPWORDS.remove("not")
    stop_words = ['samsung', 'samsungs', 'galayxs', 'galaxy', 's ', ' s', 'plus', 'ultra', 'z', 'flip', 'unpacked']

    clean_text = []
    for tweet in docs:
        new_tweet = []
        for word in tweet.split():
            if (word not in STOPWORDS) and (word not in stop_words) and (word not in string.punctuation):
                new_tweet.append(word)
        clean_text.append(' '.join(new_tweet))

    return clean_text


def clean_text_four(docs):
    """
    Cleans tweet text so that it is in a form suitable for topic modeling.
    ---
    :param docs: Series of documents to be processed.
    :return: Series of processed texts.
    """

    # lemmatize tweets
    wordNetLemmatizer = WordNetLemmatizer()

    lemmatized_tweets = []
    for text in docs:
        try:
            lemmatized_tweets.append(wordNetLemmatizer.lemmatize(text))
        except:
            pass

    return lemmatized_tweets