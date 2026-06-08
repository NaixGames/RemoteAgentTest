## Testing some AI agent loops

# Motivation 
I wanted to understand how "agent AI works". This is a repo that does a basic agentic loop in python, by using calls to the gemeni API. Nothing fancy, but it works and I learnt a lot, so I got what I wanted out of this.

# Quick Start

Using the uv package manager (or whatever one you like) run

uv add google-genai==1.12.1
uv add python-dotenv==1.1.0

Then for use run

uv run main.py "your query here"

# Usage

The agent has access to only the "calculator" subdirectory. Instaed it can contents in folders, files and write to them. You can ask what some files do and stuff like that, and it will run the query on its own.

# Contributing

Please no. Just do your own, I promise it is easier than it sounds.
