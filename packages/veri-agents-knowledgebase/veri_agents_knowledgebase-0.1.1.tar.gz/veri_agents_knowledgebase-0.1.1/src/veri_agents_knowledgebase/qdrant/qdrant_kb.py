import logging
from typing import Iterator

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models
from qdrant_client.models import Filter
from veri_agents_knowledgebase.knowledgebase import Knowledgebase, KnowledgeFilter, and_filters
from veri_agents_knowledgebase.qdrant.qdrant_doc_store import QdrantDocStore

log = logging.getLogger(__name__)


class QdrantKnowledgebase(Knowledgebase):
    def __init__(
        self,
        vectordb_url: str,
        embedding_model: Embeddings,
        filter: KnowledgeFilter | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.chunks_collection_name = f"chunks_{self.metadata.collection}"
        self.docs_collection_name = f"docs_{self.metadata.collection}"
        self.filter = filter
        # self.records_namespace = f"qdrant/{self.chunks_collection_name}"
        # self.docs_namespace = f"qdrant/{self.docs_collection_name}"

        self.embedding_model = embedding_model

        log.info(f"Connecting to Qdrant at {vectordb_url}")
        self.qdrant = QdrantClient(vectordb_url)
        sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
        self.vector_store = QdrantVectorStore(
            client=self.qdrant,
            collection_name=self.chunks_collection_name,
            # FIXME
            embedding=self.embedding_model,# pyright: ignore[reportArgumentType]
            retrieval_mode=RetrievalMode.HYBRID,
            vector_name="dense",
            sparse_embedding=sparse_embeddings,
            sparse_vector_name="sparse",
        )
        self.doc_store = QdrantDocStore(
            client=self.qdrant, collection_name=self.docs_collection_name
        )

    def retrieve(
        self,
        query: str,
        limit: int,
        filter: KnowledgeFilter | None = None,
        **kwargs,
    ):
        # for now let's do naive retrieval
        qdrant_filter = self._create_qdrant_filter(and_filters(filter, self.filter))
        log.info(f"Qdrant Filter: {qdrant_filter}")
        return self.vector_store.similarity_search(query, k=limit, filter=qdrant_filter)

    def get_documents(
        self,
        filter: KnowledgeFilter | None = None,
    ) -> Iterator[Document]:
        qdrant_filter = self._create_qdrant_filter(and_filters(filter, self.filter))
        return self.doc_store.yield_documents(filter=qdrant_filter)

    def _create_qdrant_filter(
        self,
        filter: KnowledgeFilter | None = None,
    ):
        """Create a Qdrant filter from the knowledgebase filter.
        Args:
            filter (KnowledgeFilter): The knowledge filter to convert.
        Returns:
            Filter: The Qdrant filter.
        """
        if not filter:
            return None

        must = []
        # doc filter means all the documents in the list (so a should clause)
        if filter.docs:
            doc_filter = filter.docs
            if isinstance(filter.docs, str):
                doc_filter = [filter.docs]
            should = []
            for doc_id in doc_filter:
                should.append(
                    models.FieldCondition(
                        key="metadata.source", match=models.MatchValue(value=doc_id)
                    )
                )
            must.append(Filter(should=should))
        if filter.tags_any_of:
            tag_any_filter = filter.tags_any_of
            if isinstance(filter.tags_any_of, str):
                tag_any_filter = [filter.tags_any_of]
            should = []
            for tag in tag_any_filter:
                should.append(
                    models.FieldCondition(
                        key="metadata.tags",
                        match=models.MatchValue(value=tag),
                    )
                )
            must.append(Filter(should=should))
        if filter.tags_all_of:
            tag_all_filter = filter.tags_all_of
            if isinstance(filter.tags_all_of, str):
                tag_all_filter = [filter.tags_all_of]
            for tag in tag_all_filter:
                must.append(
                    models.FieldCondition(
                        key="metadata.tags",
                        match=models.MatchValue(value=tag),
                    )
                )
        return Filter(must=must) if must else None
