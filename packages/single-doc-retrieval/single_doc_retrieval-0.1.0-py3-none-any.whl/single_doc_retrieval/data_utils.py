# Utilities for data loading and processing 

import os
import json
from typing import Tuple, Dict, Any, List

def load_parsed_document_data(doc_id: str, extraction_dir: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    
    """Loads the parsed text and hierarchy data for a given document ID.

    Args:
        doc_id (str): The unique identifier for the document.
        extraction_dir (str): The base directory where extracted document folders are stored.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the text data (from text.json)
                                                  and hierarchy data (from hierarchy.json).

    Raises:
        FileNotFoundError: If the text.json or hierarchy.json file for the given doc_id
                           or the document directory itself is not found.
        json.JSONDecodeError: If the JSON files are not valid.
    """
    
    doc_specific_path = os.path.join(extraction_dir, doc_id)
    if not os.path.isdir(doc_specific_path):
        raise FileNotFoundError(f"Directory for document ID '{doc_id}' not found at {doc_specific_path}")

    text_json_path = os.path.join(doc_specific_path, 'text.json')
    hierarchy_json_path = os.path.join(doc_specific_path, 'hierarchy.json')

    if not os.path.exists(text_json_path):
        raise FileNotFoundError(f"text.json not found for document ID '{doc_id}' at {text_json_path}")
    
    if not os.path.exists(hierarchy_json_path):
        raise FileNotFoundError(f"hierarchy.json not found for document ID '{doc_id}' at {hierarchy_json_path}")

    try:
        with open(text_json_path, 'r', encoding='utf-8') as f:
            text_data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding text.json for doc_id '{doc_id}': {e.msg}", e.doc, e.pos)

    try:
        with open(hierarchy_json_path, 'r', encoding='utf-8') as f:
            hierarchy_data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding hierarchy.json for doc_id '{doc_id}': {e.msg}", e.doc, e.pos)

    return text_data, hierarchy_data 

def load_labels_data(labels_file_path: str) -> Dict[str, Any]:
    
    """Loads the labels data from a JSON file.

    Args:
        labels_file_path (str): The path to the labels JSON file.

    Returns:
        Dict[str, Any]: The loaded labels data.

    Raises:
        FileNotFoundError: If the labels_file_path does not exist.
        json.JSONDecodeError: If the JSON file is not valid.
    """

    if not os.path.exists(labels_file_path):
        raise FileNotFoundError(f"Labels file not found at {labels_file_path}")

    try:
        with open(labels_file_path, 'r', encoding='utf-8') as f:
            labels_data = json.load(f)

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding labels file at {labels_file_path}: {e.msg}", e.doc, e.pos)
    
    return labels_data 

def extract_paragraph_data(text_data: Dict[str, Any]) -> Tuple[Dict[str, str], List[str], List[str]]:
    
    """Extracts paragraph texts and their keys from the loaded text data.

    Args:
        text_data (Dict[str, Any]): The text data loaded from text.json, structured by page.

    Returns:
        Tuple[Dict[str, str], List[str], List[str]]: A tuple containing:
            - paragraph_texts_map (Dict[str, str]): A dictionary mapping a unique key 
              (e.g., "page_tag") to the paragraph text.
            - paragraph_keys_ordered (List[str]): An ordered list of the unique keys. 
              (Note: The notebook implies order by extraction, this will be similar but 
              not strictly guaranteed across Python versions for dict iteration if not 
              using Python 3.7+. For consistent order, an explicit sort might be needed 
              if the original key construction has an inherent order, or if we derive 
              order from hierarchy.json later.)
            - paragraph_text_list (List[str]): A list of paragraph texts, in the same order 
              as paragraph_keys_ordered.
    """

    paragraph_texts_map = {}
    # For Python 3.7+, dicts preserve insertion order. For older versions, this might not be strictly true.
    
    for page, page_content in text_data.items():
        for tag, tag_text in page_content.items():
            if 'plain_text' in tag and isinstance(tag_text, str) and tag_text.strip() != '':
                unique_key = f"{page}_{tag}"
                paragraph_texts_map[unique_key] = tag_text

    # Extract keys and texts in the order they were added (for Python 3.7+)
    paragraph_keys_ordered = list(paragraph_texts_map.keys())
    paragraph_text_list = [paragraph_texts_map[key] for key in paragraph_keys_ordered]

    return paragraph_texts_map, paragraph_keys_ordered, paragraph_text_list 