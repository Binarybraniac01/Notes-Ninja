# **🥷 Notes Ninja**

**Notes Ninja** is a smart study companion built with Flask and Google Gemini AI. It helps students and educators automatically generate structured exam notes, detailed answers, and study materials from raw text or images of question papers.

By leveraging the power of the **Gemini 2.0 Flash** model, Notes Ninja can understand questions from uploaded images (OCR) or text input and generate accurate, formatted answers in a downloadable Microsoft Word (.docx) document.

## **✨ Features**

* **📷 Visual Intelligence (OCR):** Upload images of handwritten or printed question papers. The app uses Gemini's vision capabilities to extract and understand the text automatically.  
* **✍️ Flexible Input:** Paste questions directly or mix and match with image uploads.  
* **🎯 Tailored Answer Formats:** Choose the depth of the answer based on marks or type:  
  * **Definition/Concept** (2-3 marks)  
  * **Short Answer** (5 marks)  
  * **Long Answer** (10 marks)  
  * **Essay** (15 marks)  
  * **Critical Analysis** (20 marks)  
  * **Math Problems** (Step-by-step solutions)  
* **📄 Automatic Formatting:** Generates a professional .docx file with bold headers, proper spacing, and bullet points ready for printing or sharing.  
* **⚡ Fast & Responsive:** Built with Bootstrap 5 for a clean dark-mode interface that works on mobile and desktop.

## **🛠️ Tech Stack**

* **Backend:** Python 3, Flask  
* **AI Engine:** Google Gemini 2.0 Flash (via google-generativeai)  
* **Document Processing:** python-docx  
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5  
* **Image Processing:** Pillow (PIL)

## **🚀 Getting Started**

### **Prerequisites**

* Python 3.8 or higher installed.  
* A Google Cloud Project with the **Gemini API** enabled.  
* An API Key from [Google AI Studio](https://aistudio.google.com/).  
  * *Need help? Check the guide in assets/how\_to\_get\_api\_key.pdf included in this repo.*

### **Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/binarybraniac01/notes-ninja.git\](https://github.com/binarybraniac01/notes-ninja.git)  
   cd notes-ninja

2. **Create and activate a virtual environment:**  
   \# Windows  
   python \-m venv venv  
   venv\\Scripts\\activate

   \# macOS/Linux  
   python3 \-m venv venv  
   source venv/bin/activate

3. **Install dependencies:**  
   pip install \-r requirements.txt

### **Configuration**

You must set up your environment variables for the application to work. You can set these in your terminal session or create a .env file.

**Required Variable:**

* GEMINI\_API\_KEY: Your Google Gemini API Key.

**Optional Variable:**

* SESSION\_SECRET: A secret key for Flask sessions (defaults to a built-in value if not set).

**Example (Linux/macOS):**

export GEMINI\_API\_KEY="AIzaSyYourKeyHere..."

**Example (Windows CMD):**

set GEMINI\_API\_KEY=AIzaSyYourKeyHere...

### **Running the App**

Run the application using Python:

python app.py

The application will start at http://localhost:5000.

## **📖 How to Use**

1. Open your browser and navigate to http://localhost:5000.  
2. **Subject:** Enter the subject name (e.g., "Physics", "European History").  
3. **Format:** Select the desired answer format (e.g., "Short Answer").  
4. **Input:**  
   * **Text:** Type or paste questions into the text area.  
   * **Images:** Click to upload images of your question paper.  
5. Click **Generate Answers**.  
6. Wait a moment for the AI to process. A .docx file containing your formatted study notes will download automatically\!

## **📂 Project Structure**

notes-ninja/  
├── app.py                  \# Main Flask application  
├── gemini\_helper.py        \# AI logic for generating answers  
├── ocr\_helper.py           \# AI logic for extracting text from images  
├── document\_generator.py   \# Word document creation logic  
├── question\_parser.py      \# Regex logic to identify distinct questions  
├── requirements.txt        \# Python dependencies  
├── static/                 \# CSS, JS, and images  
└── templates/              \# HTML templates

## **🤝 Contributing**

Contributions are welcome\! If you have suggestions for improvements or new features:

1. Fork the repo.  
2. Create a feature branch (git checkout \-b feature/NewFeature).  
3. Commit your changes.  
4. Push to the branch.  
5. Open a Pull Request.

## **📄 License**

This project is licensed under the MIT License.