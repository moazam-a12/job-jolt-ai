# AI-Powered Interview Question Generator

## Overview
The AI-Powered Interview Question Generator is a Python-based Jupyter Notebook application designed to streamline interview preparation for Data Science roles. Using the Gemini API (`gemini-2.0-flash`, free tier), it parses natural language inputs to deliver tailored technical and behavioral questions, along with interview tips. The modular chatbot ensures a smooth, engaging experience, handling intents like preparing for interviews, requesting more questions, and seeking tips.

## Features
- **Interactive Chatbot**: Processes inputs like "I need to prepare for an Upper Hand interview" to provide customized question sets and tips.
- **Question Generation**: Creates technical and behavioral questions based on job descriptions, with defaults for Data Science roles if needed.
- **Context-Aware Responses**: Tracks company/role context and prompts for clarification on vague inputs.
- **Modular Design**: Organized into cells for helper functions, data loading, and the chatbot loop for easy maintenance.
- **Robust Error Handling**: Uses keyword-based parsing to manage Gemini API quota limits, ensuring reliability.
- **Data Persistence**: Saves generated question sets to `output/updated_interview_questions.json`.

## Dataset
The project leverages datasets sourced from Kaggle:
- `job_descriptions.csv`: Contains Data Science job postings, enhanced with additional instances from various datasets for richer context.
- `updated_coding_interview_question_bank.csv`: Includes ~71 behavioral and technical questions tagged for Deep Learning, Data Science, and Machine Learning (ML), augmented with data from other sources.

## Setup and Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-powered-interview-question-generator.git
   cd ai-powered-interview-question-generator
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Required packages: `google-generativeai`, `pandas`, and others in `requirements.txt`.
3. **Set Up Gemini API Key**:
   - Get a free Gemini API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs).
   - Set the key as an environment variable:
     ```bash
     export GOOGLE_API_KEY='your-api-key'
     ```
     **Note**: The public free Gemini key used in development was removed for security. You must provide your own key.
4. **Directory Structure**:
   ```
   AI-Powered Interview Question Generator/
   ├── data/
   │   ├── updated_coding_interview_question_bank.csv
   │   ├── job_descriptions.csv
   ├── utils/
   │   ├── preprocess.py
   │   ├── preprocessed_data.json
   ├── output/
   │   ├── interview_questions.json
   │   ├── updated_interview_questions.json
   ├── requirements.txt
   └── main.ipynb
   ```
5. **Run the Notebook**:
   - Open `main.ipynb` in Jupyter Notebook.
   - Run Cells 1–5 to set up imports, preprocess data, and load question sets.
   - Run Cell 6 to start the chatbot.

## Usage
- Start the chatbot with Cell 6 in `main.ipynb`.
- Use inputs like:
  - "I need to prepare for an Upper Hand interview"
  - "More technical questions"
  - "Interview tips"
  - "Hi" (greeting response)
  - "exit" or "quit" to end
- The chatbot generates/retrieves Data Science questions, saves new sets to `output/updated_interview_questions.json`, and provides context-aware prompts.

## Implementation Details
- **Preprocessing**: `utils/preprocess.py` generates `utils/preprocessed_data.json` and `output/interview_questions.json` from enhanced Kaggle datasets.
- **Gemini Integration**: Employs `gemini-2.0-flash` for parsing inputs and generating questions/tips, with keyword fallbacks for API limits.
- **Modular Cells**:
  - **Cell 4**: Helper functions (`parse_user_input`, `generate_questions`, `get_interview_tips`).
  - **Cell 5**: Loads data and initializes context.
  - **Cell 6**: Runs the interactive chatbot with clean output.
- **Error Handling**: Manages API limits, empty job descriptions, and vague inputs with fallbacks and prompts.

## Limitations
- The free `gemini-2.0-flash` API has request/token limits, triggering fallbacks to keyword parsing or default questions.
- Users must supply their own Gemini API key.
- Relies on preprocessed data quality; ensure `preprocessed_data.json` and `interview_questions.json` are correctly generated.

## Author
Crafting ML projects in this economy, one dataset at a time! 😮‍💨

## Acknowledgments
- Datasets from [Kaggle](https://www.kaggle.com), enhanced with additional Data Science and ML-focused instances.
- Powered by the Gemini API (`gemini-2.0-flash`) for natural language processing.
- Built to help job seekers ace their Data Science interviews with confidence! ✨
