import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def identify_questions(text: str) -> List[str]:
    """
    Extract questions from text using multiple techniques
    """
    questions = []
    
    # Split text into lines
    lines = text.split('\n')
    
    # Pattern for questions ending with question marks
    question_mark_pattern = r'[A-Z][^.!?]*\?'
    
    # Pattern for numbered questions
    numbered_pattern = r'^\s*(?:\d+[\).]|\([a-zA-Z]\)|\d+\s*[-.])\s*(.+)'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Find questions with question marks
        q_mark_matches = re.finditer(question_mark_pattern, line)
        for match in q_mark_matches:
            question = match.group().strip()
            if len(question) > 10:  # Avoid short fragments
                questions.append(question)
        
        # Find numbered questions
        numbered_match = re.match(numbered_pattern, line)
        if numbered_match:
            question_text = numbered_match.group(1).strip()
            if len(question_text) > 10:  # Avoid short fragments
                questions.append(question_text)
        
        # Look for common question starters
        starters = ['explain', 'describe', 'discuss', 'analyze', 'compare', 'what', 'how', 'why', 'give', 'write', 'differenciate']
        lower_line = line.lower()
        if any(lower_line.startswith(starter) for starter in starters):
            if len(line) > 10:  # Avoid short fragments
                questions.append(line)
    
    # Remove duplicates while preserving order
    seen = set()
    questions = [q for q in questions if not (q in seen or seen.add(q))]
    
    logger.info(f"Identified {len(questions)} questions from text")
    return questions

def structure_questions(subject: str, questions: List[str], format_info: Dict) -> str:
    """
    Structure questions for Gemini API prompt
    """
    structured_text = f"""
Subject: {subject}
Question Format: {format_info.get('marks', 5)} marks

Questions to analyze and answer:
"""
    
    for i, question in enumerate(questions, 1):
        structured_text += f"\nQuestion {i}:\n{question}\n"
    
    structured_text += f"\nPlease provide detailed answers following these requirements:\n{format_info.get('instructions', '')}"

    # structured_text += f"\nMake use of HTML to highlight elements and structure the document and other important things."
    
    return structured_text.strip()
