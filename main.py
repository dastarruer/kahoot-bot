import os
from time import time

import groq

client = groq.Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

question = "Which country has the highest population in the world?"
option_a = "India"
option_b = "China"
option_c = "USA"
option_d = "Nepal"


def main():
    start = time()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Pick the correct option. Reply with only the letter",
            },
            {
                "role": "user",
                "content": f"Question: {question}\na) {option_a} b) {option_b} c) {option_c} d) {option_d}"
            }
        ],
        temperature=0, # we need predictable answers. creativity CANNOT be allowed in here.
        max_tokens=1, # only generate one letter
        model="llama-3.1-8b-instant" # Incredibly fast
    )
    elapsed = time() - start

    print(f"Answer: {chat_completion.choices[0].message.content}")
    print(f"Time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
