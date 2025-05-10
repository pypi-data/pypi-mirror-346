import math

import scipy
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib


class BM25:

    def __init__(self,k1=1.25,b=.75):
        self.k1 = k1
        self.b = b
        self.cvectorizer = None
        self.vocab = None
        self.avgdl = None
        self.idfs = None
        self.weights = None
        self.cvectors = None

    def get_k1(self):
        return self.k1

    def get_b(self):
        return self.b

    def get_vocab(self):
        return self.vocab

    def set_vocab(self,vocab):
        self.vocab = vocab

    def get_weights(self):
        return self.weights

    def set_weights(self,weights):
        self.weights = weights

    def get_idfs(self):
        return self.idfs

    def set_idfs(self,idfs):
        self.idfs = idfs

    def get_cvectors(self):
        return self.cvectors

    def set_cvectors(self,cvectors):
        self.cvectors = cvectors

    def is_empty(self):
        return self.cvectors is None or self.cvectors.shape[0]==0

    def fit(self,corpus):
        self.cvectorizer = CountVectorizer(dtype=np.float32)
        self.set_cvectors(self.cvectorizer.fit_transform(corpus))
        self.set_vocab(self.cvectorizer.vocabulary_)
        return self.update()

    def update(self):
        if self.cvectors is None:
            return

        self.set_weights(scipy.sparse.lil_matrix(self.cvectors.shape,dtype=self.cvectors.dtype))
        self.set_idfs(scipy.sparse.lil_array((1,self.cvectors.shape[1]),dtype=self.cvectors.dtype))
        cx = scipy.sparse.coo_matrix(self.cvectors)

        if self.cvectors.shape[0]==0:
            return self
        
        n = self.cvectors.shape[0]        
        self.avgdl = self.cvectors.sum()/n
        dfs = np.zeros(len(self.vocab))
        ntds = np.zeros(n)

        last_i = None
        ntd = 0
        for i,j,count in zip(cx.row, cx.col, cx.data):
            if last_i is None:
                last_i = i
                
            dfs[j] += 1

            if i!=last_i:
                ntds[last_i] = ntd
                last_i = i
                ntd = 0
            ntd += count

        if last_i is not None:
            ntds[last_i] = ntd

        for i,j,count in zip(cx.row, cx.col, cx.data):
            tf = count/ntds[i]
            tf_ = tf * (self.k1 + 1)/(tf+self.k1*(1 - self.b + self.b*ntds[i]/self.avgdl))
            idf_ = math.log(1 + (n - dfs[j] + .5)/(dfs[j] + .5))
            self.weights[i,j] = tf_*idf_
            self.idfs[0,j] = idf_

        return self

    def encode(self,queries):
        cvectorizer = CountVectorizer(vocabulary=self.get_vocab(),dtype=np.float32)
        cvectors = cvectorizer.fit_transform(queries)

        weights = scipy.sparse.lil_matrix(cvectors.shape,dtype=cvectors.dtype)
        cx = scipy.sparse.coo_matrix(cvectors)

        if cvectors.shape[0]==0:
            return weights

        n = cvectors.shape[0]
        ntds = np.zeros(n)

        last_i = None
        ntd = 0
        for i,j,count in zip(cx.row, cx.col, cx.data):
            if last_i is None:
                last_i = i
                
            if i!=last_i:
                ntds[last_i] = ntd
                last_i = i
                ntd = 0
            ntd += count

        if last_i is not None:
            ntds[last_i] = ntd

        for i,j,count in zip(cx.row, cx.col, cx.data):
            tf = count/ntds[i]
            tf_ = tf * (self.k1 + 1)/(tf+self.k1*(1 - self.b + self.b*ntds[i]/self.avgdl))
            weights[i,j] = tf_*self.idfs[0,j]
        return weights

    def search(self,queries,k=5,filter=None):
        res = cosine_similarity(self.weights,self.encode(queries))
        results = [[] for _ in range(len(queries))]
        for i in range(res.shape[0]):
            for j in range(res.shape[1]):
                if filter is None or filter((i,res[i,j])):
                    results[j].append((i,res[i,j]))
        return list(map(lambda docs: sorted(docs,key=lambda x: (x[1],x[0]),reverse=True)[:k],results))

    def merge(self,bm25):
        vocab1 = self.get_vocab()
        vocab2 = bm25.get_vocab()
        cvectors1 = self.get_cvectors()
        cvectors2 = bm25.get_cvectors()
        vocab = sorted(frozenset(list(vocab1.keys())+list(vocab2.keys())))
        shape = (cvectors1.shape[0]+cvectors2.shape[0],len(vocab))
        cvectors = scipy.sparse.lil_matrix(shape,dtype=cvectors2.dtype)
        for j,token in enumerate(vocab):
            if token in vocab1:
                cvectors[:cvectors1.shape[0],j]  = cvectors1[:,vocab1[token]]
            if token in vocab2:
                cvectors[cvectors1.shape[0]:,j]  = cvectors2[:,vocab2[token]]
        self.set_cvectors(cvectors)
        self.set_vocab({v:j for j,v in enumerate(vocab)})
        self.cvectorizer = CountVectorizer(vocabulary=self.get_vocab(),dtype=np.float32)
        self.update()
        return self

    def remove(self,keys):
        key_set = frozenset(keys)        
        mask = [i not in key_set for i in range(self.cvectors.shape[0])]
        self.cvectors = self.cvectors[mask]
 
        self.update()
        return self

    def save_local(self,folder_path,index_name):
        weights = self.weights
        self.set_weights(None)
        joblib.dump(self,folder_path+"/"+index_name+".pkl", compress=True)
        self.set_weights(weights)
        return self

    @staticmethod
    def load_local(folder_path,index_name):
        bm25 = joblib.load(folder_path+"/"+index_name+".pkl")
        bm25.update()
        return bm25