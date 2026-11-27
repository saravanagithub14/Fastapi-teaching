# ---------------------------------------------------------------------------
# main.py - A small chatbot web app.
#
# How it works:
#   1. The browser loads the chat page (static/index.html) from this server.
#   2. When the user sends a message, the page POSTs it to the /chat endpoint.
#   3. /chat forwards the message to OpenAI and returns the model's reply.
#   4. The page shows the reply in the chat window.
#
# Run it with:  .\venv\Scripts\python.exe main.py
# Then open:    http://127.0.0.1:8000
# ---------------------------------------------------------------------------

# Imports:
#   os          - reads environment variables (like the API key)
#   load_dotenv - loads variables from the .env file
#   FastAPI     - the web framework; HTTPException returns HTTP errors
#   StaticFiles - serves plain files (HTML/CSS/JS) from a folder
#   OpenAI      - the official OpenAI client library
#   BaseModel   - validates the shape of incoming JSON data
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel

# Load environment variables.
# load_dotenv() reads the .env file in this folder and adds each KEY=value line
# to the process environment, so os.getenv("OPENAI_API_KEY") can find it.
# This keeps the secret key out of the source code.
load_dotenv()

# Initialize OpenAI.
# One client is created when the app starts and reused for every request,
# which is faster than creating a new client each time.
# If OPENAI_API_KEY is missing, api_key will be None and requests will fail.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI application.
# "app" is the object uvicorn runs. The title appears on the auto-generated
# API docs page at http://127.0.0.1:8000/docs
app = FastAPI(title="My OpenAI Chatbot")


# Define the message structure.
# Every request to /chat must be JSON shaped like: {"message": "some text"}
# Pydantic checks this automatically; if "message" is missing or not a string,
# FastAPI rejects the request with a 422 error before our code even runs.
class ChatRequest(BaseModel):
    message: str  # The text the user typed in the chat box


# Create chatbot endpoint.
# @app.post("/chat") registers this function to handle POST requests to /chat.
# FastAPI reads the JSON body, validates it against ChatRequest, and passes
# it in as the "request" argument.
@app.post("/chat")
async def chat(request: ChatRequest):

    try:
        # Send the user's message to OpenAI using the Responses API.
        #   model - which OpenAI model generates the reply
        #   input - the user's message text
        # Note: each call is independent, so the bot does not remember
        # earlier messages in the conversation.
        response = client.responses.create(
            model="gpt-5-mini",
            input=request.message
        )

        # response.output_text is a convenience property that joins all the
        # text the model produced into one string.
        # FastAPI converts this dict to JSON: {"reply": "..."}
        return {
            "reply": response.output_text
        }

    except Exception as e:
        # If anything goes wrong (bad API key, network problem, rate limit...),
        # return an HTTP 500 error with a friendly message instead of crashing.
        # The page shows this "detail" text to the user.
        # Tip: add print(e) here while debugging to see the real error
        # in the terminal.
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the response."
        )


# Serve frontend.
# Mounts the "static" folder at the site root "/", so visiting
# http://127.0.0.1:8000/ returns static/index.html.
#   html=True - serve index.html automatically when a folder URL is requested
# This must come AFTER the /chat route: a mount at "/" matches every path,
# so routes defined before it are checked first.
# The app will refuse to start if the "static" folder does not exist.
app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)


# Start the server when run directly with "python main.py".
# This block is skipped when another tool imports the file
# (for example: uvicorn main:app --reload).
if __name__ == "__main__":
    import uvicorn  # The ASGI server that actually runs the FastAPI app

    # host="127.0.0.1" - only this computer can reach the app
    #                    (use "0.0.0.0" to allow other devices on your network)
    # port=8000        - the app is available at http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
