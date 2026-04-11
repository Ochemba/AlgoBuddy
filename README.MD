# 🎓 AI Programming Tutor

An intelligent AI-powered tutoring system that helps students learn Python programming through personalized instruction, practice problems, and adaptive difficulty.

Built by: **Obianuju**  
Date: **March 2025**

---

## ✨ Features

### Core Features:
- 💬 **Interactive Chat** - Ask questions and get detailed, patient explanations
- 📝 **Practice Problems** - AI-generated coding problems with solutions
- 💡 **Progressive Hints** - 3-level hint system (gentle → specific → strong)
- ✅ **Answer Checking** - Intelligent validation with helpful feedback
- 📊 **Progress Tracking** - Monitor accuracy, topics covered, and streaks
- 🎯 **Adaptive Difficulty** - Problems automatically adjust to your skill level
- 🔥 **Study Streaks** - Daily consistency tracking
- 💰 **Flashcard Generation** - Generate flashcards based on course and topic chosen by user

### Teaching Methods:
- **Scaffolding** - Break complex topics into small steps
- **Socratic Method** - Learn through guided questions
- **Personalized Feedback** - Tailored to your learning style

---

## 🚀 Quick Start

### Prerequisites:
- Python 3.9 or higher
- OpenAI API key
- Internet connection
- supabase account

### Installation:

1. **Clone or download this project**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key:**

Create a `.env` file in the project folder:
```
OPENAI_API_KEY=your-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

4. **Run the tutor:**
```bash
streamlit run app.py
```

---

## 📖 How to Use

### Basic Chat:
```python
from tutor_engine import get_tutor_response

# Ask a question
response = get_tutor_response("What is a Python loop?")
print(response)
```

### Generate Practice Problem:
```python
from tutor_engine import generate_practice_problem

# Create a problem
problem = generate_practice_problem("loops", "easy")
print(problem["problem"])
print(problem["hints"])
```

### Complete Study Session:
```python
from tutor_engine import (
    start_study_session,
    generate_adaptive_problem,
    submit_answer_with_tracking,
    get_progress_report,
    end_study_session
)

# Start session
start_study_session()

# Practice
problem = generate_adaptive_problem("loops")
result = submit_answer_with_tracking(problem, "your answer", "loops")

# Check progress
print(get_progress_report())

# End session
end_study_session()
```

---

---

## 🎯 Supported Topics

- Variables
- Loops (for, while)
- Functions
- Lists
- Dictionaries
- Conditionals (if/else)
- Strings
- Classes
- Files
- Error Handling
- Modules

---

## 💰 Cost Information

This tutor uses OpenAI's GPT-3.5-turbo API:

- **Price:** $0.002 per 1,000 tokens
- **Typical question:** ~500-1000 tokens (~$0.001-0.002)
- **Practice problem:** ~800 tokens (~$0.0016)
- **Daily usage (20 questions):** ~$0.03-0.05
- **Monthly budget:** $5-10 for regular use

The system includes cost tracking to monitor usage!

---

## 🧪 Testing

Run the comprehensive test suite:
```bash
cd tests
python test_suite.py
```

This tests:
- ✅ Input validation
- ✅ Error handling
- ✅ API functionality
- ✅ Progress tracking
- ✅ Integration flows

---

## 🔧 Troubleshooting

### "Invalid API key" error:
- Check your `.env` file exists
- Verify the API key is correct
- Make sure `.env` is in the project root folder

### "Cannot connect" error:
- Check your internet connection
- Verify OpenAI services are up
- Check firewall settings

### "Rate limit" error:
- You're making too many requests
- Wait a minute and try again
- Consider adding longer delays

### Check logs:
All errors are logged in `logs/tutor_YYYYMMDD.log`

---

## 📚 Learning Resources

- **OpenAI Docs:** https://platform.openai.com/docs
- **Python Tutorial:** https://docs.python.org/3/tutorial/
- **Real Python:** https://realpython.com/

---

## 🎓 For Students

### Tips for Best Results:
1. **Ask specific questions** - "How do I use a for loop?" not just "loops"
2. **Try before asking for hints** - Challenge yourself!
3. **Practice daily** - Build your streak!
4. **Review weak topics** - Check your progress report
5. **Experiment** - Modify examples and see what happens

### Study Workflow:
1. Start with chat to understand concepts
2. Generate practice problems
3. Try to solve without hints
4. Use hints if stuck (3 levels available)
5. Check your answer
6. Review feedback and learn from mistakes

---

## 👩‍💻 For Developers

### Adding New Topics:
Edit `validators.py` and add to `valid_topics`:
```python
valid_topics = [
    "loops", "functions", "lists",
    "your_new_topic"  # Add here
]
```

### Customizing Teaching Style:
Edit `prompts.py` - change `PROGRAMMING_TUTOR_SYSTEM`:
```python
PROGRAMMING_TUTOR_SYSTEM = """
Your custom teaching instructions here...
"""
```

### Adding New Teaching Methods:
Add to `prompts.py` and update `get_tutor_response()` to use it.

---

## 🚧 Future Features (Coming Soon)

- 🌐 **Multiple Languages** - Support for more programming languages
- 🔉 **Voice chatting** - Support audio conversations
- 📚 **More Courses** - Support for more Courses and topics
- 🎭 **More Persona** - Support for more Personas for more fun explanation



---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🙏 Acknowledgments
I am still leraning and improving, i would love to come back to this in a couple of years as a reminder to myself not to give up!
- OpenAI for the GPT-3.5 API
- All the tutorial creators who made learning possible
- The Python community

---

## 📞 Contact

**Developer:** Obianuju Ochemba
**Project:** AI Programming Tutor  
**Year:** 2025

---

**Made with stress and tears**

**Happy Learning! 🚀**