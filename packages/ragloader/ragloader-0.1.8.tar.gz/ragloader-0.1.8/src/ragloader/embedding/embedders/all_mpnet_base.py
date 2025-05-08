from langchain_huggingface import HuggingFaceEmbeddings

from ragloader.splitting import DocumentChunk
from ragloader.embedding import ChunkEmbedder, EmbeddedChunk


class AllMpnetBase(ChunkEmbedder):
    model_name: str = "sentence-transformers/all-mpnet-base-v2"
    vector_length: int = 768
    embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'token': "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"},
            encode_kwargs={'batch_size': 4}
        )

    def embed(self, chunk: DocumentChunk) -> EmbeddedChunk:
        embedding: list[float] = self.embeddings.embed_query(chunk.content)

        embedded_chunk: EmbeddedChunk = EmbeddedChunk(
            document_chunk=chunk, embedding=embedding, embedding_model=self.model_name
        )

        return embedded_chunk
