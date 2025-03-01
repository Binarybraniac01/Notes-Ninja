from docx import Document
from docx.shared import Pt
import tempfile
import os
import logging
from question_parser import identify_questions

logger = logging.getLogger(__name__)

def create_document(subject, questions_text, answers):
    """
    Create a formatted Word document with questions and answers
    """
    try:
        doc = Document()

        # Add title
        title = doc.add_heading(f'{subject} - Exam Answers', 0)
        title.alignment = 1  # Center alignment

        # Identify questions
        questions = identify_questions(questions_text)

        # Split answers if multiple questions
        answer_sections = answers.split('\nQuestion') if '\nQuestion' in answers else [answers]

        # Add content sections
        if questions and len(questions) > 1:
            # Multiple questions format
            for i, (question, answer) in enumerate(zip(questions, answer_sections), 1):
                # Add question section
                doc.add_heading(f'Question {i}:', level=1)
                doc.add_paragraph(question)

                # Add answer section
                doc.add_heading(f'Answer {i}:', level=2)
                # Clean up the answer text
                answer_text = answer.replace(f'{i}:', '').strip()
                doc.add_paragraph(answer_text)

                # Add separator except for last question
                if i < len(questions):
                    doc.add_paragraph('---')
        else:
            # Single question/context format
            doc.add_heading('Question Context:', level=1)
            doc.add_paragraph(questions_text)

            doc.add_heading('Answer:', level=1)
            doc.add_paragraph(answers)

        # Save document
        temp_path = os.path.join(tempfile.gettempdir(), 'exam_answers.docx')
        doc.save(temp_path)

        return temp_path
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}")
        raise Exception("Failed to create document")