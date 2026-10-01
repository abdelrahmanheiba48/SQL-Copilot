import chromadb
from sentence_transformers import SentenceTransformer
from documents import documents, metadatas 
from google import genai
from google.genai import types
import time

#embedding_model

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = embedding_model.encode(
    documents,
    batch_size=8,
    show_progress_bar=True
).tolist()

print("Documents:", len(documents))
print("Embeddings:", len(embeddings))
print("Vector size:", len(embeddings[0]))

#VectorDB
client = chromadb.EphemeralClient()
collection = client.create_collection('sql_schema_collection')

ids = [f"table_{i}" for i in range(len(documents))]

collection.add(
    ids = ids,
    documents = documents,
    metadatas=metadatas,
    embeddings=embeddings
)
print("Documents in Chroma:", collection.count())

# Retrival 

def retrieve(question , k = 3) :
    query_embeddings = embedding_model.encode([question]).tolist()

    result = collection.query(
        query_embeddings=query_embeddings,
        n_results=k
    )
    return result
'''
question = "Which tables contain customer information?"

results = retrieve(question)

print(results)

'''



def build_context(results):

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context
'''
question = "Which tables contain customer information?"

results = retrieve(question)

context = build_context(results)

print(context)
'''

# Prompt Engineering for RAG


def generate_sql(question: str, context: str) -> str:

    prompt = f"""
You are a SQL Server expert.

Generate a valid T-SQL query based only on the schema below.

DATABASE SCHEMA:
{context}

USER QUESTION:
{question}

RULES:
- Use only tables and columns present in the schema.
- Do not invent tables or columns.
- Return only the SQL query.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0
                )
            )

            return response.text.strip()

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < 2:
                time.sleep(5)

    return "Failed to generate SQL."

#=====================================================================================================


"""
question = "What table stores customer records?"

results = retrieve(question)

context = build_context(results)

prompt = generate_sql(question, context)

print(prompt)

"""

# LLM
API_KEY = "..."

# creating the client
client = genai.Client(api_key = API_KEY)




# test
question = "What table stores customer records?"

results = retrieve(question)

context = build_context(results)

sql = generate_sql(question, context)

print("Generated SQL:")
print(sql)
