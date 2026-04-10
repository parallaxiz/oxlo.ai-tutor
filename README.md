# Codexa — AI Coding Tutor

> Learn to code. Think like a dev.

Codexa pairs frontier AI reasoning with a live coding lab — so every concept clicks, not just compiles. It's an AI-powered coding education platform designed to teach you the mental model behind the code, not just the correct syntax.

## Features

- 🧠 **Chain-of-Thought Reasoning**: Instructs step-by-step without giving away black-box answers.
- ⚡ **Live Coding Lab**: Features an integrated Monaco editor (same engine as VS Code) seamlessly running in your browser. Write, run, and get AI feedback instantly.
- 🎯 **Concept-First Learning**: Designed to teach you *why*, not just *what*. Understand the logic behind problems like fibonacci sequences, sorting algorithms, and more.
- 🌐 **Multi-Language Support**: Work in your preferred environment with built-in support for **Python**, **JavaScript**, **C++**, and **Java**.

## Tech Stack

- **Streamlit**: Powers the interactive web interface.
- **Monaco Editor**: Embedded VS Code style editor.
- **HTML/CSS/JS**: Custom styled UI layers wrapped efficiently in Streamlit iframes.

## Installation

1. **Clone the repository** (or download the source):
   ```bash
   git clone <repository-url>
   cd oxlo-ai-tutor
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   If needed, configure any specific environment variables in a `.env` file (e.g., API keys).

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open the provided `localhost` URL in your browser.
3. Click on **⚡ Open the Lab** to enter the coding environment.
4. Select your preferred programming language and initialize the environment.
5. Use the **AI Quick Actions**, write custom code, and run it directly in your browser.

## Project Structure

- `app.py`: The main entry point containing the Streamlit application logic and embedded UI.
- `ui/`: Automatically generated folder containing static HTML templates (`home.html`, `setup.html`, `lab.html`) for the different views.
- `requirements.txt`: Python package dependencies.
