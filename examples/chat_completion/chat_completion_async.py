from os import environ
import asyncio
import openai

from mona_openai import monitor

openai.api_key = environ.get("OPEN_AI_KEY")

MONA_API_KEY = environ.get("MONA_API_KEY")
MONA_SECRET = environ.get("MONA_SECRET")
MONA_CREDS = {
    "key": MONA_API_KEY,
    "secret": MONA_SECRET,
}

# This is the name of the monitoring class on Mona
MONITORING_CONTEXT_NAME = "MONITORED_CHAT_COMPLETION_USE_CASE_NAME"

monitored_chat_completion = monitor(
    openai.ChatCompletion,
    MONA_CREDS,
    MONITORING_CONTEXT_NAME,
)


response = asyncio.run(
    monitored_chat_completion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "I want to generate some text about "}
        ],
        max_tokens=20,
        n=1,
        temperature=0.2,
        # Adding additional information for monitoring purposes, unrelated to
        # internal OpenAI call.
        MONA_additional_data={"customer_id": "A531251"},
    )
)

print(response.choices[0].message.content)
