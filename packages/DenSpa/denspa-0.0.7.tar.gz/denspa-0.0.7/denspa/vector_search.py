import os
import glob

from .dense import FAISSAPI
from .sparse import BM25API
from .tokenizer import Tokenizer

class VectorSearch:

    def __init__(self,folder_path,index_name,embedding_function,bm25_options={"k1":1.25,"b":.75}):
        self.bm25_options = bm25_options
        self.bm25API = BM25API(k1=bm25_options["k1"],b=bm25_options["b"],folder_path=folder_path,index_name=index_name)
        self.faissAPI = FAISSAPI(folder_path=folder_path,index_name=index_name,embedding_function=embedding_function)
        self.folder_path = folder_path
        self.index_name = index_name
        self.embedding_function = embedding_function

    @staticmethod
    def from_documents(documents,folder_path,index_name,embedding_function,engine="*",lang=None,bm25_options={"k1":1.25,"b":.75}):
        vectorSearch = VectorSearch(folder_path=folder_path,index_name=index_name,embedding_function=embedding_function,bm25_options=bm25_options)
        if engine in ['*','faiss']:
            vectorSearch.faissAPI = vectorSearch.faissAPI.from_documents(documents,folder_path=folder_path,index_name=index_name,embedding_function=embedding_function)
        if engine in ['*','bm25']:
            tokenizer = Tokenizer(lang=lang)
            #for doc in documents:
            #    doc.page_content = " ".join(tokenizer.stem(token) for token in tokenizer.tokenize(doc.page_content))
            vectorSearch.bm25API = vectorSearch.bm25API.from_documents(documents,k1=bm25_options["k1"],b=bm25_options["b"],
                                                                       folder_path=folder_path,index_name=index_name,
                                                                       preprocess=lambda text: " ".join(tokenizer.stem(token) for token in tokenizer.tokenize(text)))
        return vectorSearch

    def add_documents(self,documents,engine='*',lang=None):
        if engine in ['*','faiss']:
            if self.faissAPI.exists():
                self.faissAPI.add_documents(documents)
            else:
                self.faissAPI = self.from_documents(documents,engine="faiss",lang=lang,folder_path=self.folder_path,index_name=self.index_name,embedding_function=self.embedding_function,bm25_options=self.bm25_options).faissAPI
        if engine in ['*','bm25']:
            tokenizer = Tokenizer(lang=lang)
            #for doc in documents:
            #    doc.page_content = " ".join(tokenizer.stem(token) for token in tokenizer.tokenize(doc.page_content))
            if self.bm25API.exists():
                self.bm25API.add_documents(documents,preprocess=lambda text: " ".join(tokenizer.stem(token) for token in tokenizer.tokenize(text)))
            else:
                self.bm25API = self.from_documents(documents,engine="bm25",lang=lang,folder_path=self.folder_path,index_name=self.index_name,embedding_function=self.embedding_function,bm25_options=self.bm25_options).bm25API
        return self


    def save_local(self,folder_path=None,index_name=None):
        folder_path = self.folder_path if folder_path is None else folder_path
        index_name = self.index_name if index_name is None else index_name
        self.bm25API.save_local(folder_path,index_name)
        self.faissAPI.save_local(folder_path,index_name)
        return self

    def delete_local(self,folder_path=None,index_name=None):
        folder_path = self.folder_path if folder_path is None else folder_path
        index_name = self.index_name if index_name is None else index_name

        search_pattern = os.path.join(folder_path, index_name + ".*")
        files_to_delete = glob.glob(search_pattern)

        for file in files_to_delete:
            try:
                os.remove(file)
            except Exception as e:
                pass
        return self

    @staticmethod
    def load_local(folder_path,index_name,embedding_function):
        vectorSearch = VectorSearch(folder_path=folder_path,index_name=index_name,embedding_function=embedding_function)
        vectorSearch.bm25API = BM25API.load_local(folder_path,index_name)
        vectorSearch.faissAPI = FAISSAPI.load_local(folder_path,index_name,embedding_function)
        return vectorSearch

    def exists(self):
        if self.folder_path is None or self.index_name is None:
            raise Exception("folder_path or index_name not defined")
        return self.faissAPI.exists() and self.bm25API.exists()

    def removeByMetadata(self,metadata):
        self.bm25API.removeByMetadata(metadata)
        self.faissAPI.removeByMetadata(metadata)
        return self

    def similarity_search_with_score(self, query, k = 5, filter=None,lang=None,method="cascade"):
        if method=="faiss":
            return self.faissAPI.similarity_search_with_score(query,k=k,filter=filter)
        elif method=="bm25":
            tokenizer = Tokenizer(lang=lang)
            return self.bm25API.similarity_search_with_score(" ".join(tokenizer.stem(token) for token in tokenizer.tokenize(query)),k=k,filter=filter)
        else:
            faiss_results = self.faissAPI.similarity_search_with_score(query,k=k,filter=filter)
            def filter_func(metadata):
                return (filter is None or filter(metadata)) and any(all(metadata.get(k,None)==v for k,v in doc.metadata.items()) for doc,_ in faiss_results)
            tokenizer = Tokenizer(lang=lang)
            bm25_results = self.bm25API.similarity_search_with_score(" ".join(tokenizer.stem(token) for token in tokenizer.tokenize(query)),k=k,filter=lambda metadata: filter_func(metadata))
            
            def findI(metadata):
                return [i for i,(doc,_) in enumerate(faiss_results) if all(metadata.get(k,None)==v for k,v in doc.metadata.items())][0]
            indexes = [findI(doc.metadata) for doc,_ in bm25_results]
            indexes += [i for i in range(len(faiss_results)) if i not in indexes]
        return [faiss_results[idx] for idx in indexes]
