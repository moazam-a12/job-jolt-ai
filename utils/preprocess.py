import pandas as pd
import re
import json
from pathlib import Path
from collections import defaultdict

def load_question_bank(question_bank_path, category_column='category'):
    """Load and clean the question bank CSV, categorizing by unique values in category_column."""
    try:
        df = pd.read_csv(question_bank_path)
        # Handle missing values
        df = df.dropna(subset=['id', 'question', 'difficulty', category_column])
        
        # Count total and unique questions
        total_questions = len(df)
        unique_questions = len(df['question'].drop_duplicates())
        print(f"Total questions in dataset: {total_questions}")
        print(f"Unique questions in dataset: {unique_questions}")
        
        # Remove duplicates based on question column
        df = df.drop_duplicates(subset=['question'])
        
        # Get unique categories
        unique_categories = df[category_column].str.lower().unique().tolist()
        print("Unique categories in question bank:", unique_categories)
        
        # Initialize questions dictionary
        questions = {'technical': {}, 'behavioral': []}
        # Define technical and behavioral category keywords
        technical_keywords = ['machine learning', 'data science', 'deep learning']
        behavioral_keywords = ['behavior', 'behavioral']
        
        # Categorize questions
        for cat in unique_categories:
            cat_lower = cat.lower()
            # Check if category is technical
            if any(keyword in cat_lower for keyword in technical_keywords):
                questions['technical'][cat_lower] = df[df[category_column].str.lower() == cat_lower][['id', 'question', 'difficulty']].to_dict('records')
            # Check if category is behavioral
            elif any(keyword in cat_lower for keyword in behavioral_keywords):
                questions['behavioral'].extend(df[df[category_column].str.lower() == cat_lower][['id', 'question', 'difficulty']].to_dict('records'))
        
        # Fallback for behavioral questions based on question text
        behavioral_text_keywords = [
            'tell me about yourself', 'why should we hire you', 'strengths', 'weaknesses', 'teamwork',
            'experience', 'challenge', 'leadership', 'conflict', 'accomplishment', 'failure', 'motivation',
            'career goals', 'work with others', 'problem solving'
        ]
        behavioral_fallback = df[df['question'].str.lower().str.contains('|'.join(behavioral_text_keywords), na=False)][['id', 'question', 'difficulty']].to_dict('records')
        # Add fallback questions to behavioral, avoiding duplicates
        existing_behavioral_questions = {q['question'].lower() for q in questions['behavioral']}
        questions['behavioral'].extend([q for q in behavioral_fallback if q['question'].lower() not in existing_behavioral_questions])
        
        # Print counts for each category
        for subcat in questions['technical']:
            print(f"{subcat.title()} questions: {len(questions['technical'][subcat])}")
        print(f"Behavioral questions: {len(questions['behavioral'])}")
        
        return questions
    except Exception as e:
        print(f"Error loading question bank: {e}")
        return None

def extract_keywords(text):
    """Extract relevant keywords from job description text."""
    if not isinstance(text, str):
        return []
    words = re.findall(r'\b\w+\b', text.lower())
    relevant_keywords = [
        'machine learning', 'data science', 'python', 'pytorch', 'tensorflow', 'sql', 'pandas', 'spark',
        'cloud', 'aws', 'gcp', 'azure', 'databricks', 'communication', 'collaboration', 'sports technology',
        'generative ai', 'deep learning', 'data pipelines', 'feature engineering', 'model deployment',
        'kubernetes', 'docker', 'r', 'statistics', 'natural language processing', 'computer vision'
    ]
    keywords = []
    for keyword in relevant_keywords:
        if keyword in text.lower():
            keywords.append(keyword)
    single_word_keywords = ['python', 'sql', 'pandas', 'spark', 'aws', 'gcp', 'azure', 'databricks', 'pytorch', 'tensorflow', 'r', 'kubernetes', 'docker']
    keywords.extend([word for word in words if word in single_word_keywords and word not in keywords])
    return list(set(keywords))

def load_job_descriptions(job_descriptions_path):
    """Load and process job descriptions CSV."""
    try:
        df = pd.read_csv(job_descriptions_path)
        df = df.fillna({'job_description_text': '', 'company_description': ''})
        df['combined_text'] = df['job_description_text'] + ' ' + df['company_description']
        df['keywords'] = df['combined_text'].apply(extract_keywords)
        jobs = df[['job_title', 'company_name', 'seniority_level', 'keywords']].to_dict('records')
        return jobs
    except Exception as e:
        print(f"Error loading job descriptions: {e}")
        return None

def save_preprocessed_data(questions, jobs, output_path):
    """Save preprocessed data as JSON."""
    output_data = {
        'questions': questions,
        'jobs': jobs
    }
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Preprocessed data saved to {output_path}")

def main(question_bank_path, job_descriptions_path, output_path, category_column='category'):
    """Main preprocessing function."""
    questions = load_question_bank(question_bank_path, category_column)
    jobs = load_job_descriptions(job_descriptions_path)
    
    if questions is None or jobs is None:
        print("Failed to load data. Exiting.")
        return
    
    save_preprocessed_data(questions, jobs, output_path)