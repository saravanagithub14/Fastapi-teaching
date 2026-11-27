# Build Your First AI Chatbot

## Roadmap: FastAPI backend → Swagger testing → HTML frontend

### Project goal

Build a simple OpenAI-powered chatbot in one continuous project. Start
with a Python backend, test it through Swagger UI, then create an
HTML/CSS/JavaScript interface and connect it to the same FastAPI
endpoint.

By the end, students will understand how a browser, backend API, and
OpenAI model communicate.

------------------------------------------------------------------------

## Final project structure

``` text
openai-chatbot/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

Keep the API key in `.env`. Never put it in frontend JavaScript or
commit it to GitHub.

------------------------------------------------------------------------

## Phase 1: Build the AI chatbot backend

**Main file:** `main.py`

### Learning objectives

-   Understand what an API is and why an application needs a backend.
-   Understand FastAPI and how to create an application.
-   Learn the difference between HTTP GET and POST methods.
-   Create an endpoint such as `POST /chat`.
-   Use Pydantic models to define and validate incoming request data.
-   Connect the backend to the OpenAI API.
-   Return the model's response as JSON.

### Build tasks

1.  Create the project folder and Python virtual environment.
2.  Install FastAPI, Uvicorn, OpenAI SDK, and python-dotenv.
3.  Create `requirements.txt`.
4.  Store the OpenAI API key in `.env`.
5.  Create the FastAPI application in `main.py`.
6.  Define a `ChatRequest` model with a `message` field.
7.  Create the `POST /chat` endpoint.
8.  Call the OpenAI Responses API from the endpoint.
9.  Return the generated answer in a JSON response.
10. Run the application locally with Uvicorn.

### Key concepts

-   `FastAPI()`
-   `@app.post("/chat")`
-   `BaseModel`
-   Request body
-   JSON
-   Environment variables
-   OpenAI Responses API
-   Uvicorn

### Checkpoint

Run the backend locally and confirm that the server starts without
errors.

------------------------------------------------------------------------

## Phase 2: Test the backend using Swagger UI

**Documentation URL:** `http://127.0.0.1:8000/docs`

### Learning objectives

-   Understand what Swagger UI is.
-   Understand the OpenAPI specification.
-   Explore API methods, paths, request bodies, and schemas.
-   Send a request without building a frontend.
-   Read responses and HTTP status codes.
-   Understand automatic request validation.

### Demonstration

1.  Open `/docs` in the browser.

2.  Expand `POST /chat`.

3.  Click **Try it out**.

4.  Enter a request body:

    ``` json
    {
      "message": "Explain artificial intelligence in simple terms"
    }
    ```

5.  Click **Execute**.

6.  Inspect the response body and status code.

7.  Explain how the request reached FastAPI and how the response came
    back.

### Deliberate error test

Send an invalid request:

``` json
{
  "text": "Hello"
}
```

Discuss why the request fails: the model expects a required `message`
field. Explain the `422 Unprocessable Entity` response and the
validation details.

### Optional extension

Add a simple health-check endpoint:

``` python
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "application": "OpenAI Chatbot"
    }
```

Refresh Swagger UI and test `GET /health`.

### Checkpoint

Students can successfully send a message through Swagger UI, inspect the
response, and explain a validation error.

------------------------------------------------------------------------

## Phase 3: Build the frontend

**Files:** `static/index.html`, `static/style.css`, and
`static/script.js`

Do not start this phase until the backend works through Swagger. This
makes it clear that the frontend is a separate way to interact with the
same API.

### Learning objectives

-   Understand the basic structure of an HTML page.
-   Use CSS to style a chat interface.
-   Use JavaScript to read user input and update the page.
-   Understand `fetch()`, HTTP POST, JSON, and `async/await`.

### Build tasks

