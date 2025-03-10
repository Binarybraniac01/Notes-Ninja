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
        'definition': {
            'marks': 2,
            'instructions': """
                - Provide clear, precise definitions
                - Give a brief example
                - Keep response focused and concise
                """
        },
        'short_answer': {
            'marks': 5,
            'instructions': """
                - Structure answer suitble for 5 marks question maintaining better readability.
                - Use simple, clear language
                - Focus on key concepts and definitions
                - Include relevant example if necessary
                - Provide reference links for diagrams, do not draw them.
                """
        },
        'long_answer': {
            'marks': 10,
            'instructions': """
                - Give answer suitble for 10 marks question maintaining better readability
                - Use simple, clear language
                - Focus on key concepts and definitions
                - Include relevant examples if necessary
                - Provide reference links for diagrams, do not draw them.
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
                - If there are digrams in answer then simply give refrence link to it do not draw digram in answer
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
                - If there are digrams in answer then simply give refrence link to it do not draw digram in answer

                """
        },
        'Math_Problem': {
            'marks': None,
            'instructions': """
                - Solve the Mathematical problem given 
                - Keep explanation concise and include only necessary stuff
                - verify given solution, but do not include it in answer
                - Include relevant calculations
                - Provide reference links for diagrams if necessary, do not draw them. 
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

        
        #questions = identify_questions(text) 
        # if not questions:
        #     logger.warning("No specific questions identified, treating entire text as context")
        #     questions = [text]

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