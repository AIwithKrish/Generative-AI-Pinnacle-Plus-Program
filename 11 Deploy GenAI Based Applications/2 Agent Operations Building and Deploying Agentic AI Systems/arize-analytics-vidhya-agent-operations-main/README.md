# Agent Operations -- Course Setup Guide

Welcome, learners! This guide explains how to download the course notebooks, configure your local development environment, and run the application.

**GitHub repository:** https://github.com/Jgilhuly/arize-analytics-vidhya-agent-operations

## Step 1: Install Prerequisites

-   [Git](https://git-scm.com/downloads)
-   [VS Code](https://code.visualstudio.com/download) (or your preferred IDE)
-   [Python](https://www.python.org/downloads/) (check the repository for the required version)

## Step 2: Clone the Repository

Open Terminal, Command Prompt, or PowerShell. Navigate to your preferred working directory and run:

``` bash
git clone https://github.com/Jgilhuly/arize-analytics-vidhya-agent-operations.git
cd arize-analytics-vidhya-agent-operations
```

## Step 3: Open the Project in VS Code

From the cloned project directory, run:

``` bash
code .
```

Alternatively, open VS Code, select **File \> Open Folder**, and choose the cloned repository folder.

## Step 4: Set Up a Virtual Environment

Create a virtual environment:

``` bash
python -m venv venv
```

Activate it using the appropriate command for your operating system.

**macOS / Linux:**

``` bash
source venv/bin/activate
```

**Windows (Command Prompt):**

``` cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

``` powershell
.\venv\Scripts\Activate.ps1
```

On macOS or Linux, use `python3` instead of `python` if necessary.

## Step 5: Install Dependencies

If the repository contains a `requirements.txt` file, install the dependencies:

``` bash
python -m pip install -r requirements.txt
```

Otherwise, follow the dependency installation instructions provided in the repository.

## Step 6: Explore the Code

Open the course notebooks (`.ipynb`) in VS Code using the Python and Jupyter extensions. Select your virtual environment as the notebook kernel.

Explore the following example application files, if present:

-   `main.py` -- Application entry point.
-   `agent.py` -- Agent implementation.
-   `tools.py` -- Agent tools and supporting functions.

## Step 7: Run the Code

If the project contains a FastAPI application named `app` in `main.py`, run the following command from the appropriate directory:

``` bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser. FastAPI interactive API documentation is typically available at http://127.0.0.1:8000/docs.

Press `Ctrl+C` to stop the server.

Happy learning!
