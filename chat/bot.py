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

import datetime


with open(os.path.join(os.getcwd(), "config/env.yaml"), "r") as stream:
    try:
        env_variables = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

openai.api_type = env_variables['api_type']
openai.api_version = env_variables['api_version']
openai_api_base = env_variables['api_base']
openai_api_key= env_variables['api_key']

messages=[{"role": "system", "content": f"you are news reporting robot,\n "
                                        f"you are now report world news in {datetime.datetime.now().strftime('%m/%d/%Y')}"}]


# Init LLM and embeddings model
llm = AzureChatOpenAI(deployment_name="dominic-gpt-35-turbo", temperature=0, openai_api_version="2023-03-15-preview",
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

qa2 = ConversationalRetrievalChain.from_llm(llm=llm,
                                           retriever=db.as_retriever(),
                                           condense_question_prompt=CONDENSE_QUESTION_PROMPT,
                                           return_source_documents=True,
                                           verbose=False)

chat_history = []

while True:
    query = input("user: ")
    if query == "clear":
        chat_history = []
    else:
        result = qa2({"question": query, "chat_history": chat_history})
        answer = textwrap.fill(result["answer"], 80)
        print(f'\nbot: {answer}\n')
        chat_history.append((query, result["answer"]))


