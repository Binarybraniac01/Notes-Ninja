import os
import google.generativeai as genai
import logging
from question_parser import identify_questions, structure_questions

logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is not set")
    raise ValueError("Gemini API key is not configured")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Successfully configured Gemini API")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    raise

def get_format_instructions(question_format):
    """
    Get specific instructions based on question format
    """
    format_instructions = {
        'short_answer': {
            'marks': 5,
            'instructions': """
                - Provide a concise response (2-3 paragraphs or 10 points)
                - Focus on key concepts and definitions
                - Include one relevant example
                - Use simple, clear language
                """
        },
        'essay': {
            'marks': 15,
            'instructions': """
                - Write a comprehensive response (4-5 paragraphs)
                - Include detailed explanations and analysis
                - Provide multiple examples and case studies
                - Present arguments with supporting evidence
                - Include a brief conclusion
                """
        },
        'problem_solving': {
            'marks': 10,
            'instructions': """
                - Break down the problem systematically
                - Show step-by-step solution process
                - Explain the reasoning at each step
                - Include relevant calculations or diagrams
                - Verify the solution
                """
        },
        'analysis': {
            'marks': 20,
            'instructions': """
                - Provide in-depth analysis (5-6 paragraphs)
                - Evaluate multiple perspectives
                - Include theoretical frameworks
                - Cite relevant examples and research
                - Draw well-reasoned conclusions
                - Consider implications and applications
                """
        },
        'definition': {
            'marks': 3,
            'instructions': """
                - Provide clear, precise definitions
                - Include key characteristics
                - Give a brief example
                - Keep response focused and concise
                """
        }
    }
    return format_instructions.get(question_format, format_instructions['short_answer'])

def generate_answers(subject, text, question_format='short_answer'):
    """
    Generate exam-style answers using Gemini AI
    """
    try:
        # Initialize the model with gemini-2.0-flash
        model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info(f"Initialized model for subject: {subject}")

        # Identify questions from the text
        questions = identify_questions(text)
        if not questions:
            logger.warning("No specific questions identified, treating entire text as context")
            questions = [text]

        format_info = get_format_instructions(question_format)

        # Structure the questions and format requirements
        prompt = structure_questions(subject, questions, format_info)

        # Generate content with safety settings
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 50000,
        }

        response = model.generate_content(
            prompt,
            safety_settings=safety_settings,
            generation_config=generation_config
        )

        if not response or not response.text:
            logger.error("Empty response from Gemini API")
            raise Exception("No content generated")

        return response.text

    except Exception as e:
        logger.error(f"Error generating answers: {str(e)}", exc_info=True)
        raise Exception(f"Failed to generate answers: {str(e)}")