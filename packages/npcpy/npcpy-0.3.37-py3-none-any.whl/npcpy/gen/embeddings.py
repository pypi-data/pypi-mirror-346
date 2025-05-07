#######
#######
#######
#######
####### EMBEDDINGS
#######
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

try:
    from openai import OpenAI
    import anthropic
except: 
    pass

def get_ollama_embeddings(
    texts: List[str], model: str = "nomic-embed-text"
) -> List[List[float]]:
    """Generate embeddings using Ollama."""
    import ollama

    embeddings = []
    for text in texts:
        response = ollama.embeddings(model=model, prompt=text)
        embeddings.append(response["embedding"])
    return embeddings


def get_openai_embeddings(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Generate embeddings using OpenAI."""
    client = OpenAI()
    response = client.embeddings.create(input=texts, model=model)
    return [embedding.embedding for embedding in response.data]




def store_embeddings_for_model(
    texts,
    embeddings,
    chroma_client,
    model,
    provider,
    metadata=None,
):
    collection_name = f"{provider}_{model}_embeddings"
    collection = chroma_client.get_collection(collection_name)

    # Create meaningful metadata for each document (adjust as necessary)
    if metadata is None:
        metadata = [{"text_length": len(text)} for text in texts]  # Example metadata
        print(
            "metadata is none, creating metadata for each document as the length of the text"
        )
    # Add embeddings to the collection with metadata
    collection.add(
        ids=[str(i) for i in range(len(texts))],
        embeddings=embeddings,
        metadatas=metadata,  # Passing populated metadata
        documents=texts,
    )


def delete_embeddings_from_collection(collection, ids):
    """Delete embeddings by id from Chroma collection."""
    if ids:
        collection.delete(ids=ids)  # Only delete if ids are provided


def search_similar_texts(
    query: str,
    chroma_client,    
    embedding_model: str,
    embedding_provider: str ,    
    docs_to_embed: Optional[List[str]] = None,
    top_k: int = 5,
) -> List[Dict[str, any]]:
    """
    Search for similar texts using either a Chroma database or direct embedding comparison.
    """

    print(f"\nQuery to embed: {query}")
    embedded_search_term = get_ollama_embeddings([query], embedding_model)[0]
    # print(f"Query embedding: {embedded_search_term}")

    if docs_to_embed is None:
        # Fetch from the database if no documents to embed are provided
        collection_name = f"{embedding_provider}_{embedding_model}_embeddings"
        collection = chroma_client.get_collection(collection_name)
        results = collection.query(
            query_embeddings=[embedded_search_term], n_results=top_k
        )
        # Constructing and returning results
        return [
            {"id": id, "score": float(distance), "text": document}
            for id, distance, document in zip(
                results["ids"][0], results["distances"][0], results["documents"][0]
            )
        ]

    print(f"\nNumber of documents to embed: {len(docs_to_embed)}")

    # Get embeddings for provided documents
    raw_embeddings = get_ollama_embeddings(docs_to_embed, embedding_model)

    output_embeddings = []
    for idx, emb in enumerate(raw_embeddings):
        if emb:  # Exclude any empty embeddings
            output_embeddings.append(emb)

    # Convert to numpy arrays for calculations
    doc_embeddings = np.array(output_embeddings)
    query_embedding = np.array(embedded_search_term)

    # Check for zero-length embeddings
    if len(doc_embeddings) == 0:
        raise ValueError("No valid document embeddings found")

    # Normalize embeddings to avoid division by zeros
    doc_norms = np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
    query_norm = np.linalg.norm(query_embedding)

    # Ensure no zero vectors are being used in cosine similarity
    if query_norm == 0:
        raise ValueError("Query embedding is zero-length")

    # Calculate cosine similarities
    cosine_similarities = np.dot(doc_embeddings, query_embedding) / (
        doc_norms.flatten() * query_norm
    )

    # Get indices of top K documents
    top_indices = np.argsort(cosine_similarities)[::-1][:top_k]

    return [
        {
            "id": str(idx),
            "score": float(cosine_similarities[idx]),
            "text": docs_to_embed[idx],
        }
        for idx in top_indices
    ]
def get_embeddings(
    texts: List[str],
    model: str ,
    provider: str,
) -> List[List[float]]:
    """Generate embeddings using the specified provider and store them in Chroma."""
    if provider == "ollama":
        embeddings = get_ollama_embeddings(texts, model)
    elif provider == "openai":
        embeddings = get_openai_embeddings(texts, model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    # Store the embeddings in the relevant Chroma collection
    # store_embeddings_for_model(texts, embeddings, model, provider)
    return embeddings
