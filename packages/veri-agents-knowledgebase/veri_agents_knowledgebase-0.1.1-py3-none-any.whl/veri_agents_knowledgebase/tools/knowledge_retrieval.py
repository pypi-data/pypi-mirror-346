import logging
from typing import Callable, Optional, Tuple, Unpack

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel, Field
from veri_agents_knowledgebase.knowledgebase import Knowledgebase, KnowledgeFilter
from veri_agents_knowledgebase.utils import get_filter_from_config

log = logging.getLogger(__name__)


class FixedKnowledgebaseQueryInput(BaseModel):
    query: str = Field(
        description="query to search for documents in the knowledgebase."
    )


class FixedKnowledgebaseQuery(BaseTool):
    """Search for documents in a knowledgebase that is not selected by the agent.
    IMPORTANT: The knowledgebase must be specified when initiating through ToolProvider.
    Example:
    ```
    kb_tool = ToolProvider.get_tool("knowledge_retrieval_fixed_kb", knowledgebase="regulations")
    ```
    """

    name: str = "knowledge_retrieval_fixed_kb"
    description: str = (
        "Searches for documents in a knowledgebase. Input should be a search query."
    )
    args_schema = FixedKnowledgebaseQueryInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    num_results: int = 4
    knowledgebase: Knowledgebase

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "kb_retrieve_" + self.knowledgebase.name
        if not self.knowledgebase:
            raise ToolException(
                "Knowledgebase not specified (pass into get_tool as knowledgebase='kb')."
            )
        self.description = f"Searches for documents in the {self.knowledgebase.name} knowledgebase. Use this tool if you're interested in documents about {self.knowledgebase.description}."

    def _run(
        self,
        query: str,
        # knowledgebase: Annotated[str, InjectedState("knowledgebase")],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[list[str], dict]:
        log.info(f"Searching in knowledgebase {self.knowledgebase.name} for {query}")
        docs = self.knowledgebase.retrieve(query, limit=self.num_results)
        log.info(f"Retrieved {len(docs)} documents.")
        # TODO: do we really want all that docling stuff? or filter already during ingestion?
        return [d.page_content for d in docs], {
            "items": docs,
            "type": "document",
            "source": "knowledgebase",
        }


class FixedKnowledgebaseWithTagsQueryInput(BaseModel):
    query: str = Field(
        description="query to search for documents in the knowledgebase."
    )
    tags_any: Optional[list[str]|str] = Field(
        default=None,
        description="Documents are selected if they match any of the tags in this list. Useful if for example searching for a document that's either about 'electricity' or about 'software'.",
    )
    tags_all: Optional[list[str]|str] = Field(
        default=None,
        description="Documents are selected if they match all of the tags in this list. Useful if for example searching for a document that's both a 'policy' and valid in 'Nashville'.",
    )
    documents: Optional[list[str]|str] = Field(
        default=None,
        description="Documents are selected only if they match the document IDs in the list. Useful if you only want to search inside specific documents.",
    )


class FixedKnowledgebaseWithTagsQuery(BaseTool):
    """Search for documents in a knowledgebase (that can not be selected by the agent) where the agent can specify tags to filter the documents."""

    name: str = "kb_retrieve_tags"
    description: str = "Searches in documents."
    args_schema = FixedKnowledgebaseWithTagsQueryInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    num_results: int = 5
    knowledgebase: Knowledgebase
    """ The knowledgebase to list documents from. This is passed in when the tool is created. """

    name_suffix: str | None = None
    """ You can pass in a suffix to the name of the tool. This is useful if you want to have multiple instances of this tool. """

    runnable_config_filter_prefix: str = "filter_"
    """ The prefix to use for the filter in the runnable config. For example if the prefix is 'filter_' then it will pull from the config 'filter_tags_any', 'filter_tags_all', 'filter_documents' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.name_suffix:
            self.name = self.name + self.name_suffix
        kb_tags = self.knowledgebase.tags
        self.description = f"Searches for documents in the {self.knowledgebase.name} knowledgebase. Use this tool if you're interested in documents about {self.knowledgebase.description}."
        if kb_tags:
            self.description += " The knowledgebase has the following tags: "
            for k, v in kb_tags.items():
                self.description += f"{k}: {v}, "

    def _run(
        self,
        query: str,
        config: RunnableConfig,
        tags_any: Optional[list[str]|str] = None,
        tags_all: Optional[list[str]|str] = None,
        documents: Optional[list[str]|str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[list[str], dict]:

        # We tell the LLM if the user has specified any filters
        return_texts = []

        # filter set by the agent
        filter = KnowledgeFilter(
            docs=documents,
            tags_any_of=tags_any,
            tags_all_of=tags_all,
        )

        # if the user overrides using runnable config, use that instead
        # TODO: perhaps we should apply those filters first and then the agent picked one in addition to this
        if config:
            user_filter = get_filter_from_config(
                config,
                default_filter=filter,
                prefix=self.runnable_config_filter_prefix,
            )
            if user_filter != filter:
                filter = user_filter
                return_texts.append(f"User applied the following filters: {user_filter}.\n")
            

        log.info(
            f"[FixedKnowledgebaseWithTagsQuery] Searching in knowledgebase {self.knowledgebase.name} for {query} using filter {filter}"
        )
        docs = self.knowledgebase.retrieve(query, limit=self.num_results, filter=filter)
        log.info(f"[FixedKnowledgebaseWithTagsQuery] Retrieved {len(docs)} documents.")

        if len(docs) == 0:
            return_texts.append(
                f"No documents found in the knowledgebase for query '{query}'."
            )
        else:
            for d in docs:
                return_texts.append(f"Source: {d.metadata.get('source', 'unknown')}\nContent: {d.page_content}\n")
        # TODO: do we really want all that docling stuff? or filter already during ingestion?
        return return_texts , {
            "items": docs,
            "type": "document",
            "source": "knowledgebase",
        }


class FixedKnowledgebaseListDocumentsInput(BaseModel):
    tags_any: Optional[list[str]|str] = Field(
        default=None,
        description="Documents are selected if they match any of the tags in this list. Useful if for example searching for a document that's either about 'electricity' or about 'software'.",
    )
    tags_all: Optional[list[str]|str] = Field(
        default=None,
        description="Documents are selected if they match all of the tags in this list. Useful if for example searching for a document that's both a 'policy' and valid in 'Nashville'.",
    )


class FixedKnowledgebaseListDocuments(BaseTool):
    """List documents in a knowledgebase that is not selected by the agent.
    """

    name: str = "list_documents"
    description: str = "Lists documents in a knowledgebase"
    args_schema = FixedKnowledgebaseListDocumentsInput
    # response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    knowledgebase: Knowledgebase
    """ The knowledgebase to list documents from. This is passed in when the tool is created. """

    name_suffix: str | None = None
    """ You can pass in a suffix to the name of the tool. This is useful if you want to have multiple instances of this tool. """

    runnable_config_filter_prefix: str = "filter_"
    """ The prefix to use for the filter in the runnable config. For example if the prefix is 'filter_' then it will pull from the config 'filter_tags_any', 'filter_tags_all' """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.name_suffix:
            self.name = self.name + self.name_suffix
        kb_tags = self.knowledgebase.tags
        self.description = (
            f"Lists the documents in the {self.knowledgebase.name} knowledgebase."
        )
        if kb_tags:
            self.description += " The knowledgebase has the following tags: "
            for k, v in kb_tags.items():
                self.description += f"{k}: {v}, "

    def _run(
        self,
        config: RunnableConfig,
        tags_any: Optional[list[str]|str] = None,
        tags_all: Optional[list[str]|str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:  # -> Tuple[list[str], dict]:
        # TODO: would be interesting to not get the content as well
        log.debug("[FixedKnowledgebaseListDocuments] Listing documents")

        # filter set by the agent
        filter = KnowledgeFilter(
            docs=None,
            tags_any_of=tags_any,
            tags_all_of=tags_all,
        )

        # if the user overrides using runnable config, use that instead
        # TODO: perhaps we should apply those filters first and then the agent picked one in addition to this
        if config:
            filter = get_filter_from_config(
                config,
                default_filter=filter,
                prefix=self.runnable_config_filter_prefix,
            )

            print("KB RETRIEVAL RUNNABLE FILTER")
            print(filter)

        docs = self.knowledgebase.get_documents(filter)
        log.debug("[FixedKnowledgebaseListDocuments] Retrieved documents.")
        return str(
            [
                (
                    d.metadata.get("source"),
                    d.metadata.get("doc_name"),
                    d.metadata.get("last_updated"),
                    d.metadata.get("tags"),
                    d.metadata.get("summary"),
                )
                for d in docs
            ]
        )
