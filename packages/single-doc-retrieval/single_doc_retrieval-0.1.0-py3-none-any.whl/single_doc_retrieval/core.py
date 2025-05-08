# Core RAG pipeline logic 

import logging
from typing import Optional, Dict, Any, List, Tuple
import numpy as np
from openai import OpenAI

from . import config
from . import prompts
from . import data_utils
from . import embedding_utils

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Core RAG pipeline logic

def check_context_sufficiency(
    client: OpenAI,
    original_query: str,
    context_text: str,
    model_name: Optional[str] = None,
    sufficiency_prompt_template: Optional[str] = None,
    sufficiency_system_role: Optional[str] = None,
    max_tokens: int = 10,
    temperature: float = 0.0
) -> str:
    """Checks if the provided context is sufficient to answer the original query using an LLM call.

    Args:
        client (OpenAI): The initialized OpenAI client.
        original_query (str): The original user query.
        context_text (str): The accumulated context text to check.
        model_name (Optional[str], optional): The chat model to use. 
            Defaults to config.DEFAULT_CHAT_MODEL.
        sufficiency_prompt_template (Optional[str], optional): The prompt template for sufficiency check. 
            Defaults to prompts.SUFFICIENCY_PROMPT_TEMPLATE.
        sufficiency_system_role (Optional[str], optional): The system role for sufficiency check. 
            Defaults to prompts.SUFFICIENCY_SYSTEM_ROLE.
        max_tokens (int, optional): Max tokens for the LLM response. Defaults to 10.
        temperature (float, optional): Temperature for LLM sampling. Defaults to 0.0.

    Returns:
        str: The LLM's decision (e.g., "yes" or "no").

    Raises:
        Exception: If the OpenAI API call fails.
    """
    actual_model_name = model_name if model_name else config.DEFAULT_CHAT_MODEL
    actual_prompt_template = sufficiency_prompt_template if sufficiency_prompt_template else prompts.SUFFICIENCY_PROMPT_TEMPLATE
    actual_system_role = sufficiency_system_role if sufficiency_system_role else prompts.SUFFICIENCY_SYSTEM_ROLE

    if not context_text.strip():
        logging.warning("Context text is empty for sufficiency check. Returning 'no'.")
        return "no" # Cannot be sufficient if empty

    try:
        formatted_prompt = actual_prompt_template.format(original_query, context_text)
        
        response = client.chat.completions.create(
            model=actual_model_name,
            messages=[
                {"role": "system", "content": actual_system_role},
                {"role": "user", "content": formatted_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        decision = response.choices[0].message.content.strip().lower()
        return decision
    except Exception as e:
        logging.error(f"OpenAI API call for sufficiency check failed with model {actual_model_name}: {e}")
        # In case of API error, conservatively assume context is not sufficient or re-raise
        # For now, let's re-raise to make the caller aware of the API issue.
        raise Exception(f"Sufficiency check API call failed: {e}") 

def refine_query(
    client: OpenAI,
    original_query: str,
    current_query: str,
    insufficient_context: str,
    model_name: Optional[str] = None,
    refinement_prompt_template: Optional[str] = None,
    refinement_system_role: Optional[str] = None,
    max_tokens: int = 150,
    temperature: float = 0.3
) -> str:
    """Refines the current search query based on the original goal and insufficient context.

    Args:
        client (OpenAI): The initialized OpenAI client.
        original_query (str): The user's original high-level goal.
        current_query (str): The current search query that yielded insufficient results.
        insufficient_context (str): The context retrieved that was deemed insufficient.
        model_name (Optional[str], optional): The chat model for refinement. 
            Defaults to config.DEFAULT_CHAT_MODEL.
        refinement_prompt_template (Optional[str], optional): The prompt template for query refinement. 
            Defaults to prompts.QUERY_REFINEMENT_PROMPT_TEMPLATE.
        refinement_system_role (Optional[str], optional): The system role for query refinement. 
            Defaults to prompts.QUERY_REFINEMENT_SYSTEM_ROLE.
        max_tokens (int, optional): Max tokens for the LLM response. Defaults to 150.
        temperature (float, optional): Temperature for LLM sampling. Defaults to 0.3.

    Returns:
        str: The refined search query.

    Raises:
        Exception: If the OpenAI API call fails.
    """
    actual_model_name = model_name if model_name else config.DEFAULT_CHAT_MODEL
    actual_prompt_template = refinement_prompt_template if refinement_prompt_template else prompts.QUERY_REFINEMENT_PROMPT_TEMPLATE
    actual_system_role = refinement_system_role if refinement_system_role else prompts.QUERY_REFINEMENT_SYSTEM_ROLE

    try:
        formatted_prompt = actual_prompt_template.format(
            original_query=original_query,
            current_query=current_query,
            insufficient_context=insufficient_context
        )

        response = client.chat.completions.create(
            model=actual_model_name,
            messages=[
                {"role": "system", "content": actual_system_role},
                {"role": "user", "content": formatted_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        refined_query_text = response.choices[0].message.content.strip()
        return refined_query_text
    except Exception as e:
        logging.error(f"OpenAI API call for query refinement failed with model {actual_model_name}: {e}")
        # In case of API error, re-raise to make the caller aware.
        raise Exception(f"Query refinement API call failed: {e}") 

def find_relevant_context(
    doc_id: str,
    label_name: str,
    extraction_dir: str,
    labels_file_path: str,
    openai_api_key: Optional[str] = None, # API key is now optional here, get_openai_client will handle it
    pipeline_options: Optional[Dict[str, Any]] = None
) -> str:
    """Finds relevant context for a given label in a document using a RAG pipeline.

    Args:
        doc_id (str): The unique identifier for the document.
        label_name (str): The name of the label to find (key in labels_data).
        extraction_dir (str): Base directory for extracted document data.
        labels_file_path (str): Path to the JSON file containing label descriptions and examples.
        openai_api_key (Optional[str], optional): OpenAI API key. If not provided, the client
            will attempt to use the OPENAI_API_KEY environment variable. Defaults to None.
        pipeline_options (Optional[Dict[str, Any]], optional): A dictionary for overriding 
            default pipeline behaviors and parameters. Defaults to None.
            Supported options:
                - embedding_model (str): Name of the embedding model.
                - chat_model (str): Name of the chat model for sufficiency/refinement.
                - max_refinement_attempts (int): Max attempts for query refinement.
                - max_context_iterations (int): Max iterations for accumulating context per query.
                - sufficiency_prompt_template (str): Custom template for sufficiency check.
                - sufficiency_system_role (str): Custom system role for sufficiency.
                - query_refinement_prompt_template (str): Custom template for refinement.
                - query_refinement_system_role (str): Custom system role for refinement.
                - sufficiency_max_tokens (int): Max tokens for sufficiency check response.
                - sufficiency_temperature (float): Temperature for sufficiency check.
                - refinement_max_tokens (int): Max tokens for refinement response.
                - refinement_temperature (float): Temperature for refinement.

    Returns:
        str: The final, most relevant context found, or a message if no sufficient context
             could be retrieved.

    Raises:
        ValueError: If label_name is not found in labels_data.
        FileNotFoundError: If data files are not found by data_utils.
        Exception: For API call failures or other processing errors.
    """
    logging.info(f"Starting RAG pipeline for doc_id='{doc_id}', label_name='{label_name}'")

    opts = pipeline_options if pipeline_options else {}
    embedding_model = opts.get("embedding_model", config.DEFAULT_EMBEDDING_MODEL)
    chat_model = opts.get("chat_model", config.DEFAULT_CHAT_MODEL)
    max_refinement_attempts = opts.get("max_refinement_attempts", 2)
    max_context_iterations = opts.get("max_context_iterations", 5)
    
    # Prompt and role overrides
    suff_prompt_template_override = opts.get("sufficiency_prompt_template")
    suff_system_role_override = opts.get("sufficiency_system_role")
    ref_prompt_template_override = opts.get("query_refinement_prompt_template")
    ref_system_role_override = opts.get("query_refinement_system_role")

    # LLM call parameter overrides
    suff_max_tokens = opts.get("sufficiency_max_tokens", 10)
    suff_temp = opts.get("sufficiency_temperature", 0.0)
    ref_max_tokens = opts.get("refinement_max_tokens", 150)
    ref_temp = opts.get("refinement_temperature", 0.3)

    # 1. Initialize OpenAI Client
    client = embedding_utils.get_openai_client(api_key=openai_api_key)

    # 2. Load Data
    logging.info("Loading parsed document data...")
    text_data, hierarchy_data = data_utils.load_parsed_document_data(doc_id, extraction_dir)
    labels_data = data_utils.load_labels_data(labels_file_path)

    if label_name not in labels_data:
        raise ValueError(f"Label '{label_name}' not found in labels data at {labels_file_path}")

    logging.info("Extracting paragraph data...")
    paragraph_texts_map, paragraph_keys_ordered, paragraph_text_list = data_utils.extract_paragraph_data(text_data)

    if not paragraph_text_list:
        logging.warning("No paragraph texts extracted from the document. Cannot proceed.")
        return "No paragraph texts found in the document."

    # 3. Get Original Query and Example Texts for the Label
    original_query = labels_data[label_name].get("description")
    if not original_query:
        raise ValueError(f"No 'description' (original query) found for label '{label_name}'.")
    example_texts = labels_data[label_name].get("examples", [])
    label_texts_for_embedding = [original_query] + example_texts

    # 4. Generate and Normalize Embeddings
    logging.info("Generating embeddings for paragraph texts...")
    paragraph_text_embeddings = embedding_utils.generate_embeddings(client, paragraph_text_list, model_name=embedding_model)
    normalized_paragraph_text_embeddings = embedding_utils.normalize_embeddings(paragraph_text_embeddings)

    logging.info("Generating embeddings for label-related texts...")
    label_embeddings = embedding_utils.generate_embeddings(client, label_texts_for_embedding, model_name=embedding_model)
    # Using the first embedding (original query description) as the primary target, as in notebook
    # mean_label_embedding = np.mean(label_embeddings, axis=0) # Alternative: mean of all label texts
    if label_embeddings.size == 0:
        raise ValueError("Could not generate embeddings for label texts.")
    target_label_embedding = label_embeddings[0]

    # 5. Initialize RAG Loop Variables
    current_query = original_query
    current_query_embedding = target_label_embedding # Start with the original label embedding
    
    final_sufficient_text = ""
    main_processing_active = True
    refinement_iteration_count = 0
    current_context_text_overall = "" # To store the last known context

    # 6. Main RAG Loop
    while main_processing_active and refinement_iteration_count <= max_refinement_attempts:
        logging.info(f"Starting/Retrying with Query (Attempt {refinement_iteration_count + 1}): \"{current_query}\"")

        # Ensure current_query_embedding is 1D if it became 2D (e.g. after API call for refined query)
        if current_query_embedding.ndim > 1:
             current_query_embedding = current_query_embedding.flatten()

        similarity_matrix = np.dot(normalized_paragraph_text_embeddings, current_query_embedding)
        
        # Map similarity scores back to paragraph keys
        paragraph_query_similarity = {key: score for key, score in zip(paragraph_keys_ordered, similarity_matrix)}
        sorted_paragraph_query_similarity = sorted(paragraph_query_similarity.items(), key=lambda x: x[1], reverse=True)

        accumulated_context_keys_current_attempt = set()
        current_context_text_current_attempt = ""
        ordered_context_keys_for_current_text = [] # Keep track of order for joining
        found_sufficient_this_query_version = False

        for i, (match_key, match_score) in enumerate(sorted_paragraph_query_similarity):
            if i >= max_context_iterations:
                logging.info(f"Reached max context iterations ({max_context_iterations}) for query: \"{current_query}\".")
                if not final_sufficient_text: # If no sufficient text found yet in entire process
                    final_sufficient_text = current_context_text_current_attempt
                break

            current_heading = hierarchy_data.get(match_key, {}).get('heading')
            section_keys_to_add = set()

            if current_heading:
                # Find all keys under the same heading that are actual paragraphs
                section_keys_to_add = {k for k, v in hierarchy_data.items() 
                                       if v.get('heading') == current_heading and k in paragraph_texts_map}
            
            # Always include the matched key itself if it's a valid paragraph
            if match_key in paragraph_texts_map:
                section_keys_to_add.add(match_key)

            new_keys = section_keys_to_add - accumulated_context_keys_current_attempt
            if not new_keys:
                if not current_context_text_current_attempt: # If context still empty, must proceed
                    pass 
                else: # If context exists and no new keys, skip LLM call for this iteration
                    continue
            
            accumulated_context_keys_current_attempt.update(new_keys)
            
            # Sort all accumulated keys by their order in the document hierarchy
            valid_keys_for_sorting = [k for k in accumulated_context_keys_current_attempt 
                                      if k in hierarchy_data and 'order' in hierarchy_data[k]]
            ordered_context_keys_for_current_text = sorted(valid_keys_for_sorting, key=lambda k: hierarchy_data[k]['order'])
            
            # Rebuild context based on sorted order
            accumulated_texts_list = [paragraph_texts_map[key] for key in ordered_context_keys_for_current_text 
                                      if key in paragraph_texts_map] # Ensure key exists
            current_context_text_current_attempt = "\n\n".join(accumulated_texts_list)
            current_context_text_overall = current_context_text_current_attempt # Update overall last known context

            if not current_context_text_current_attempt.strip():
                continue # Skip sufficiency if context is empty

            try:
                decision = check_context_sufficiency(
                    client,
                    original_query, # Always check against the original goal
                    current_context_text_current_attempt,
                    model_name=chat_model,
                    sufficiency_prompt_template=suff_prompt_template_override,
                    sufficiency_system_role=suff_system_role_override,
                    max_tokens=suff_max_tokens,
                    temperature=suff_temp
                )
                logging.info(f"Context Iteration {i+1}: Query: \"{current_query}\", Context length: {len(current_context_text_current_attempt)}, Sufficiency for \"{original_query}\": {decision}")

                if decision.startswith("yes"):
                    final_sufficient_text = current_context_text_current_attempt
                    logging.info("LLM deemed context sufficient.")
                    main_processing_active = False # Signal to exit outer loop
                    found_sufficient_this_query_version = True
                    break # Exit inner context accumulation loop
            
            except Exception as e:
                logging.error(f"Error during sufficiency check: {e}")
                # Decide if we should break or continue. For now, let it try next context or refinement.
                # decision = "no" # Implicitly handled as not "yes"

        # --- End of inner context accumulation loop ---

        if not found_sufficient_this_query_version and main_processing_active:
            if refinement_iteration_count < max_refinement_attempts:
                logging.info(f"Context insufficient for query \"{current_query}\". Attempting refinement...")
                refinement_iteration_count += 1
                try:
                    refined_query_candidate = refine_query(
                        client,
                        original_query=original_query,
                        current_query=current_query,
                        insufficient_context=current_context_text_current_attempt, # Use context from this failed attempt
                        model_name=chat_model,
                        refinement_prompt_template=ref_prompt_template_override,
                        refinement_system_role=ref_system_role_override,
                        max_tokens=ref_max_tokens,
                        temperature=ref_temp
                    )
                    if refined_query_candidate and refined_query_candidate.lower() != current_query.lower():
                        logging.info(f"Query refined from \"{current_query}\" to \"{refined_query_candidate}\"")
                        current_query = refined_query_candidate
                        # Get embedding for the new refined query
                        refined_query_embedding_list = embedding_utils.generate_embeddings(client, [current_query], model_name=embedding_model)
                        if refined_query_embedding_list.size > 0:
                            current_query_embedding = refined_query_embedding_list[0]
                        else:
                            logging.error("Failed to generate embedding for refined query. Stopping.")
                            main_processing_active = False # Stop if embedding fails
                        final_sufficient_text = "" # Reset, as we are using a new query
                    else:
                        logging.info("LLM failed to refine query meaningfully or produced same query. Stopping.")
                        if not final_sufficient_text:
                            final_sufficient_text = current_context_text_current_attempt
                        main_processing_active = False # Stop refinement attempts
                except Exception as e:
                    logging.error(f"Error during query refinement: {e}")
                    if not final_sufficient_text:
                        final_sufficient_text = current_context_text_current_attempt
                    main_processing_active = False # Stop on error
            else:
                logging.info(f"Max refinement attempts ({max_refinement_attempts}) reached.")
                if not final_sufficient_text:
                    final_sufficient_text = current_context_text_current_attempt
                main_processing_active = False # Stop after max attempts
        
        elif found_sufficient_this_query_version:
            main_processing_active = False # Ensure outer loop terminates
        
        # If main_processing_active became false for other reasons (e.g. error), ensure loop ends

    # --- End of main RAG loop ---

    if not final_sufficient_text and current_context_text_overall:
        logging.info("No definitively sufficient context found. Using the last accumulated context.")
        final_sufficient_text = current_context_text_overall
    elif not final_sufficient_text:
        logging.info("No sufficient context could be retrieved, and no prior context was accumulated.")
        final_sufficient_text = "No sufficient context could be retrieved."
    
    logging.info(f"RAG pipeline finished for doc_id='{doc_id}', label_name='{label_name}'")
    return final_sufficient_text 