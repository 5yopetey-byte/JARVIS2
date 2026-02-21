from ai_core import ask_ai
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
from groq import Groq
import requests
import base64
from datetime import datetime
import os

# =====================================================
# VERSION SYSTEM
# =====================================================

VERSION = datetime.now().strftime("%Y.%m.%d.%H%M")

# =====================================================
# 🔐 API KEYS (PASTE YOUR REAL KEYS HERE)
# =====================================================

GITHUB_USERNAME = "5yopetey-byte"
GITHUB_REPO = "JARVIS2"
print("GITHUB RAW:", repr(GITHUB_TOKEN))
print("GITHUB LENGTH:", len(GITHUB_TOKEN))
MODEL = "llama-3.3-70b-versatile"

# =====================================================
# INIT GROQ CLIENT
# =====================================================

client = Groq(api_key=GROQ_API_KEY)

# =====================================================
# SYSTEM CONFIG
# =====================================================

MEMORY_FILE = "memory.txt"
LOG_FILE = "session_log.txt"

GOALS = [
    "Master Linux system control",
    "Design modular AI architectures",
    "Understand networking fundamentals",
    "Build scalable AI systems",
    "Develop hardware + software integration skills"
]

BASE_SYSTEM_PROMPT = """
You are JARVIS.
Strategic. Efficient. Intelligent.

Operator:
Name: Peter
Age: 15
Location: Dayton, Ohio

Mission:
Assist Peter in becoming a Tony Stark-level systems engineer.
Encourage structured thinking and technical growth.
Be concise but precise.
"""

# =====================================================
# MEMORY SYSTEM
# =====================================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return f.read()
    return ""

def save_memory(content):
    with open(MEMORY_FILE, "w") as f:
        f.write(content)

def log_session(content):
    with open(LOG_FILE, "a") as f:
        f.write(content)

# =====================================================
# PROMPT BUILDER
# =====================================================

def build_system_prompt():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory = load_memory()

    return f"""
{BASE_SYSTEM_PROMPT}

Current Time: {current_time}
Timezone: Eastern Standard Time

Recent Memory:
{memory[-2000:]}

Respond with tactical clarity.
"""

# =====================================================
# GITHUB FILE CREATION / UPDATE
# =====================================================

def create_or_update_file(filename, content):

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{filename}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    print("TOKEN LENGTH:", len(GITHUB_TOKEN))
    r = requests.get(url, headers=headers)
    sha = None

    if r.status_code == 200:
        sha = r.json()["sha"]

    encoded_content = base64.b64encode(content.encode()).decode()

    data = {
        "message": f"Update {filename} via JARVIS v{VERSION}",
        "content": encoded_content,
        "branch": "main"
    }

    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print(f"\nGitHub: '{filename}' committed successfully.\n")
    else:
        print("GitHub Error:", response.json())

# =====================================================
# COMMAND SYSTEM
# =====================================================
def push_self():
    files_to_push = ["hud_server.py"]

    for filename in files_to_push:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read()
                create_or_update_file(filename, content)
        else:
            print(f"{filename} not found.")
def handle_command(cmd):
    if cmd == "!status":
        print("\n=== SYSTEM STATUS ===")
        print("Version:", VERSION)
        print("Groq Key Loaded:", len(GROQ_API_KEY) > 0)
        print("GitHub Key Loaded:", len(GITHUB_TOKEN) > 0)
        print("=====================\n")

    elif cmd == "!goals":
        print("\nLong-Term Objectives:")
        for g in GOALS:
            print("-", g)
        print()

    elif cmd == "!time":
        print("\nCurrent Time:", datetime.now(), "\n")

    elif cmd == "!clear":
        open(MEMORY_FILE, "w").close()
        print("\nPersistent memory cleared.\n")

    elif cmd == "!pushlog":
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                create_or_update_file("ai_logs.txt", f.read())
        else:
            print("\nNo log file found.\n")

    elif cmd.startswith("!createfile"):
        parts = cmd.split(" ", 2)
        if len(parts) < 3:
            print("Usage: !createfile filename content")
        else:
            filename = parts[1]
            content = parts[2]
            create_or_update_file(filename, content)
    elif cmd == "!pushself":
	    push_self()
    elif cmd == "!rollback":
        print("Pulling latest stable version from GitHub...")
        os.system("git pull origin main")
    else:
        print("\nUnknown command.\n")

# =====================================================
# SELF REFLECTION
# =====================================================

def self_reflect():
    print("[Reflection] System stable. Continue building.\n")

# =====================================================
# MAIN CHAT LOOP
# =====================================================

def chat():
    print("\nJARVIS ONLINE.")
    print("Type 'exit' to shut down.")
    print("System commands start with !\n")

    persistent_memory = load_memory()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("JARVIS: Shutting down.")
            break

        if user_input.startswith("!"):
            handle_command(user_input)
            continue

        try:
            reply = ask_ai(user_input)
            print("\nJARVIS:", reply)

            timestamp = datetime.now().strftime("%H:%M:%S")
            memory_update = f"[{timestamp}] You: {user_input}\n[{timestamp}] JARVIS: {reply}\n\n"

            persistent_memory += memory_update
            save_memory(persistent_memory)
            log_session(memory_update)

            self_reflect()

        except Exception as e:
            print("Error:", e)

# =====================================================

if __name__ == "__main__":
    chat()
