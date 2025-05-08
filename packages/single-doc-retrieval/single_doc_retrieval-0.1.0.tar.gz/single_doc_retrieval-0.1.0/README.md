# Single Document RAG Pipeline

A Python library to perform retrieval on a single, pre-parsed document. 
It identifies relevant text sections from a document based on a query (label description) and, if necessary, refines the search query iteratively to find the most sufficient context.

## Testing

The main way to use the library is by calling the `find_relevant_context` function.

```python
from src.single_doc_retrieval import find_relevant_context

my_doc_id = "sample_doc_id"  
my_label_name = "governing_law_clause" 

# Path to the directory containing folders for each parsed document
my_extraction_dir = "examples/sample_data/" 

# Path to JSON file containing descriptions and examples for various labels
my_labels_file_path = "examples/sample_data/labels.json"

my_api_key = "your_openai_api_key_here" 

custom_options = {"embedding_model": "text-embedding-3-large",
                  "chat_model": "gpt-4o", 
                  "max_refinement_attempts": 2, 
                  "max_context_iterations": 5}

try:
    relevant_text = find_relevant_context(doc_id=my_doc_id,
                                          label_name=my_label_name,
                                          extraction_dir=my_extraction_dir,
                                          labels_file_path=my_labels_file_path,
                                          openai_api_key=my_api_key,
                                          pipeline_options=custom_options)
```