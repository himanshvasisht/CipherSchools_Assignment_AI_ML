# 🤖 Robo-Reviewer: The Smart Code Inspector!

Welcome to **Robo-Reviewer**! Have you ever built a giant castle out of Lego bricks? Writing computer code is just like that! But sometimes, we put a brick in the wrong spot or build a tower that is too wobbly. 

Robo-Reviewer is your **friendly robot helper** who scans your code castle, finds the wobbly parts, and tells you exactly how to fix them!

---

## 📸 Sneak Peek of the Dashboard
Here is what Robo-Reviewer looks like in action:

![Dashboard Preview](dashboard_preview.png)

---

## 🧸 How it Works (Explained for Kids!)

Robo-Reviewer does its job in 5 simple steps:

1. **🏰 Copying the Castle (Cloning)**: 
   You give Robo-Reviewer a link to your code castle on GitHub. It flies over, makes an exact copy of it, and brings it back to its workshop.
2. **🧩 Sorting the Blocks (Parsing)**: 
   Robo-Reviewer looks at all your code blocks and sorts them into piles (like sorting red bricks, blue bricks, and green bricks). It reads Python and JavaScript!
3. **🗺️ Drawing a Map (Graphing)**: 
   It draws a map showing which Lego blocks connect to each other. If one block is connected to *everything* else, it's a super-important block!
4. **🕵️ Finding the Wobbly Towers (Risk Routing)**: 
   Robo-Reviewer calculates which sections of code are the most complicated and wobbly. It picks the top wobbly spots to inspect closely.
5. **🤖 The Robot Council (Multi-Agent Panel)**: 
   Instead of just one robot looking at it, Robo-Reviewer calls a council of **four robot experts** to debate:
   * **🧹 Mr. Neat (Quality Agent)**: Checks if your blocks are clean and easy to read.
   * **🛡️ Officer Safe (Security Agent)**: Checks if there are any holes where bad guys (bugs or hackers) could sneak in.
   * **🏗️ Archie the Architect (Architecture Agent)**: Checks if the overall design of your castle is strong.
   * **🔧 Fixer-Upper (Repair Agent)**: Suggests a new set of instructions to repair the wobbly blocks!

---

## 🚀 How to Play (Run it Locally)

Follow these easy steps to run Robo-Reviewer on your computer:

### 1. Set Up the Project
Open your terminal (command prompt) and type:
```bash
# Create a virtual environment (a private room for our robot)
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install the robot dependencies
pip install -r requirements.txt
```

### 2. Configure Your API Key
Make a copy of the `.env.example` file and rename it to `.env`. Open it and paste your free **Gemini** or **OpenRouter** API key:
```text
GEMINI_API_KEY=your_gemini_key_here
# or
OPENROUTER_API_KEY=your_openrouter_key_here
```

### 3. Launch the Dashboard!
Run this command to open the beautiful interactive screen in your browser:
```bash
streamlit run frontend/app.py
```
Open your browser to: **http://localhost:8501**

---

## ☁️ How to Deploy for 100% Free!

Want to share Robo-Reviewer with your friends? You can host it on the internet for **completely free**!

### Method 1: Streamlit Community Cloud (Recommended)
1. **Put your code on GitHub**: Create a free GitHub account and upload this folder.
2. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. **Create a New App**: Click **"New App"**, then:
   * **Repository**: Select your uploaded repo.
   * **Main file path**: Type `frontend/app.py`.
4. **Add Your API Key**: Click on **Advanced Settings**, and in the **Secrets** box, paste:
   ```toml
   GEMINI_API_KEY = "your_free_gemini_key_here"
   # or
   OPENROUTER_API_KEY = "your_free_openrouter_key_here"
   ```
5. **Launch!** Click **Deploy**. Your app will be live on the web in 2 minutes!

### Method 2: Hugging Face Spaces
1. Sign up for a free account at [Hugging Face](https://huggingface.co).
2. Click **"New Space"**, choose **Streamlit** as your SDK, and select the **Free CPU Tier**.
3. Upload your files and add your `GEMINI_API_KEY` or `OPENROUTER_API_KEY` under the Space's **Secret Variables** in settings.
