# Chatbot
🎧 Personalized Music Curator Chatbot (RAG Architecture)

🚀 1. Project Overview and Motivation

The Personalized Music Curator Chatbot is designed to solve a simple, everyday problem: the difficulty of finding music that perfectly matches one's momentary mood, especially during routine activities like the morning commute or school preparation.

Our goal is to accurately identify subtle user emotions expressed through natural language input and instantly recommend the optimal music track. By skipping the tedious manual search process, the chatbot aims to deliver high-quality, personalized musical suggestions, ultimately making the user's day more efficient and enjoyable.

This service prioritizes a personalized user experience (UX), utilizing advanced AI to feel less like a tool and more like a sensitive, personal curator.

🏗️ 2. System Architecture: Retrieval-Augmented Generation (RAG)

The chatbot employs a robust Retrieval-Augmented Generation (RAG) architecture. This hybrid approach ensures recommendations are accurate (grounded in our verified dataset) while maintaining a high quality of conversational response (thanks to the LLM).

User Input
The user initiates the interaction with a query in natural language (e.g., "I feel energized and need something fast-paced.").

Retrieval
A high-performance search engine queries the local music database to find data entries that match the emotional or genre keywords from the input. / Local JSON/CSV Dataset (music_db.csv)

Augmentation
The retrieved music metadata (Title, Artist, Genre, etc.) is formatted into a clear context block. / Prompt Construction

Generation
The LLM synthesizes the context to generate a final, polished recommendation, adopting a professional curator persona. / LLM (Gemini Agent)

🛠️ 3. Implementation and Core Technologies

Core Technology: RAG Model

We leverage RAG to combine the generative power of the LLM with the precision of external data. This setup minimizes "hallucinations" and ensures that the recommendations are always sourced from our validated music catalog.

Data Source

Data Source: A local CSV file (music_db.csv) serves as the proprietary music database (our local DB).

Content: This dataset contains critical metadata (Artist, Title, Genre, Mood Tags, Release Year, etc.) used for the retrieval step.

LLM Role and Generation Prompt

Prompting: The retrieved music data is passed to the LLM as explicit context.

Expert Persona: The Gemini Agent is instructed to act as a "World-Class Music Curator". This persona is crucial for generating not just the song title, but also a rich, detailed explanation of why the song fits the user's mood, elevating the user experience.

🖥️ 4. Execution Views

This section details the two primary interfaces for interacting with the chatbot: the application's user interface and the backend console logs.

4.1. Running Interface (Application Screen)

This is the front-end view where users input their natural language queries and receive the stylized music recommendation cards.

Visual Elements: Input field, Submit button, and formatted display of the LLM's final, curated recommendation (including the expert rationale).

4.2. Terminal Execution Screen (Console Output)

When running the application locally, the terminal displays the backend processing steps, which are crucial for debugging and monitoring the RAG pipeline.

Expected Output:

System initialization messages.

Retrieval Log: Confirmation that the music_db.csv file was successfully queried.

Context Payload: The data snippet (e.g., [Title: 'Smooth Sailing', Artist: 'The Groovers', Genre: 'Lo-Fi Jazz']) sent to the LLM for augmentation.

API Calls: Status of the final call to the Gemini Agent.

⚙️ 5. Getting Started

To run the Music Curator Chatbot, ensure you have the required dependencies installed and your Gemini API key configured.

# 1. Clone the repository
git clone [YOUR_REPO_URL]
cd music-curator-chatbot

# 2. Install dependencies (e.g., Python environment)
pip install -r requirements.txt

# 3. Configure API Key
# Set your Gemini API key as an environment variable
export GEMINI_API_KEY="YOUR_API_KEY_HERE"

# 4. Run the application
python main_chatbot.py
