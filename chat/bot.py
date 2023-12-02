import os
import textwrap

import yaml
import openai
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter

from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

# with open(os.path.join(os.getcwd(), "config/env.yaml"), "r") as stream:
#     try:
#         env_variables = yaml.safe_load(stream)
#     except yaml.YAMLError as exc:
#         print(exc)

def get_q_and_a(openai_api_key, openai_api_base, deployment_name="dominic-gpt-35-turbo",
                openai_api_version="2023-03-15-preview", api_type="azure", temperature=0):
    # openai.api_type = env_variables['api_type']
    # openai.api_version = env_variables['api_version']
    # openai_api_base = env_variables['api_base']
    # openai_api_key = env_variables['api_key']

    openai.api_type = api_type
    openai.api_version = openai_api_version
    openai_api_base = openai_api_base
    openai_api_key = openai_api_key
    # messages = [{"role": "system", "content": f"you are news reporting robot,\n "
    #                                           f"you are now report world news in {datetime.datetime.now().strftime('%m/%d/%Y')}"}]
    llm = AzureChatOpenAI(deployment_name=deployment_name, temperature=temperature,
                          openai_api_version=openai_api_version,
                          openai_api_key=openai_api_key, openai_api_base=openai_api_base)
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=1, openai_api_key=openai_api_key)

    loader = DirectoryLoader('data', glob="*.txt", loader_cls=TextLoader)

    documents = loader.load()
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    from langchain.vectorstores import FAISS

    db = FAISS.from_documents(documents=docs, embedding=embeddings)
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, 
    rephrase the follow up question to be a standalone question.
    
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:""")

    qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                               retriever=db.as_retriever(),
                                               condense_question_prompt=CONDENSE_QUESTION_PROMPT,
                                               return_source_documents=True,
                                               verbose=False)
    return qa


def bot(qa):
    chat_history = []

    while True:
        query = input("user: ")
        if query == "clear":
            chat_history = []
        elif query == "quit":
            return True
        else:
            result = qa({"question": query, "chat_history": chat_history})
            answer = textwrap.fill(result["answer"], 80)
            print(f'\nbot: {answer}\n')
            chat_history.append((query, result["answer"]))

    return False


