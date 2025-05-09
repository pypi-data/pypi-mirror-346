import logging
from os import PathLike
from typing import Iterator, Optional, List, Dict, cast
from collections.abc import Sequence

from langchain_core.documents import Document
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class DocumentLoader:
    """Loads data from a data source and returns documents."""

    def __init__(self):
        pass

    def load_documents(self, **kwargs):
        """Parse documents from a data source."""
        raise NotImplementedError


class KnowledgeFilter(BaseModel):
    """Filter for knowledge base queries."""

    docs: list[str] | str | None = None
    """ List of document IDs or single document ID to filter by. """

    tags_any_of: list[str] | str | None = None
    """ List of tags to filter by, if any of the provided tags matches, a document is selected. """

    tags_all_of: list[str] | str | None = None
    """ List of tags to filter by, if all of the provided tags match, a document is selected. """

    def __repr__(self):
        return f"KnowledgeFilter(docs={self.docs}, tags_any_of={self.tags_any_of}, tags_all_of={self.tags_all_of})"

    def __str__(self):
        return f"KnowledgeFilter(docs={self.docs}, tags_any_of={self.tags_any_of}, tags_all_of={self.tags_all_of})"

def and_filters(filter1: KnowledgeFilter | None, filter2: KnowledgeFilter | None):
    if filter1 is None:
        return filter2
    elif filter2 is None:
        return filter1
    else:
        # docs
        if filter1.docs is None:
            docs = filter2.docs
        elif filter2.docs is None:
            docs = filter1.docs
        else:
            # intersection
            docs1 = filter1.docs if isinstance(filter1.docs, Sequence) and not isinstance(filter1.docs, str) else [cast(str, filter1.docs)]
            docs2 = filter2.docs if isinstance(filter2.docs, Sequence) and not isinstance(filter2.docs, str) else [cast(str, filter2.docs)]

            docs = list(set(docs1) & set(docs2))

        # tags_any_of
        if filter1.tags_any_of is None:
            tags_any_of = filter2.tags_any_of
        elif filter2.tags_any_of is None:
            tags_any_of = filter1.tags_any_of
        else:
            # union
            tags_any_of1 = filter1.tags_any_of if isinstance(filter1.tags_any_of, Sequence) and not isinstance(filter1.tags_any_of, str) else [cast(str, filter1.tags_any_of)]
            tags_any_of2 = filter2.tags_any_of if isinstance(filter2.tags_any_of, Sequence) and not isinstance(filter2.tags_any_of, str) else [cast(str, filter2.tags_any_of)]

            tags_any_of = list(set(tags_any_of1) | set(tags_any_of2))

        # tags_all_of
        if filter1.tags_all_of is None:
            tags_all_of = filter2.tags_all_of
        elif filter2.tags_all_of is None:
            tags_all_of = filter1.tags_all_of
        else:
            # union
            tags_all_of1 = filter1.tags_all_of if isinstance(filter1.tags_all_of, Sequence) and not isinstance(filter1.tags_all_of, str) else [cast(str, filter1.tags_all_of)]
            tags_all_of2 = filter2.tags_all_of if isinstance(filter2.tags_all_of, Sequence) and not isinstance(filter2.tags_all_of, str) else [cast(str, filter2.tags_all_of)]

            tags_all_of = list(set(tags_all_of1) | set(tags_all_of2))

        return KnowledgeFilter(
            docs=docs,
            tags_any_of=tags_any_of,
            tags_all_of=tags_all_of
        )


class DataSource(BaseModel):
    """Data source for a knowledge base."""

    location: PathLike | str = Field(
        description="Location of the data source, e.g. a file path or URL."
    )
    name: str = Field(
        description="Name of the data source. Can be used for filtering in the knowledgebase and important that document names are unique"
    )
    tags: list[str] = Field(
        default=[],
        description="Tags applied to all documents and chunks of the source, e.g. 'finance'.",
    )
    incremental: bool = Field(
        default=False,
        description="Whether to do incremental indexing of the data source.",
    )

class KnowledgebaseMetadata(BaseModel):
    """Metadata for a knowledgebase."""

    name: str
    description: str | None = None
    tags: dict[str, str] = {}
    collection: str
    doc_summarize: bool = False
    doc_autotag: bool = False
    data_sources: List[Dict] = []

    class Config:
        extra = 'ignore'

class Knowledgebase:
    def __init__(self, **kwargs):
        print(f"Knowledgebase init: {kwargs}", flush=True)
        self.metadata = KnowledgebaseMetadata.model_validate(kwargs)

    @property
    def tags(self):
        """Get the tags for the workflow."""
        return self.metadata.tags

    @property
    def name(self):
        """Get the name of the workflow."""
        return self.metadata.name

    @property
    def description(self):
        """Get the description of the workflow."""
        return self.metadata.description

    def retrieve(
        self,
        query: str,
        limit: int,
        filter: KnowledgeFilter | None = None,
        **kwargs,
    ):
        """Retrieve documents from the knowledge base."""
        raise NotImplementedError

    def get_documents(
        self,
        filter: KnowledgeFilter | None = None,
    ) -> Iterator[Document]:
        """Get all documents from the knowledge base."""
        raise NotImplementedError


class RWKnowledgebase(Knowledgebase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def index(self, data_source: Optional[DataSource] = None):
        """Do an index run on either a provides data source or data sources defined in its config.

        Args:
            data_source (DataSource): Data source to index. If None, will use the data sources defined in the config.
        """
        raise NotImplementedError

    def set_tags(
        self,
        doc_id: str,
        tags: list[str],
    ):
        """Add tags to a document."""
        raise NotImplementedError
