import os

from langchain_community.vectorstores import FAISS


class FAISSAPI:

    def __init__(self,folder_path,index_name,embedding_function,autoload=True):
        self.embedding_function = embedding_function
        self.folder_path = folder_path
        self.index_name = index_name
        self.faiss = None
        try:
            if autoload and self.exists():
                self.faiss = FAISSAPI.load_local(folder_path,index_name,embedding_function=embedding_function).faiss
        except:
            pass

    @staticmethod
    def from_documents(documents,folder_path,index_name,embedding_function):
        faissAPI = FAISSAPI(folder_path=folder_path,index_name=index_name,embedding_function=embedding_function)
        faissAPI.faiss = FAISS.from_documents(
            documents,
            embedding_function
        )
        return faissAPI

    def add_documents(self,documents):
        self.faiss.add_documents(documents)
        return self

    def save_local(self,folder_path=None,index_name=None):
        folder_path = self.folder_path if folder_path is None else folder_path
        index_name = self.folder_path if index_name is None else index_name
        self.faiss.save_local(folder_path, index_name=index_name)
        return self

    @staticmethod
    def load_local(folder_path,index_name,embedding_function):
        faissAPI = FAISSAPI(folder_path=folder_path,index_name=index_name,embedding_function=embedding_function,autoload=False)
        faissAPI.faiss = FAISS.load_local(folder_path=folder_path, embeddings=embedding_function, 
                                          index_name=index_name,allow_dangerous_deserialization=True)
        return faissAPI

    def exists(self):
        if self.folder_path is None or self.index_name is None:
            raise Exception("folder_path or index_name not defined")
        return os.path.exists(self.folder_path+"/"+self.index_name+".faiss")

    def removeByMetadata(
            self,
            metadata
    ):
        id_to_remove = []
        for _id, doc in self.faiss.docstore._dict.items():
            if all(doc.metadata.get(k,None)==v for k,v in metadata.items()):
                id_to_remove.append(_id)
        if len(id_to_remove)==0:
            return self

        self.faiss.delete(id_to_remove)
        self.faiss.index_to_docstore_id = {
            i: _id
            for i, _id in enumerate(self.faiss.index_to_docstore_id.values())
        }
        return self

    def similarity_search_with_score(self, query, k = 5, filter=None):
        return self.faiss.similarity_search_with_score(query, k=k,filter=filter)