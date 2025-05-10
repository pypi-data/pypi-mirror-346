import os
import scipy

from ..doc_store import DocStore
from .bm25 import BM25

class BM25API:

    def __init__(self,folder_path,index_name,k1=1.25,b=.75,autoload=True):
        self.folder_path = folder_path
        self.index_name = index_name
        self.bm25 = BM25(k1=k1,b=b)
        self.doc_store = DocStore()
        try:
            if autoload and self.exists():
                new = BM25API.load_local(folder_path,index_name)
                self.bm25 = new.bm25
                self.doc_store = new.doc_store
        except:
            pass

    @staticmethod
    def from_documents(documents,folder_path,index_name,k1=1.25,b=.75,preprocess=None):
        bm25API = BM25API(k1=k1,b=b,folder_path=folder_path,index_name=index_name)
        bm25API.bm25.fit([doc.page_content if preprocess is None else preprocess(doc.page_content) for doc in documents])
        bm25API.doc_store.add(documents)
        return bm25API

    def get_token_weights(self,token):
        weights = self.bm25.get_weights().toarray()
        return weights[:,self.bm25.get_vocab()[token]]

    def get_encoded_doc_weights(self,queries):
        encodings = [{} for _ in range(len(queries))]
        id2token = {v:k for k,v in self.bm25.get_vocab().items()}
        cx = scipy.sparse.coo_matrix(self.bm25.encode(queries))
        for i,j,weight in zip(cx.row, cx.col, cx.data):
            encodings[i][id2token[j]] = weight
        return encodings

    def get_doc_weights(self,i):
        weights = self.bm25.get_weights().toarray()
        cvectors = self.bm25.get_cvectors().toarray()
        idx = cvectors[i,:].nonzero()[0]
        id2token = {v:k for k,v in self.bm25.get_vocab().items()}
        data = {}
        for id in idx:
            data[id2token[id]] = weights[i,id]
        return data
    
    def add_documents(self,documents,preprocess=None):
        texts = [doc.page_content if preprocess is None else preprocess(doc.page_content) for doc in documents]
        if self.bm25.is_empty():
            self.bm25.fit(texts)
        else:
            self.bm25.merge(BM25(k1=self.bm25.get_k1(),b=self.bm25.get_b()).fit(texts))
        self.doc_store.add(documents)
        return self

    def save_local(self,folder_path=None,index_name=None):
        folder_path = self.folder_path if folder_path is None else folder_path
        index_name = self.index_name if index_name is None else index_name
        self.bm25.save_local(folder_path,index_name+".bm25.index")
        self.doc_store.save_local(folder_path,index_name+".bm25.doc_store")
        return self

    @staticmethod
    def load_local(folder_path,index_name):
        bm25API = BM25API(folder_path=folder_path,index_name=index_name,autoload=False)
        bm25API.bm25 = BM25.load_local(folder_path,index_name+".bm25.index")
        bm25API.doc_store = DocStore.load_local(folder_path,index_name+".bm25.doc_store")
        return bm25API

    def exists(self):
        if self.folder_path is None or self.index_name is None:
            raise Exception("folder_path or index_name not defined")
        return os.path.exists(self.folder_path+"/"+self.index_name+".bm25.index.pkl") and os.path.exists(self.folder_path+"/"+self.index_name+".bm25.doc_store.pkl")

    def removeByMetadata(self,metadata):
        keys = [key for key,_ in self.doc_store.search(metadata)]
        self.bm25.remove(keys)
        self.doc_store.remove(keys)
        
        return self

    def similarity_search_with_score(self, query, k = 5,filter=None):
        results = []
        for key,score in self.bm25.search([query],k=k,filter=None if filter is None else lambda res: filter(self.doc_store.get(res[0]).metadata))[0]:
            results.append((self.doc_store.get(key),score))
        return results