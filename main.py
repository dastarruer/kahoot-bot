import os

import groq

client = groq.Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

question = "Which country has the highest population in the world?"
option_a = "India"
option_b = "China"
option_c = "USA"
option_d = "Nepal"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a Kahoot bot. Given a question and multiple options, choose only ONE option by returning a, b, c, or d. Nothing else.",
        },
        {
            "role": "user",
            "content": f"Question: {question}\na) {option_a}\nb) {option_b}\nc) {option_c}\nd) {option_d}"
        }
    ],
    temperature=0, # we need predictable answers. creativity CANNOT be allowed in here.
    model="llama-3.3-70b-versatile"
)

def main():
    print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    main()
