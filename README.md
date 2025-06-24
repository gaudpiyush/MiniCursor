
# 🛠️ MiniCursor: Frontend App Builder using Gemini API

MiniCursor is a terminal-based AI assistant that helps you generate simple HTML/CSS/JavaScript frontend projects step-by-step using [Gemini 1.5 Flash](https://ai.google.dev/).

---

## 📦 Features

- Interactive CLI-based assistant
- Uses Google Gemini 1.5 Flash API
- Follows a structured process: `start → plan → action → observe → output`
- Writes files (`index.html`, `styles.css`, `script.js`)
- Executes Ubuntu shell commands
- Returns all steps in clean JSON format
- Auto-detects and writes content using tools

---

## 🧰 Tools Used

- **Gemini 1.5 Flash** – AI assistant backend
- **dotenv** – for secure API key loading
- **OS module** – to execute shell commands
- **JSON** – communication and response handling

---

## 📁 Project Structure

```bash
project/
│
├── main.py            # MiniCursor assistant logic
├── .env               # Contains GEMINI_API_KEY
├── index.html         # Generated HTML (example)
├── styles.css         # Generated CSS (example)
└── script.js          # Generated JS (example)
```

---

## 🔑 .env Format

```
GEMINI_API_KEY=your_api_key_here
```

---

## 🧠 Workflow Overview

1. **User** types a prompt (e.g. "Build a calculator").
2. **Gemini** responds with a `plan` step (description of app).
3. **MiniCursor** sends the next request for `action`.
4. **Gemini** sends JSON with:
   - step: `action`
   - function: `"write_file"`
   - input: `{ "index.html": "<html>..." }`
5. **MiniCursor** writes files and observes.
6. **Gemini** sends an `output` with final result.

---

## ⚙️ Supported Functions

| Function       | Description                             |
|----------------|-----------------------------------------|
| `write_file`   | Writes one or more files to disk        |
| `run_command`  | Executes a shell command in Ubuntu      |

---

## 📜 System Prompt for Gemini

```
You are MiniCursor — an AI assistant that builds basic frontend apps using HTML, CSS, and JS. 
You follow the process: start → plan → action → observe → output.

Rules:
- Respond only in JSON format:
{
  "step": "action",
  "function": "write_file",
  "input": {
    "index.html": "<html>...</html>",
    "styles.css": "body { ... }",
    "script.js": "const x = ...;"
  }
}
- Always return tool input for `write_file` as a JSON object: { "filename": "file content" }.
- Do not use markdown code blocks (like ```html) inside JSON.

Only build HTML/CSS/JS projects.
Keep the user updated step-by-step.
```

---

## 💡 Example Input

```
> Build a to-do app
```

### Output JSON (from Gemini):

```json
{
  "step": "action",
  "function": "write_file",
  "input": {
    "index.html": "<html>...</html>",
    "styles.css": "body { ... }",
    "script.js": "const x = ...;"
  }
}
```

---

## 🚀 How to Run

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

---

## 🛡️ Error Handling

- Empty responses
- Invalid JSON from Gemini
- File writing issues
- Unknown tools

All are logged in terminal with appropriate emojis:
✅ Success, ❌ Fail, ⚠️ Warning

---

## ✅ Example Output

```
📟 Running: mkdir demo
✅ Command executed: mkdir demo

📁 File written: index.html
📁 File written: styles.css
📁 File written: script.js

🤖 OUTPUT: All files generated. Your project is ready!
```
