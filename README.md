---
title: Career_chatbot
app_file: app.py
sdk: gradio
sdk_version: 6.14.0
---

# Career Conversation Chatbot

An AI-powered chatbot that answers questions about my professional background, skills, and experience using generative AI.

## 🚀 Live Demo

Try the chatbot here: [https://huggingface.co/spaces/Deb2026hf02032000/Career_chatbot](https://huggingface.co/spaces/Deb2026hf02032000/Career_chatbot)

## 📋 About

This chatbot acts as my personal AI assistant, providing information about my career, technical skills, projects, and experience. It's trained on my LinkedIn profile and professional summary to give accurate and engaging responses to career-related questions.

## ✨ Features

- **Intelligent Q&A**: Answers questions about professional background, skills, and experience
- **Contact Recording**: Captures user contact details and inquiries for follow-up
- **Unknown Question Tracking**: Records questions the bot can't answer for continuous improvement
- **Push Notifications**: Sends real-time alerts via Pushover when users express interest or ask unknown questions
- **Natural Conversations**: Built with Gradio for a smooth, intuitive chat experience

## 🛠️ Tech Stack

- **Frontend**: Gradio ChatInterface
- **LLM**: Llama 3.1 8B (via Groq API)
- **PDF Parsing**: pypdf
- **Notifications**: Pushover API
- **Deployment**: HuggingFace Spaces

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/career-chatbot.git
cd career-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
GROQ_API_KEY=your_groq_api_key
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user
```

4. Add your files to the `me/` directory:
- `linkedin.pdf` - Your LinkedIn profile export
- `summary.txt` - Your professional summary

5. Run the app:
```bash
python app.py
```

## 🎯 Use Cases

- Personal portfolio website chatbot
- Career information assistant
- Lead generation for job opportunities
- Automated FAQ handling for recruiters and hiring managers

## 📝 How It Works

1. The chatbot reads your LinkedIn profile (PDF) and professional summary
2. Uses a system prompt to instruct the LLM to act as you
3. Answers career-related questions based on your data
4. Triggers special actions (like recording contact info) via JSON-based tool calling
5. Sends push notifications for important interactions

## 👤 Author

**Debajyoti**
- Software Engineer (GenAI Engineer)
- 2+ years of experience in AI-driven platforms and scalable backend systems

## 📄 License

This project is open source and available for educational purposes.
