# Utilities for generating and handling embeddings 

import os
import numpy as np
from openai import OpenAI
from typing import List, Optional

from . import config

def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Initializes and returns an OpenAI client.

    Args:
        api_key (Optional[str], optional): The OpenAI API key.
            If not provided, it will try to use the OPENAI_API_KEY environment variable.
            Defaults to None.

    Raises:
        ValueError: If no API key is provided and the OPENAI_API_KEY environment variable is not set.

    Returns:
        OpenAI: An initialized OpenAI client.
    """
    if api_key:
        return OpenAI(api_key=api_key)
    else:
        env_api_key = os.environ.get("OPENAI_API_KEY")
        if env_api_key:
            return OpenAI(api_key=env_api_key)
        else:
            raise ValueError(
                "No OpenAI API key provided directly or found in OPENAI_API_KEY environment variable."
            ) 

def generate_embeddings(
    client: OpenAI,
    texts_list: List[str],
    model_name: Optional[str] = None
) -> np.ndarray:
    """Generates embeddings for a list of texts using the specified model.

    Args:
        client (OpenAI): The initialized OpenAI client.
        texts_list (List[str]): A list of texts to embed.
        model_name (Optional[str], optional): The name of the embedding model to use.
            If None, defaults to config.DEFAULT_EMBEDDING_MODEL. Defaults to None.

    Returns:
        np.ndarray: A NumPy array of embeddings.

    Raises:
        Exception: If the OpenAI API call fails or if the input list is empty and an array cannot be formed as expected.
    """
    if not texts_list:
        # Return an empty 2D array with a shape like (0, embedding_dimension) if possible,
        # or handle as appropriate. For now, returning a simple empty array.
        # If a specific dimension is known for the model, it could be np.empty((0, dim)).
        return np.array([]) 

    actual_model_name = model_name if model_name else config.DEFAULT_EMBEDDING_MODEL

    try:
        api_response = client.embeddings.create(input=texts_list, model=actual_model_name)
        # Assuming all embeddings in a batch have the same dimension
        if not api_response.data:
            return np.array([]) # Should ideally match expected dimension if known
        
        embeddings = np.array([item.embedding for item in api_response.data])
        return embeddings
    except Exception as e:
        # Consider more specific error handling for API errors if needed
        # e.g., from openai.APIError
        raise Exception(f"OpenAI API call for embeddings failed with model {actual_model_name}: {e}") 

def normalize_embeddings(embeddings_array: np.ndarray) -> np.ndarray:
    """Normalizes embeddings by subtracting the mean embedding.

    If the input array is empty or has no embeddings, it returns the array as is.

    Args:
        embeddings_array (np.ndarray): A NumPy array of embeddings.
            Expected shape is (n_embeddings, embedding_dimension).

    Returns:
        np.ndarray: The normalized NumPy array of embeddings.
    """
    if embeddings_array.size == 0:  # Handles empty array or array with no elements
        return embeddings_array
    
    mean_embedding = np.mean(embeddings_array, axis=0)
    normalized_embeddings = embeddings_array - mean_embedding
    return normalized_embeddings 