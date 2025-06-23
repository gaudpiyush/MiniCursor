from dotenv import load_dotenv
import os
import time
import json
import google.generativeai as genai

# Load .env and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# === Tool Functions ===
def run_command(cmd: str):
    print(f"📟 Running: {cmd}")
    result = os.system(cmd)
    return f"✅ Command executed: {cmd}" if result == 0 else f"❌ Failed: {cmd}"

def write_file(path: str, content: str):
    try:
        with open(path, "w") as file:
            file.write(content)
        return f"✅ File written: {path}"
    except Exception as e:
        return f"❌ Error: {e}"

# Tool Map
available_tools = {
    "run_command": run_command,
    "write_file": write_file,
}

# === System Prompt ===
SYSTEM_PROMPT = """
You are Tecy — an AI assistant that builds basic frontend apps using HTML, CSS, and JS. 
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


Available tools:
- run_command: runs Ubuntu shell commands
- write_file: writes code into files

Only build HTML/CSS/JS projects.
Keep the user updated step-by-step.
"""

# === Start Chat ===
messages = [{"role": "user", "parts": [SYSTEM_PROMPT]}]
chat = model.start_chat(history=messages)

# === Main Loop ===
while True:
    query = input("\n> ")
    response = chat.send_message(f"{query}\nStart planning.")
    time.sleep(2)

    while True:
        raw = response.text.strip()
        print(f"\n📩 Gemini Raw:\n{raw}\n")

        # Clean up response
        if raw.startswith("```json"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        if not raw:
            print("❌ Gemini returned empty output.")
            break

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            print("❌ Invalid JSON:\n", raw)
            break

        step = parsed.get("step")
        content = parsed.get("content")
        tool = parsed.get("function")
        tool_input = parsed.get("input")

        if step == "plan":
            plan_info = parsed.get("content") or parsed.get("description") or parsed.get("message") or parsed.get("plan", {}).get("description")
            print(f"\n🧠 PLAN: {plan_info}")    
            response = chat.send_message("Continue to next step. Respond ONLY in JSON format.")
            time.sleep(2)
            continue

        if step == "action":
            print(f"\n🛠️ ACTION: {tool}")

            if tool == "write_file":
                try:
                    if isinstance(tool_input, str):
                        tool_input = tool_input.strip()

                        # Remove code fences like ```html, ```css, ```js, etc.
                        if tool_input.startswith("```"):
                            tool_input = "\n".join(tool_input.split("\n")[1:-1]).strip()

                        if "\n" in tool_input:
                            split_index = tool_input.index("\n")
                            filename = tool_input[:split_index].strip()
                            content = tool_input[split_index + 1:].strip()
                        else:
                            raise ValueError("Filename and content not properly formatted")

                        result = write_file(filename, content)
                        print(f"📁 {result}")

                    elif isinstance(tool_input, dict):
                        for file_name, file_content in tool_input.items():
                            result = write_file(file_name, file_content)
                            print(f"📁 {result}")

                except Exception as e:
                    print(f"❌ Error writing files: {e}")
                    break

            elif tool in available_tools:
                result = available_tools[tool](tool_input)
                print(f"📁 {result}")
            else:
                print("❌ Unknown tool:", tool)
                break

            # Send observation
            response = chat.send_message(json.dumps({
                "step": "observe",
                "output": "Tool executed successfully."
            }))
            time.sleep(2)

            # Handle next step
            raw = response.text.strip()
            print(f"\n📩 Gemini Follow-Up:\n{raw}\n")

            if raw.startswith("```json"):
                raw = raw.replace("```json", "").replace("```", "").strip()

            try:
                parsed = json.loads(raw)
                step = parsed.get("step")
                content = parsed.get("content") or parsed.get("description") or parsed.get("message") or parsed.get("result")

                if step == "output":
                    print(f"\n🤖 OUTPUT: {content}")
                    break
                else:
                    response = chat.send_message("Continue to next step.")
                    time.sleep(2)
                    continue
            except Exception as e:
                print("⚠️ Couldn't parse follow-up step:", e)
                break

        if step == "output":
            output_info = parsed.get("content") or parsed.get("description") or parsed.get("message") or parsed.get("result")
            print(f"\n🤖 OUTPUT: {output_info}")
            break
