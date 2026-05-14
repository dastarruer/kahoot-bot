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
        page.goto(
            "https://create.kahoot.it/solo?quizId=ed8e165f-27dc-4a90-94eb-f4692d01f75f&gameMode=normal"
        )
        page.get_by_text("OK, go!").click()

        while True:
            page.wait_for_selector("[data-functional-selector='answer-0']")

            question = page.query_selector("[data-functional-selector^='block-title-']")
            choices = []
            for element in page.query_selector_all(
                "[data-functional-selector^='answer-']"
            ):
                choices.append(element.inner_text())

            start = time()
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Pick the correct option. Reply with only the number",
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\n0) {choices[0]} 1) {choices[1]} 2) {choices[2]} 3) {choices[3]}",
                    },
                ],
                temperature=0,  # we need predictable answers. creativity CANNOT be allowed in here.
                max_tokens=1,  # only generate one letter
                model="llama-3.1-8b-instant",  # Incredibly fast
            )
            elapsed = time() - start

            answer = chat_completion.choices[0].message.content
            
            print(f"Answer: {answer}")
            print(f"Time: {elapsed:.2f}s")

            page.click(
                f"[data-functional-selector='answer-{answer}']"
            )


if __name__ == "__main__":
    main()
