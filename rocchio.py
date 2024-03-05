import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from itertools import permutations


# download 'stopwords' package
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("stopwords")


from string import punctuation
import re
import math


class Rocchio:

    def __init__(self, relevant_docs, unrelevant_docs, query) -> None:
        """
        relevant_docs: list of str
        unrelevant_docs: list of str
        query: str
        """
        self.num_relevant_docs = len(relevant_docs)
        self.num_unrelevant_docs = len(unrelevant_docs)
        self.relevant_docs = " ".join(relevant_docs)
        self.unrelevant_docs = " ".join(unrelevant_docs)
        # self.relevant_docs = relevant_docs
        # self.unrelevant_docs = unrelevant_docs
        self.all_docs = relevant_docs + unrelevant_docs

        self.n = 2

        self.relevant_docs_token = [self.tokenizer(d) for d in relevant_docs]
        self.unrelevant_docs_token = [self.tokenizer(d) for d in unrelevant_docs]
        self.all_docs_token = self.relevant_docs_token + self.unrelevant_docs_token

        self.query = query
        self.vocab = None
        self.get_vocab()
        self.vecs_rel = None
        self.vecs_unrel = None
        self.vec_query = None
        self.get_vec()

    @staticmethod
    def tokenizer(text):
        text = text.lower()
        text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
        text = re.sub("[^a-z]+", " ", text)
        res = text.split()  # Remove spaces, tabs, and new lines
        res = [word for word in res if word not in stopwords.words("english")]
        # ps = PorterStemmer()
        # stemmed_words_set = set()

        # for word in res:
        #     stemmed_word = ps.stem(word)
        #     if stemmed_word not in stopwords.words("english"):
        #         stemmed_words_set.add(stemmed_word)
        #
        # return list(stemmed_words_set)

        # res = word_tokenize(text)
        return res

    def get_vocab(self):
        raw_vocabs = self.relevant_docs + " " + self.unrelevant_docs + " " + self.query
        self.vocab = list(set(self.tokenizer(raw_vocabs)))

    @staticmethod
    def map_vec(vocab, tokens):
        mp = {k: 0 for k in set(vocab)}
        for t in tokens:
            mp[t] += 1
        return mp

    # def get_vec(self):
    #     rel_docs_mp = self.map_vec(self.vocab, self.tokenizer(self.relevant_docs))
    #     unrel_docs_mp = self.map_vec(self.vocab, self.tokenizer(self.unrelevant_docs))
    #     query_mp = self.map_vec(self.vocab, self.tokenizer(self.query))
    #     self.vec_rel = np.array([rel_docs_mp[k] for k in self.vocab])
    #     self.vec_unrel = np.array([unrel_docs_mp[k] for k in self.vocab])
    #     self.vec_query = np.array([query_mp[k] for k in self.vocab])
    # print(self.vec_query, self.vec_unrel)
    def get_vec(self):
        idf_map = self.get_idf(self.vocab, self.all_docs_token)
        self.vecs_unrel = [
            self.get_tf_idf(self.vocab, idf_map, tokens)
            for tokens in self.unrelevant_docs_token
        ]
        self.vecs_rel = [
            self.get_tf_idf(self.vocab, idf_map, tokens)
            for tokens in self.relevant_docs_token
        ]
        query_mp = self.map_vec(self.vocab, self.tokenizer(self.query))
        self.vec_query = np.array([query_mp[k] for k in self.vocab])
        # print(self.vecs_unrel)

    def get_idf(self, vocab, all_docs):
        # vocab: list of tokens
        # all_docs: list all list of tokens, rel and unrel
        # return df
        res = dict()
        all_docs_set = [set(s) for s in all_docs]
        for word in vocab:
            res[word] = 0
            for d in all_docs_set:
                if word in d:
                    res[word] += 1
        result = dict()
        for k, v in res.items():
            result[k] = math.log10(len(all_docs) / v)
        # return np.array([result[k] for k in self.vocab])
        return result

    def get_tf_idf(self, vocab, idf_map, tokens):
        # vocab: list of vocab
        # idf_map: [word: its idf
        # tokens: words in a doc
        # return vec of document tf_idf
        token_freq = dict()
        temp_res = []
        for t in tokens:
            if t not in token_freq:
                token_freq[t] = 1
            else:
                token_freq[t] += 1
        for t in vocab:
            freq = 0
            if t in token_freq:
                freq = token_freq[t]
            temp = math.log10(freq + 1) * idf_map[t]
            temp_res.append(temp)
        return np.array(temp_res)

    def generate_ngrams(self, n, all_docs_token):

        ngrams = {}

        # Iterate through the words to generate n-grams
        for doc in all_docs_token:
            for i in range(len(doc) - n + 1):
                # Construct the 2-gram word

                ngram_word = ' '.join([doc[i], doc[i + n -1]])

                # Add the 2-gram word to the dictionary and update its occurrence count
                if ngram_word in ngrams:
                    ngrams[ngram_word] += 1
                else:
                    ngrams[ngram_word] = 1

        return ngrams

    def generate_groups(self, res_tokens, n, ngrams):
        words = [self.vocab[idx] for idx, _ in res_tokens]
        # print(words, len(words), n)
        # print(list(combinations(words, n)))

        all_groups =[]

        # Generate all combinations of n numbers from the given list
        for group in permutations(words, len(words)):
            all_groups.append(' '.join(group))
        # print(all_groups)

        prob_map = dict()
        for group in all_groups:
            i = 2
            occ = 0
            while i < len(group):
                s = group[:i]
                if s in ngrams:
                    occ += ngrams[s]
                i += 1
            prob_map[occ] = group
        max_key = max(prob_map.keys())
        res = prob_map[max_key]
        return res

    def run(self, alpha, beta, gamma):
        # return the new query
        # print(self.vocab)

        query_prev = self.vec_query
        vecs_rel_norm = [v / np.linalg.norm(v, ord=2) for v in self.vecs_rel]
        vecs_unrel_norm = [v / np.linalg.norm(v, ord=2) for v in self.vecs_unrel]

        rel = np.sum(vecs_rel_norm, axis=0)
        unrel = np.sum(vecs_unrel_norm, axis=0)
        query_new = (
            alpha * query_prev
            + (beta / self.num_relevant_docs) * rel
            - (gamma / self.num_unrelevant_docs) * unrel
        )

        # print(query_new)
        difference = (
            query_new - query_prev
        )  # get the diff and only find the positive increase tokens
        all_new_tokens = [
            (i, diff)
            for i, diff in enumerate(difference)
            if diff > 0 and query_prev[i] == 0
        ]
        old_tokens = [
            (i, diff) for i, diff in enumerate(difference) if query_prev[i] == 1
        ]

        top_new_tokens = sorted(all_new_tokens, key=lambda x: x[1], reverse=True)[:2]

        res_tokens = sorted(
            old_tokens + top_new_tokens, key=lambda x: x[1], reverse=True
        )


        n_gram_dict = self.generate_ngrams(self.n, self.relevant_docs_token)


        possible_n_gram = self.generate_groups(res_tokens,self.n, n_gram_dict)
        return possible_n_gram
        # print(n_gram_dict)
        # print(possible_n_gram)



