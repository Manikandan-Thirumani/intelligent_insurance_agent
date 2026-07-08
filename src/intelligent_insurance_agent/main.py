"""A small RAG-style CLI application for insurance documents and prompts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional, Sequence, Union

from .Model.chat import ChatMessage, ChatModel
from .RAG.embedding import embed_chunks
from .RAG.loader import load_documents
from .RAG.retriever import retrieve_similar_chunks
from .RAG.splitter import split_document
from .RAG.vectorstore import VectorStore


class InsuranceRAGApp:
    def __init__(self, vector_store: Optional[VectorStore] = None, chat_model: Optional[ChatModel] = None) -> None:
        self.vector_store = vector_store or VectorStore()
        self.chat_model = chat_model or ChatModel()
        self.chat_history: List[ChatMessage] = []

    def ingest_documents(self, paths: Sequence[Union[str, Path]]) -> int:
        documents = load_documents(list(paths))
        indexed_chunks = 0
        for document in documents:
            chunks = split_document(document)
            if not chunks:
                continue
            embedded_chunks = embed_chunks(chunks)
            self.vector_store.add_many(embedded_chunks)
            indexed_chunks += len(embedded_chunks)
        return indexed_chunks

    def answer_query(self, query: str) -> str:
        retrieved = retrieve_similar_chunks(query, self.vector_store, top_k=3)
        if retrieved:
            context = "\n".join(chunk for chunk, _ in retrieved)
        else:
            context = "No indexed documents available yet."

        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        response = self.chat_model.generate([ChatMessage(role="user", content=query), ChatMessage(role="assistant", content=prompt)])

        self.chat_history.append(ChatMessage(role="user", content=query))
        self.chat_history.append(ChatMessage(role="assistant", content=response))
        return response

    def run_cli(self) -> None:
        print("Insurance RAG assistant")
        print("Type 'upload <path>' to index a document or 'quit' to exit.")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in {"quit", "exit"}:
                break
            if user_input.lower().startswith("upload "):
                path = user_input[len("upload "):].strip()
                if not path:
                    print("Please provide a document path.")
                    continue
                count = self.ingest_documents([path])
                print(f"Indexed {count} chunks from {path}")
                continue

            response = self.answer_query(user_input)
            print(f"Assistant: {response}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Insurance RAG assistant")
    parser.add_argument("--document", action="append", default=[], help="Document path to index")
    parser.add_argument("--prompt", help="Prompt to answer immediately")
    args = parser.parse_args()

    app = InsuranceRAGApp()
    for document_path in args.document:
        app.ingest_documents([document_path])

    if args.prompt:
        print(app.answer_query(args.prompt))
        return

    app.run_cli()


if __name__ == "__main__":
    main()
