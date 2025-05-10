# DenSpa

**DenSpa** is an open-source package designed for hybrid search, enabling seamless integration into Retrieval-Augmented Generation (RAG) frameworks. The package combines **dense** and **sparse vector embeddings** to perform efficient searches on document corpora.  

- **Dense-vector-based search** leverages the FAISS vector database to manage and query collections.  
- **Sparse-vector-based search** utilizes a custom implementation of BM25, enhanced with pre-processing techniques like stemming to optimize the index.  

## Installation

To get started, clone this repository and install the dependencies or use pip:  
```bash
pip install DenSpa
```

## Quick Start

### Initializing the Vector Search Engine
You can easily initialize the vector search engine using the following code:  

```python
from denspa import VectorSearch
from langchain.embeddings import HuggingFaceEmbeddings
import os

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

INDEX_PATH = "database/index"
if not os.path.exists(INDEX_PATH):
    os.makedirs(INDEX_PATH)

vecsea = VectorSearch(
    folder_path=INDEX_PATH,
    index_name="denspa",
    embedding_function=embedding_function,
    bm25_options={"k1": 1.25, "b": 0}
)
```

### Indexing Documents
DenSpa supports indexing documents in both **English** and **German**. Documents can be added to the search engine like this:

```python
from langchain.docstore.document import Document

documents = [Document(page_content="There are many variations...", metadata={"source": "lecture.pdf"})]

# Indexing with FAISS
vecsea.add_documents(documents, lang="en", engine="faiss")

# Indexing with BM25
vecsea.add_documents(documents, lang="en", engine="bm25")

# Save the index locally
vecsea.save_local()
```

### Deleting Indexed Documents
To remove a specific document from the index, use the `removeByMetadata` function:

```python
vecsea.removeByMetadata({"source": "lecture.pdf"})
vecsea.save_local()
```

### Deleting Indexes
To remove the indexes, use the `delete_local` function:

```python
vecsea.delete_local()
```

## Search Methods

DenSpa currently supports **three search methods**:  

1. **FAISS**: Semantic search that uses dense vectors for similarity.  
2. **BM25**: Keyword-based search leveraging sparse vectors.  
3. **Hybrid Search**: A cascade method combining FAISS and BM25. Hybrid search first retrieves the top-k results using FAISS (high recall) and then applies BM25 (high precision) to re-rank the results without changing the FAISS's similarity scores.  

Example usage:  
```python
results = vecsea.similarity_search_with_score(
    query="Quantum mechanics",
    k=3,
    method="bm25" | "faiss" | "cascade",
    lang="en" | "de"
)
```

## Features
- **Dense and Sparse Search**: Utilize semantic embeddings and keyword-based indexing for versatile search capabilities.  
- **Hybrid Search Strategy**: Combine the strengths of both FAISS and BM25 for balanced recall and precision.  
- **Customizable**: Easily configure embeddings, BM25 parameters, and storage paths.  
- **Language Support**: Works with English and German document corpora.  

## Contributions
Contributions are welcome! Please feel free to open an issue or submit a pull request if you have suggestions or improvements.
