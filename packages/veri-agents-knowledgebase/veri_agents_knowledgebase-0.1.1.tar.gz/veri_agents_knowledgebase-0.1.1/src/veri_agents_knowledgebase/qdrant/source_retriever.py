import uuid
from typing import Any, List, Optional, Tuple, Sequence

from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter

from langchain.retrievers import MultiVectorRetriever


class SourceDocumentRetriever(MultiVectorRetriever):
    """ Retrieve small chunks and return the full source document.

    This is a special case of the ParentDocumentRetriever but we don't want
    a full parent doc to be split into chunks but we already have chunks 
    available due to the structured nature of the data we got.

            )
    """  # noqa: E501

    child_splitter: TextSplitter
    """The text splitter to use to create child documents."""

    """The key to use to track the parent id. This will be stored in the
    metadata of child documents."""
    parent_splitter: Optional[TextSplitter] = None
    """The text splitter to use to create parent documents.
    If none, then the parent documents will be the raw documents passed in."""

    child_metadata_fields: Optional[Sequence[str]] = None
    """Metadata fields to leave in child documents. If None, leave all parent document 
        metadata.
    """

    # TODO: shall we split parents as well and then add them to the docstore as ID#1, ID#2, etc?
    def _split_docs_for_adding(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None,
        add_to_docstore: bool = True,
    ) -> Tuple[List[Document], List[Tuple[str, Document]]]:
        if self.parent_splitter is not None:
            documents = self.parent_splitter.split_documents(documents)
        if ids is None:
            doc_ids = [str(uuid.uuid4()) for _ in documents]
            if not add_to_docstore:
                raise ValueError(
                    "If ids are not passed in, `add_to_docstore` MUST be True"
                )
        else:
            if len(documents) != len(ids):
                raise ValueError(
                    "Got uneven list of documents and ids. "
                    "If `ids` is provided, should be same length as `documents`."
                )
            doc_ids = ids

        docs = []
        full_docs = []
        for i, doc in enumerate(documents):
            _id = doc_ids[i]
            sub_docs = self.child_splitter.split_documents([doc])
            if self.child_metadata_fields is not None:
                for _doc in sub_docs:
                    _doc.metadata = {
                        k: _doc.metadata[k] for k in self.child_metadata_fields
                    }
            for _doc in sub_docs:
                _doc.metadata[self.id_key] = _id
            docs.extend(sub_docs)
            full_docs.append((_id, doc))

        return docs, full_docs

    def add_documents(
        self,
        parent_document: Document,
        child_documents: List[Document],
        id_key: str = "source",
        ids: Optional[List[str]] = None,
        add_to_docstore: bool = True,
        **kwargs: Any,
    ) -> None:
        """Adds documents to the docstore and vectorstores.

        Args:
            documents: List of documents to add
            ids: Optional list of ids for documents. If provided should be the same
                length as the list of documents. Can be provided if parent documents
                are already in the document store and you don't want to re-add
                to the docstore. If not provided, random UUIDs will be used as
                ids.
            add_to_docstore: Boolean of whether to add documents to docstore.
                This can be false if and only if `ids` are provided. You may want
                to set this to False if the documents are already in the docstore
                and you don't want to re-add them.
        """
        for doc in child_documents:
            doc.metadata[self.id_key] = parent_document.metadata[self.id_key]
        self.vectorstore.add_documents(child_documents, **kwargs)
        if add_to_docstore:
            self.docstore.mset([(parent_document.metadata[self.id_key], parent_document)])

    async def aadd_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None,
        add_to_docstore: bool = True,
        **kwargs: Any,
    ) -> None:
        docs, full_docs = self._split_docs_for_adding(documents, ids, add_to_docstore)
        await self.vectorstore.aadd_documents(docs, **kwargs)
        if add_to_docstore:
            await self.docstore.amset(full_docs)
