import os
from time import sleep, time

import groq
from playwright.sync_api import ElementHandle, sync_playwright

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

            question_el = page.wait_for_selector("[data-functional-selector^='block-title']")
            assert question_el is not None
            question = question_el.inner_text()

            options: list[str] = []
            for element in page.query_selector_all(
                "[data-functional-selector^='answer-']"
            ):
                options.append(element.inner_text())

            start = time()
            answer = ask_groq_for_the_answer(question, options)
            elapsed = time() - start

            print(f"Answer: {answer}")
            print(f"Time: {elapsed:.2f}s")

            page.click(f"[data-functional-selector='answer-{answer}']")


def ask_groq_for_the_answer(question: str, options: list[str]) -> str:
    system_prompt = "Pick the correct option. Reply with only the number"

    content = f"Question: {question}\n"
    for i, option in enumerate(options):
        # Will look similar to "0) <option> "
        content += f"{i}) {option} "

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        temperature=0,  # we need predictable answers. creativity CANNOT be allowed in here.
        max_tokens=1,  # only generate one letter
        model="llama-3.1-8b-instant",  # Incredibly fast
    )

    # I choose 0 because... no reason really, just need *a* fallback
    fallback = "0"
    return chat_completion.choices[0].message.content or fallback


if __name__ == "__main__":
    main()
