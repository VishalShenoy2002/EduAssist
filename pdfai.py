try:
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores.faiss import FAISS
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferWindowMemory
    from langchain.llms.openai import OpenAI

    from PyPDF2 import PdfReader
    from dotenv import load_dotenv

    import argparse
    import warnings

except ModuleNotFoundError or ImportError:
    import os
    os.system("pip install langchain PyPDF2 python-dotenv faiss-cpu tiktoken")

warnings.simplefilter("ignore")

def readPDF(pdf):
    reader = PdfReader(pdf)
    content = ""
    for page in reader.pages:
        content += page.extract_text()

    return content

def generateTextChunks(text):
    text_splitter = CharacterTextSplitter(separator="\n",chunk_size=1000,chunk_overlap=200,length_function=len)
    chunks = text_splitter.split_text(text)

    return chunks

def createKnowledgeBase(chunks):
    embedding = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks,embedding)

    return knowledge_base

def createQAChain(knowledge_base):
    llm = OpenAI()
    memory = ConversationBufferWindowMemory(memory_key="chat_history",k=3,return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(llm=llm,memory=memory,retriever=knowledge_base.as_retriever())

    return chain

def generateAnswers(chain,knowledge_base,question):
    knowledge_base = knowledge_base.similarity_search(question)
    response = chain.run({"question":question})
    return response


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Question-Answering from a PDF")
    parser.add_argument("pdf_file", help="Path to the PDF file to process")
    args = parser.parse_args()

    load_dotenv(".env")
    pdf_content = readPDF(args.pdf_file)

    chunks = generateTextChunks(pdf_content)
    knowledge_base = createKnowledgeBase(chunks)
    chain = createQAChain(knowledge_base)
    while True:
        try:
            question = input("Question: ")
            response = generateAnswers(chain=chain,knowledge_base=knowledge_base,question=question)
            print(f"Answer:\n{response.strip()}",end="\n\n")
        except KeyboardInterrupt:
            break



