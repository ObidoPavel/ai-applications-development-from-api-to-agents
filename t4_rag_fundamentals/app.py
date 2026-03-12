import os
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from commons.constants import OPENAI_API_KEY

_BASE_DIR = Path(__file__).resolve().parent
_INDEX_DIR = _BASE_DIR / "microwave_faiss_index"
_MANUAL_PATH = _BASE_DIR / "microwave_manual.txt"

_SYSTEM_PROMPT = """You are an assistant that answers questions about the microwave oven using only the information provided in the conversation.

The user message has two blocks:
- RAG CONTEXT: Information retrieved from the microwave manual based on the user's request.
- USER QUESTION: The user's actual question.

You must use only information from the RAG CONTEXT to answer. Do not use external knowledge. If the answer is not in the RAG CONTEXT, say that the information is not available in the manual. Do not answer questions that are unrelated to the microwave manual or that cannot be answered from the provided context."""

_USER_PROMPT = """##RAG CONTEXT:
{context}


##USER QUESTION:
{query}"""


class MicrowaveRAG:

    def __init__(self, embeddings: OpenAIEmbeddings, llm_client: ChatOpenAI):
        self.llm_client = llm_client
        self.embeddings = embeddings
        self.vectorstore = self._setup_vectorstore()

    def _setup_vectorstore(self) -> VectorStore:
        """
        Load existing FAISS index from disk or create a new one.
        Returns:
              VectorStore: Initialized FAISS vectorstore.
        """
        print("Setting up vector store...")
        if _INDEX_DIR.exists():
            vectorstore = FAISS.load_local(
                str(_INDEX_DIR),
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            print("Loaded existing FAISS index from disk.")
        else:
            vectorstore = self._create_new_index()
            print("Created and saved new FAISS index.")
        return vectorstore

    def _create_new_index(self) -> VectorStore:
        """
        Load the manual, split into chunks, embed, and save a new FAISS index.
        Returns:
              VectorStore: Newly created and saved FAISS vectorstore.
        """
        loader = TextLoader(str(_MANUAL_PATH))
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", "."],
        )
        chunks = splitter.split_documents(documents)
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        vectorstore.save_local(str(_INDEX_DIR))
        return vectorstore

    def retrieve_context(self, query: str, k: int = 4, score: float = 0.3) -> str:
        """
        Retrieve the context for a given query.
        Args:
              query (str): The query to retrieve the context for.
              k (int): The number of relevant documents(chunks) to retrieve.
              score (float): The similarity score between documents and query. Range 0.0 to 1.0.
        """
        results = self.vectorstore.similarity_search_with_relevance_scores(
            query, k=k, score_threshold=score
        )
        chunks = []
        for doc, relevance_score in results:
            print(f"Retrieved (Score: {relevance_score:.3f}): {doc.page_content}")
            chunks.append(doc.page_content)
        return "\n\n".join(chunks)

    def augment_prompt(self, query: str, context: str) -> str:
        """
        Inject retrieved context and user query into the prompt template.
        Args:
              query (str): The user's question.
              context (str): Retrieved context from the vectorstore.
        Returns:
              str: Formatted prompt ready for the LLM.
        """
        augmented = _USER_PROMPT.format(context=context, query=query)
        print(augmented)
        return augmented

    def generate_answer(self, augmented_prompt: str) -> str:
        """
        Send the augmented prompt to the LLM and return its response.
        Args:
              augmented_prompt (str): The prompt with injected context and query.
        Returns:
              str: The LLM-generated answer.
        """
        messages = [
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=augmented_prompt),
        ]
        response = self.llm_client.invoke(messages)
        content = response.content if response.content else ""
        print(content)
        return content


def main(rag: MicrowaveRAG) -> None:
    print("Welcome to Microwave Manual RAG. Ask a question about the microwave (or type 'quit' to exit).")
    while True:
        query = input("Your question: ").strip()
        if not query or query.lower() == "quit":
            break
        context = rag.retrieve_context(query)
        augmented_prompt = rag.augment_prompt(query, context)
        rag.generate_answer(augmented_prompt)


if __name__ == "__main__":
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    llm_client = ChatOpenAI(
        temperature=0.0, model="gpt-4o", api_key=OPENAI_API_KEY
    )
    rag = MicrowaveRAG(embeddings=embeddings, llm_client=llm_client)
    main(rag)