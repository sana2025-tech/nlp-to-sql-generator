import os
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Write a SQL query to find the top 5 customers by total sales."}
    ]
)

print(response.choices[0].message.content)