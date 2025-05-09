import asyncio
import logging
from typing import Any, Callable

from langchain_core.language_models import LanguageModelLike, BaseLanguageModel
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from veri_agents_knowledgebase import Knowledgebase, KnowledgeFilter

log = logging.getLogger(__name__)

LLMProviderCallable = Callable[[str], BaseLanguageModel | None]
KnowledgebaseProviderCallable = Callable[[str], Knowledgebase | None]


def get_args_from_config(config: RunnableConfig, arg: str) -> str | None:
    """Get workflow arguments for from the runnable configuration."""
    return config["configurable"].get("args", {}).get(arg)  # type: ignore


def get_llm_from_config(
    config: RunnableConfig,
    llm_field: str = "llm",
    default_llm: BaseLanguageModel | str | None = None,
    llm_provider: LLMProviderCallable | None = None,
) -> BaseLanguageModel:
    """ Get an LLM from the runnable config or use a default LLM.
    
    Args:
        config: The runnable configuration.
        llm_field: The field in the config to look for the LLM.
        default_llm: The default LLM to use if not found in the config, can be a string then llm_provider is required or an LLM object.
        llm_provider: A callable to get the LLM by name if the default_llm is a string or if the config contains an LLM key.
    Returns:
        The retrieved LLM.
    Raises:
        ValueError: If the LLM is not found in the config and no default LLM is provided.
    """
    llm_override = get_args_from_config(config, llm_field)
    # config LLMs
    if llm_override:
        if llm_provider is None:
            raise ValueError(
                "LLM provider not provided but runnable config contains LLM key."
            )
        llm = llm_provider(llm_override)
        if llm is None:
            raise ValueError(f"LLM {llm_override} not found.")
        return llm

    # LLM as string?
    if isinstance(default_llm, str):
        if llm_provider is None:
            raise ValueError("LLM provider not provided but LLM provided as string.")
        llm = llm_provider(default_llm)
        if llm is None:
            raise ValueError(f"LLM {default_llm} not found.")
        return llm

    # LLM as object
    if default_llm is not None:
        return default_llm
    raise ValueError("LLM not provided.")


def get_knowledgebase_from_config(
    config: RunnableConfig,
    knowledgebase_field: str = "knowledgebase",
    default_knowledgebase: Knowledgebase | str | None = None,
    knowledgebase_provider: KnowledgebaseProviderCallable | None = None,
) -> Knowledgebase:
    """ Get a knowledgebase from the runnable config or use a default knowledgebase.
    Args:
        config: The runnable configuration.
        knowledgebase_field: The field in the config to look for the knowledgebase.
        default_knowledgebase: The default knowledgebase to use if not found in the config, can be a string then knowledgebase_provider is required or an Knowledgebase object.
        knowledgebase_provider: A callable to get the knowledgebase by name if the default_knowledgebase is a string or if the config contains a knowledgebase key.
    Returns:
        The retrieved knowledgebase.
    Raises:
        ValueError: If the knowledgebase is not found in the config and no default knowledgebase is provided.
    """
    kb_override = get_args_from_config(config, knowledgebase_field)
    # config knowledgebase
    if kb_override:
        if knowledgebase_provider is None:
            raise ValueError(
                "Knowledgebase provider not provided but runnable config contains knowledgebase key."
            )
        kb = knowledgebase_provider(kb_override)
        if kb is None:
            raise ValueError(f"Knowledgebase {kb_override} not found.")
        return kb

    # Knowledgebase as string?
    if isinstance(default_knowledgebase, str):
        if knowledgebase_provider is None:
            raise ValueError(
                "Knowledgebase provider not provided but knowledgebase provided as string."
            )
        kb = knowledgebase_provider(default_knowledgebase)
        if kb is None:
            raise ValueError(f"Knowledgebase {default_knowledgebase} not found.")
        return kb

    # Knowledgebase as object
    if default_knowledgebase is not None:
        return default_knowledgebase
    raise ValueError("Knowledgebase not provided.")


def get_filter_from_config(
    config: RunnableConfig,
    default_filter: KnowledgeFilter | None = None,
    prefix: str = "",
) -> KnowledgeFilter:
    """Gets filter parameters from a runnable config.
    
    Args:
        config: The runnable configuration.
        default_filter: The default filter settings to use if not found in the config.
        prefix: The prefix to use for the filter keys in the config.
    Returns:
        A KnowledgeFilter object with the filter settings.
    """
    if default_filter is None:
        default_filter = KnowledgeFilter()
    doc_filter = (
        get_args_from_config(config, f"{prefix}documents") or default_filter.docs
    )
    tag_any_filter = (
        get_args_from_config(config, f"{prefix}tags_any") or default_filter.tags_any_of
    )
    tag_all_filter = (
        get_args_from_config(config, f"{prefix}tags_all") or default_filter.tags_all_of
    )
    filter = KnowledgeFilter(
        docs=doc_filter,
        tags_any_of=tag_any_filter,
        tags_all_of=tag_all_filter,
    )
    return filter


