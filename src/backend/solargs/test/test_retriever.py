#!/usr/bin/env python
# -*- coding:utf-8
from langchain.embeddings import SentenceTransformerEmbeddings

repo_id =r"D:\soloy\huggingface_model\pytorch_model\bge-large-zh"
embeddings = SentenceTransformerEmbeddings(model_name=repo_id)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import CharacterTextSplitter
loader = CSVLoader(file_path=r'C:\Users\Sikh0\Desktop\SmoothNLP金融新闻数据集样本20k.csv')
documents = loader.load()
# print(embeddings.embed_query("你好"))
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
db = FAISS.from_documents(texts, embeddings)
import time
# retriever = db.as_retriever()
while True:
    query = input("请输入查询：")
    start_time = time.time()
    docs = db.similarity_search_with_score(query)
    print(f"检索时间：{time.time() - start_time}秒")
    print(docs)