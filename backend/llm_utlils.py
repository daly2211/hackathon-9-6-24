from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def get_llm_response(prompt, max_tokens=1):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-70b-versatile",
        temperature=0.0,
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content



def get_dataset():
    with open('dataset/dataset.txt', 'r') as file:
        text = file.read()

    return text
