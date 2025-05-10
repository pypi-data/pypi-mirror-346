import joblib
from itertools import compress

class DocStore:

    def __init__(self,documents=[]):
        self._documents = documents

    def get(self,key):
        return self._documents[key]

    def add(self,values):
        self._documents += values
        return self

    def remove(self,keys):
        key_set = frozenset(keys)        
        mask = [i not in key_set for i in range(len(self._documents))]
        self._documents = list(compress(self._documents, mask))
        
        return self

    def is_empty(self):
        return len(self._documents)==0

    def search(self,metadata):
        documents = []
        for key,doc in enumerate(self._documents):
            if all(doc.metadata.get(k,None)==v for k,v in metadata.items()):
                documents.append((key,doc))
        return documents

    def save_local(self,folder_path,filename):
        joblib.dump(self,folder_path+"/"+filename+".pkl", compress=True)
        return self

    @staticmethod
    def load_local(folder_path,filename):
        return joblib.load(folder_path+"/"+filename+".pkl")