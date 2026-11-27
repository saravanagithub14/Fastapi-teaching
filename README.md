# My OpenAI Chatbot

A small chatbot web app built with **FastAPI** and the **OpenAI API**. You type a message on a web page, the Python server sends it to OpenAI, and the reply appears on the page.

This guide walks you through building the project from an empty folder, step by step. The commands are for **Windows PowerShell** (the default terminal in VS Code on Windows).

---

## How it works

```
Browser (static/index.html)
   │  1. You type a message and click Send
   │  2. The page sends  POST /chat  {"message": "..."}
   ▼
FastAPI server (main.py)
   │  3. The server forwards the message to OpenAI
   ▼
OpenAI API (model: gpt-5-mini)
   │  4. OpenAI returns the reply text
   ▼
FastAPI server  →  returns {"reply": "..."}  →  page shows the reply
```

## Final project layout

```
New folder/
├── .env              ← your secret OpenAI API key (never share this)
├── .gitignore        ← keeps .env and venv out of git
├── main.py           ← the FastAPI server
├── README.md         ← this file
├── static/
│   └── index.html    ← the chat web page
└── venv/             ← the Python virtual environment (created by you)
```

---

## Prerequisites

1. **Python 3.10 or newer.** This project was built with Python 3.12.
   Check your version:
   ```powershell
   python --version
   ```
   If Python isn't installed, download it from [python.org](https://www.python.org/downloads/). During setup, tick **"Add python.exe to PATH"**.

2. **An OpenAI API key.**
   - Sign in at [platform.openai.com](https://platform.openai.com/).
   - Open **API keys** and click **Create new secret key**.
   - Copy the key (it starts with `sk-`). You only see it once.
   - Your OpenAI account needs billing set up or credits for the API to work.

3. **A code editor.** VS Code is recommended.

---

## Step 1: Create the project folder

Create a folder for the project and open it in VS Code (**File → Open Folder**). Then open a terminal in VS Code (**Terminal → New Terminal**).

Or create it from the terminal:

```powershell
mkdir my-chatbot
cd my-chatbot
code .
```

All the following commands are run from inside this folder.

---

## Step 2: Create a virtual environment

A virtual environment ("venv") is a private copy of Python for this project. Packages you install go into it instead of your system Python, so different projects don't conflict.

```powershell
python -m venv venv
```

This creates a `venv` folder.

**Activate it** so `python` and `pip` use the venv:

```powershell
.\venv\Scripts\Activate.ps1
```

Your prompt should now start with `(venv)`.

> **If you get "running scripts is disabled on this system":** run this once, then try activating again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> You can also skip activation and call the venv's Python directly with `.\venv\Scripts\python.exe` wherever this guide says `python`.

---

## Step 3: Install the packages

```powershell
pip install fastapi uvicorn openai python-dotenv
```

What each package does:

| Package | Purpose |
|---|---|
| `fastapi` | The web framework that defines the `/chat` endpoint and serves the page |
| `uvicorn` | The server that runs the FastAPI app |
| `openai` | The official library for calling the OpenAI API |
| `python-dotenv` | Reads your API key from the `.env` file |

`pydantic`, which checks incoming data, is installed automatically with FastAPI.

*Optional:* save the exact versions so others can install the same ones:

```powershell
pip freeze > requirements.txt
```

Later, anyone can install everything with `pip install -r requirements.txt`.

---

## Step 4: Store your API key in a `.env` file

Create a file named `.env` (the name starts with a dot) in the project folder and add this line, with your real key in place of the placeholder:

```
OPENAI_API_KEY=sk-your-key-here
```

- No quotes and no spaces around `=`.
- The code reads the key from this file, so it never appears in `main.py`.

### Keep the key out of git

Create a file named `.gitignore` with:

```
.env
venv/
__pycache__/
```

This stops git from uploading your secret key and the large `venv` folder if you put the project on GitHub. If an API key is ever pushed publicly, delete it on the OpenAI website and create a new one.

---

## Step 5: Write the server (`main.py`)

Create `main.py` in the project folder. The full file, with comments explaining every part, is in this project's [main.py](main.py). Here is what it does, piece by piece.

### 5.1 Imports

```python
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel
```

### 5.2 Load the API key and create the OpenAI client

```python
load_dotenv()  # reads .env into the environment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

`load_dotenv()` must run before `os.getenv(...)`, otherwise the key isn't found.

### 5.3 Create the app

```python
app = FastAPI(title="My OpenAI Chatbot")
```

### 5.4 Describe the incoming data

```python
class ChatRequest(BaseModel):
    message: str
```

Every request to `/chat` must be JSON like `{"message": "Hello"}`. FastAPI rejects anything else with a `422` error.

### 5.5 Add the `/chat` endpoint

```python
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=request.message
        )
        return {"reply": response.output_text}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the response."
        )
