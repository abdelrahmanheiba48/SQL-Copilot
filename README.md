# SQL Database Copilot

A RAG-based AI assistant that lets users ask questions about a SQL Server database using natural language.

Instead of manually writing SQL queries, the system retrieves relevant database schema and business rules, then uses an LLM to generate the appropriate T-SQL query.

### How it works

**User Question → RAG → LLM → SQL Query → Validation → Result**

The RAG system provides the LLM with information about the database structure, relationships, and business rules so it can better understand the database before generating SQL.

### Tech Stack

* Python
* SQL Server
* SQL / T-SQL
* RAG
* Embeddings
* ChromaDB
* Pandas
* LLMs

### Project Goal

The goal of this project is to explore how RAG and LLMs can be used to build a practical **Natural Language → SQL** system that can interact with real-world databases.

This project is still under development, with more features planned such as result explanations, visualizations, follow-up questions, and evaluation.