async def ainvoke_llm(llm, messages, retries: int = 3):
    """Invoke an LLM with the given messages with retry logic."""
    for _ in range(retries):  # Retry up to 3 times
        try:
            response = await llm.ainvoke(messages)
            return response
        # should try to handle more specific exceptions
        # but it seems we have to break abstraction here
        # for example Nova gives us botocore exceptions
        except Exception as e:
            log.warning("Extract: error: %s. Retrying...", e)
            await asyncio.sleep(3)
    raise RuntimeError("LLM invocation failed after %d retries" % retries)


async def achunk_content(content: str, max_chunk_length: int) -> list[str]:
    """Chunk a document string into smaller pieces to fit within the max character length."""
    chunks = []
    start = 0
    while start < len(content):
        end = min(start + max_chunk_length, len(content))
        # If not at the end of content, try to find a good break point
        if end < len(content):
            # Try to break at paragraph, sentence, or word boundary
            for break_char in ["\n\n", "\n", ". ", " "]:
                potential_end = content.rfind(break_char, start + 1, end)
                if potential_end > start:
                    end = potential_end + len(break_char)
                    break
        chunks.append(content[start:end])
        start = end
    return chunks


async def reduce_dict_or_list(
    existing: dict[Any, list[Any]] | list[Any],
    new: dict[str, list[str]] | list[dict[str, list[str]]],
) -> dict[str, list[str]] | list[dict[str, list[str]]]:
    """Reduce a dictionary or list of dictionaries by merging values."""
    if isinstance(existing, dict) and isinstance(new, dict):
        for key, value in new.items():
            if key not in existing:
                existing[key] = []
            existing[key].extend(value)
        return existing
    elif isinstance(existing, list) and isinstance(new, list):
        for item in new:
            if item not in existing:
                existing.append(item)
        return existing
    else:
        raise ValueError("Both inputs must be either dict or list of dicts.")


async def aprocess_single_doc(
    doc,
    messages,
    llm_structured,
    system_prompt: str,
    reduce_results: Callable[[Any | None, Any], Any],
    retries_per_chunk: int = 3,
    max_chunk_length: int = 40000,
    max_concurrent_chunks: int = 5,
    docs_semaphore: asyncio.Semaphore = asyncio.Semaphore(3),
) -> tuple[str, Any]:
    """Process a document by applying a structured LLM call, extracting entities, chunking it if it exceeds the max token length threshold.

    Args:
        doc: Document to process.
        messages: Message history.
        llm_structured: LLM with structured output.
        retries_per_chunk: Number of retries for each chunk.
        max_chunk_length: Maximum length of each chunk.
        docs_semaphore: Semaphore to limit concurrent processing of documents.
    Returns:
        A tuple containing the document source and the extraction results.
    """
    async with docs_semaphore:
        content = doc.page_content
        source = doc.metadata["source"]

        # If content is short enough, process it in one go
        if len(content) <= max_chunk_length:
            send_messages = [
                SystemMessage(content=system_prompt),
                messages[-1],
                HumanMessage(content=content),
            ]
            response = await ainvoke_llm(
                llm_structured, send_messages, retries_per_chunk
            )
            log.debug("Extract: Response for full document: %s", response)
            return source, response.entities

        # For longer content, chunk it and process each chunk
        chunks = await achunk_content(content, max_chunk_length)
        log.debug(f"Split document {source} into {len(chunks)} chunks")

        # Process each chunk and merge results
        # all_entities: dict[str, list[str]] = {}
        all_results = None

        for i in range(0, len(chunks), max_concurrent_chunks):
            chunk_seq = chunks[i : i + max_concurrent_chunks]
            send_messages = [
                [
                    SystemMessage(content=system_prompt),
                    messages[-1],
                    HumanMessage(
                        content=f"Provided data: [PART {i + 1}/{len(chunks)}]\\n\\n{chunk}"
                    ),
                ]
                for chunk in chunk_seq
            ]
            results = await asyncio.gather(
                *[
                    ainvoke_llm(llm_structured, chunk_messages, retries_per_chunk)
                    for chunk_messages in send_messages
                ]
            )
            for response in results:
                all_results = reduce_results(all_results, response)
        return source, all_results


async def aprocess_docs(
    docs,
    messages,
    llm_structured,
    system_prompt: str,
    reduce_results: Callable[[Any | None, Any], Any],
    max_concurrent_docs=3,
    retries_per_chunk: int = 3,
    max_chunk_length: int = 40000,
    max_concurrent_chunks=5,
) -> dict[str, Any]:
    """Process documents concurrently to run a strctured LLM call and extract entities.

    Args:
        docs: List of documents to process.
        messages: Message history.
        llm_structured: LLM with structured output.

    Returns:
        A dictionary mapping document sources to extracted entities.
    """
    semaphore = asyncio.Semaphore(max_concurrent_docs)
    extraction_results: dict[str, dict[str, list[str]]] = {}
    results = await asyncio.gather(
        *[
            aprocess_single_doc(
                doc,
                messages,
                llm_structured,
                system_prompt,
                reduce_results,
                retries_per_chunk=retries_per_chunk,
                max_chunk_length=max_chunk_length,
                max_concurrent_chunks=max_concurrent_chunks,
                docs_semaphore=semaphore,
            )
            for doc in docs
        ]
    )
    for source, entities in results:
        extraction_results[source] = entities
    return extraction_results