```

- `client.responses.create(...)` sends the message to OpenAI.
- `response.output_text` is the model's reply as a single string.
- If anything fails (wrong key, no credits, no internet), the user gets a friendly error instead of a crash.

### 5.6 Serve the web page

```python
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```

This serves the files in the `static` folder, so `http://127.0.0.1:8000/` shows `static/index.html`. Keep it **below** the `/chat` route: a mount at `/` catches every path, so routes defined before it are matched first.

### 5.7 Start the server with `python main.py`

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Without this block, `python main.py` only loads the app and exits silently, with no output and no server.

---

## Step 6: Create the chat page (`static/index.html`)

1. Create a folder named `static` in the project folder.
2. Inside it, create `index.html`.

The full commented file is in this project's [static/index.html](static/index.html). It has three parts:

- **HTML:** a chat window (`<div id="log">`) and a form with a text box and a **Send** button.
- **CSS:** simple styling for the layout and message colors.
- **JavaScript:** when you click Send, it:
  1. shows your message in the chat window,
  2. sends it to the server:
     ```js
     const res = await fetch("/chat", {
       method: "POST",
       headers: { "Content-Type": "application/json" },
       body: JSON.stringify({ message })
     });
     ```
  3. reads the JSON response and shows `data.reply`, or `data.detail` if there was an error.

> The `static` folder must exist before you start the server. If it's missing, the app stops with `RuntimeError: Directory 'static' does not exist`.

---

## Step 7: Run the app

With the venv activated:

```powershell
python main.py
```

You should see:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The terminal stays busy while the server runs; that's normal.

**Alternative (auto-reload while developing):** this restarts the server every time you save a file:

```powershell
uvicorn main:app --reload
```

To stop the server, click the terminal and press **Ctrl+C**.

---

## Step 8: Use the chatbot

1. Open **http://127.0.0.1:8000** in your browser.
2. Type a message and press **Send** (or Enter).
3. The reply appears in the chat window.

Chat replies appear **on the web page**, not in the terminal. The terminal only logs each request, for example:

```
INFO:     127.0.0.1:63459 - "POST /chat HTTP/1.1" 200 OK
```

`200 OK` means the request succeeded.

### Test the API without the page (optional)

FastAPI creates an interactive API page at **http://127.0.0.1:8000/docs**. Open it, expand `POST /chat`, click **Try it out**, enter a message, and click **Execute**.

Or from a second PowerShell terminal:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/chat `
  -ContentType "application/json" `
  -Body '{"message": "Hello!"}'
```

---

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `python main.py` prints nothing and exits | The `if __name__ == "__main__":` block from step 5.7 is missing. Add it, or run `uvicorn main:app` instead. |
| `RuntimeError: Directory 'static' does not exist` | Create the `static` folder with `index.html` inside it (step 6). Run the command from the project folder. |
| `ModuleNotFoundError: No module named 'fastapi'` | The venv isn't active, or the packages aren't installed. Activate the venv (step 2) and run the install again (step 3). |
| Page shows "Something went wrong while generating the response." | The OpenAI call failed. Check the key in `.env`, that your OpenAI account has credits, and your internet connection. To see the real error, add `print(e)` inside the `except` block in `main.py` and watch the terminal. |
| `[Errno 10048] ... only one usage of each socket address` | Port 8000 is already in use, often by another copy of the server. Stop it with Ctrl+C, or change `port=8000` to another number such as `8001`. |
| "running scripts is disabled on this system" | See the note in step 2. |
| The page doesn't load | Make sure the server is running and you're using `http://127.0.0.1:8000`, not `https`. |

---

## Ideas for next steps

- **Conversation memory:** the bot currently treats every message on its own. Keep a list of earlier messages and send them with each request so it remembers the conversation.
- **Streaming replies:** show the answer word by word as it's generated.
- **Loading indicator:** show "Thinking..." while waiting for the reply.
- **Change the model:** edit `model="gpt-5-mini"` in `main.py` to try other OpenAI models.
- **System instructions:** pass `instructions="You are a helpful assistant who..."` to `client.responses.create(...)` to give the bot a personality or role.