1.  Create the `static` folder.
2.  Create `index.html` with a chat area, text input, and Send button.
3.  Move styling into `style.css`.
4.  Create `script.js`.
5.  Read the user's message from the input field.
6.  Use `fetch()` to send a POST request to `/chat`.
7.  Set the request header to `Content-Type: application/json`.
8.  Convert the message into JSON using `JSON.stringify()`.
9.  Read the JSON response.
10. Display the chatbot's reply in the chat area.
11. Handle empty messages and API errors.
12. Safely insert user and assistant text into the page. Prefer
    `textContent` or DOM elements over inserting untrusted text with
    `innerHTML`.

### Core request example

``` javascript
const response = await fetch("/chat", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        message: userMessage
    })
});

const data = await response.json();
```

### Checkpoint

The chat interface is visible in the browser and can collect a message.
The frontend request can be inspected in the browser's Developer Tools
under Network.

------------------------------------------------------------------------

## Phase 4: Connect the frontend and backend

### Learning objectives

-   Understand the complete request-response cycle.
-   Explain how JavaScript communicates with FastAPI.
-   Understand why the frontend does not call OpenAI directly.
-   Trace a message from the browser to the model and back.

### Request flow

1.  The user types a message in the browser.
2.  JavaScript captures the message.
3.  `fetch()` sends an HTTP POST request to `/chat`.
4.  FastAPI receives and validates the request.
5.  The backend sends the prompt to OpenAI.
6.  OpenAI returns a generated response.
7.  FastAPI sends the response to the browser as JSON.
8.  JavaScript displays the answer in the chat interface.

### Serve the frontend with FastAPI

Mount the static directory in `main.py`:

``` python
from fastapi.staticfiles import StaticFiles

app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)
```

Place the mount after defining your API routes. The browser and API now
share the same origin, so a separate CORS setup is not needed for this
arrangement.

### Checkpoint

Open the application at `http://127.0.0.1:8000`, send a message through
the HTML interface, and receive an AI-generated answer.

------------------------------------------------------------------------

## Suggested classroom teaching sequence

  -----------------------------------------------------------------------
  Stage                   Instructor              Student outcome
                          demonstration           
  ----------------------- ----------------------- -----------------------
  1\. Backend             Build `main.py` and     A working API
                          connect OpenAI          

  2\. Swagger             Test `POST /chat` and   Understand API requests
                          inspect responses       and responses

  3\. Frontend            Build the chat page     A working chat
                          with HTML, CSS, and     interface
                          JavaScript              

  4\. Integration         Connect the page to     A complete
                          `/chat` using `fetch()` browser-based chatbot
  -----------------------------------------------------------------------

## Questions to ask students

Use these questions to connect each phase:

1.  If we don't have a frontend, how can we still communicate with our
    chatbot?
2.  What does Swagger send to the backend?
3.  If Swagger can send a request, can an HTML page send the same
    request?
4.  Which part of the application calls OpenAI?
5.  Why should the OpenAI API key stay on the backend?
6.  What happens between clicking Send and seeing the chatbot's reply?

## Final architecture

``` text
                 Browser
          ┌────────────────────┐
          │ HTML + CSS         │
          │ JavaScript         │
          └─────────┬──────────┘
                    │
             POST /chat
                    │
          ┌─────────▼──────────┐
          │ FastAPI backend    │
          │ main.py            │
          └─────────┬──────────┘
                    │
              OpenAI API
                    │
          ┌─────────▼──────────┐
          │ Generated response │
          └────────────────────┘

Swagger UI (/docs) independently tests the FastAPI endpoint.
```

## After the basic chatbot

Once the end-to-end chatbot works, introduce improvements one at a time:

1.  **Conversation memory:** send previous messages as conversation
    context.
2.  **Streaming responses:** display generated text as it arrives.
3.  **Chat history:** store conversations in a database such as MongoDB.
4.  **Authentication:** support individual user accounts.
5.  **RAG:** answer questions using a collection of documents.

These are follow-up modules. Keep the first classroom build focused on
one message going from the browser to FastAPI, through OpenAI, and back.
