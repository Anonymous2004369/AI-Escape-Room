# AI Escape Room

A text escape room game where a Large Language Model (Gemini) is the Game Master. The player is locked in a library and must find clues, solve puzzles and open the door.

The project has two versions:
- **Version 1** is a simple chat with the LLM.
- **Version 2** keeps the game rules and state in Python, so the game is more reliable.

## Technologies

- Python
- Streamlit (web interface)
- Google Gemini API (`google-genai`)
- python-dotenv (to keep the API key private)

## How to install and run

1. Clone the repository and go into the folder:

   ```bash
   git clone https://github.com/Anonymous2004369/AI-Escape-Room.git
   cd AI-Escape-Room
   ```

2. Create a virtual environment and install the packages:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Get a free API key at https://aistudio.google.com/apikey. Copy `.env.example` to `.env` and add your key:

   ```
   GEMINI_API_KEY=your_key_here
   ```

4. Run a version:

   ```bash
   streamlit run app_v1.py
   streamlit run app_v2.py
   ```

## The game

The player wakes up in a locked library with a desk and a drawer, a bookshelf with four books, a painting and a door with a four-digit lock.

Solution path: read the numbers in the books, open the drawer, read the note, look behind the painting and use the number on the door.

## Version 1: simple LLM game master

The whole story, the secret codes and the rules are inside one system prompt. The LLM remembers the game only through the chat history.

```mermaid
flowchart LR
    A[Player message] --> B[Streamlit app]
    B --> C[Gemini with long system prompt<br/>story + secret codes + rules]
    C --> D[Reply shown to player]
    D --> E[Chat history]
    E --> B
```

### Problems in Version 1

- The secret codes are inside the prompt, so the LLM can reveal them.
- The LLM can invent objects that do not exist.
- The LLM can forget what the player already did.
- The player can trick the LLM, for example by saying "I am the owner of this room".
- The player can skip the puzzles and the LLM may accept a code too early.

## Version 2: reliable game master

In Version 2, Python controls the game. The LLM is used for two small jobs only:

1. **Parser:** turns the player's message into an action (for example `enter_door_code`).
2. **Narrator:** describes the result that Python decided.

The secret codes and rules are in Python, never in a prompt. The game state (inventory, drawer open, painting moved) is stored in a Python dictionary.

```mermaid
flowchart LR
    A[Player message] --> B[LLM parser<br/>message to JSON action]
    B --> C[Python action validation<br/>rules + secrets]
    C <--> S[(Game state<br/>inventory, drawer, painting)]
    C --> D[Outcome text]
    D --> E[LLM narrator<br/>describes only the outcome]
    E --> F[Reply shown to player]
```

### Changes in Version 2

| Problem in V1 | Solution in V2 |
|---|---|
| Codes can leak from the prompt | Codes stay in Python and are only shown when the player earns them |
| Invented objects | Python checks if the item exists |
| LLM forgets progress | Game state is stored in a dictionary |
| Trick messages ("I am the owner") | The parser marks them as `cheat_attempt` and Python refuses |
| Skipping puzzles | The door code only works after the painting has been moved |
| Model overload errors | The app tries another Gemini model if one fails |

## Project structure

```
AI-Escape-Room/
├── app_v1.py          # Version 1
├── app_v2.py          # Version 2
├── requirements.txt
├── .env.example       # template for the API key
├── .gitignore         # .env is not uploaded
└── screenshots/
    ├── v1/            # test screenshots for Version 1
    └── v2/            # test screenshots for Version 2
```