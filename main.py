import os
from time import sleep, time

import groq
from playwright.sync_api import sync_playwright

client = groq.Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

question = "Which country has the highest population in the world?"
option_a = "India"
option_b = "China"
option_c = "USA"
option_d = "Nepal"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        # page.goto("https://kahoot.it")
        # page.fill("[placeholder='Game PIN']", "123456")
        # page.press("[placeholder='Game PIN']", "Enter")

        # Use a solo game for now
        page.goto("https://create.kahoot.it/solo?quizId=a238a5fe-edac-4b3b-92d9-dda6ef27af94&gameMode=normal")
        page.get_by_text("OK, go!").click()


    # start = time()
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "Pick the correct option. Reply with only the letter",
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Question: {question}\na) {option_a} b) {option_b} c) {option_c} d) {option_d}"
    #         }
    #     ],
    #     temperature=0, # we need predictable answers. creativity CANNOT be allowed in here.
    #     max_tokens=1, # only generate one letter
    #     model="llama-3.1-8b-instant" # Incredibly fast
    # )
    # elapsed = time() - start

    # print(f"Answer: {chat_completion.choices[0].message.content}")
    # print(f"Time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
