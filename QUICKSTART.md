# 🚀 Quick Start Guide - CodeMentor AI

## Step-by-Step Setup (5 minutes)

### 1. Prerequisites Check
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Git installed
- [ ] Google Gemini API key ([Get one free here](https://aistudio.google.com/app/apikey))

### 2. Installation

```bash
# Navigate to project folder
cd "e:\Code\Capstone Project"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

Create a file named `.env` in the project root:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

**Important:** Replace `your_actual_api_key_here` with your real Gemini API key!

### 4. Test the Installation

Run the demo script to verify everything works:

```bash
python demo/demo_script.py
```

You should see the multi-agent demo running with FizzBuzz!

### 5. Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎮 Using CodeMentor AI

### For Students

1. **Read the Problem**: The current problem is displayed at the top
2. **Write Code**: Use the code editor on the right to write your solution
3. **Get Help**: 
   - Click "📨 Send Message" to ask questions
   - Click "📤 Submit for Review" to get code feedback
   - Click "▶️ Run Code" to test your solution
4. **Track Progress**: Check the sidebar to see concepts learned and attempts

### For Demo/Presentation

Use the pre-scripted demo:

```bash
python demo/demo_script.py
```

This runs through 5 steps showing all 4 agents in action!

---

## 🧪 Running Tests

```bash
# Test code executor (should pass all tests)
pytest tests/test_agents.py -v
```

---

## 🎯 Quick Tips

### If you see import errors:
Make sure your virtual environment is activated:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### If Gemini API doesn't work:
1. Check your API key is correct in `.env`
2. Verify you have credits/quota on your Google Cloud account
3. Test the API key at https://aistudio.google.com

### If Streamlit doesn't start:
```bash
pip install --upgrade streamlit
streamlit run app.py --server.port 8502  # Try different port
```

---

## 📚 Next Steps

1. ✅ **Test with Different Problems**: Edit `st.session_state.current_problem` in `app.py`
2. ✅ **Customize Agents**: Modify system instructions in each agent file
3. ✅ **Add More Concepts**: Extend `concept_database` in `explainer_agent.py`
4. ✅ **Deploy to Cloud**: Follow Cloud Run deployment guide (coming soon)

---

## 🎥 Recording Your Demo Video

### Recommended Tools
- **Screen Recording**: OBS Studio (free) or Loom
- **Video Editing**: DaVinci Resolve (free) or iMovie
- **Duration**: 3 minutes max

### Script Outline (3 min)
1. **00:00-00:15** - Problem intro & hook
2. **00:15-01:30** - Live demo (run Streamlit app)
3. **01:30-02:00** - Show agent collaboration
4. **02:00-02:45** - Architecture & tech stack
5. **02:45-03:00** - Impact & call to action

### Recording Tips
1. Close unnecessary apps/windows
2. Use 1080p resolution
3. Enable subtitles if possible
4. Practice 2-3 times before final recording
5. Add upbeat background music (royalty-free)

---

## 📦 Submission Checklist

For hackathon submission:

- [ ] README.md complete with all sections
- [ ] Code is well-commented
- [ ] All tests passing
- [ ] Demo script works end-to-end
- [ ] Video recorded (3 min max)
- [ ] GitHub repository is public
- [ ] .env file NOT committed (in .gitignore)
- [ ] requirements.txt has all dependencies
- [ ] Screenshots/demo images added

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: "Import could not be resolved"
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: "API key not found"
**Solution**: Create `.env` file with `GOOGLE_API_KEY=your_key`

**Issue**: "Port already in use"
**Solution**: Use different port: `streamlit run app.py --server.port 8502`

**Issue**: Agent responses are slow
**Solution**: Normal! Gemini API can take 2-5 seconds per response

**Issue**: Code execution timeout
**Solution**: This is intentional security feature (5 sec limit)

---

## 💬 Need Help?

- **Documentation**: See README.md
- **Code Examples**: Check `demo/demo_script.py`
- **Tests**: Look at `tests/test_agents.py`

---

**Good luck with your hackathon! 🚀**
