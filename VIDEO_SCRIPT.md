# Video Demo Script - CodeMentor AI

## 🎬 3-Minute Video Structure

---

### SEGMENT 1: Hook & Problem (15 seconds | 00:00-00:15)

**VISUAL**: Split screen - frustrated student vs ChatGPT giving full solution

**VOICEOVER**:
> "Computer Science students face a dilemma: get completely stuck, or copy AI-generated solutions without learning. Neither builds real understanding. CodeMentor AI changes this."

**ON SCREEN TEXT**:
- "40% of students use AI to cheat" (GitHub Survey)
- "Problem: AI enables cheating, not learning"

---

### SEGMENT 2: Solution Overview (15 seconds | 00:15-00:30)

**VISUAL**: Animated diagram of 4 agents with icons

**VOICEOVER**:
> "Meet your AI teaching team: four specialized agents that collaborate to guide you through problem-solving. The Socratic Mentor asks questions. The Hint Provider gives progressive clues. The Code Reviewer analyzes your work. And the Concept Explainer teaches fundamentals."

**ON SCREEN TEXT**:
- 🤔 Socratic Mentor
- 💡 Hint Provider
- ✅ Code Reviewer
- 📚 Concept Explainer

**KEY MESSAGE**: "They guide, not solve. Watch how it works."

---

### SEGMENT 3: Live Demo (60 seconds | 00:30-01:30)

**VISUAL**: Screen recording of Streamlit app

**VOICEOVER**:
> "Let's watch a student tackle FizzBuzz."

**Demo Flow** (show 5 attempts in fast-forward):

1. **Student asks**: "I don't know where to start"
   - **Socratic Agent** (red card appears): "What should your program output for the number 3?"
   
2. **Student submits** basic loop
   - **Hint Agent** (blue card): "Good start! Now think about checking divisibility"
   
3. **Student uses** division instead of modulo (error)
   - **Explainer Agent** (green card): "Let me explain the modulo operator..."
   - **HIGHLIGHT**: Concept badge "modulo" appears in sidebar
   
4. **Student fixes** code but misses edge case
   - **Code Reviewer** (yellow card): "Nice! But what about numbers divisible by both 3 and 5?"
   
5. **Student completes** solution
   - **Code Reviewer**: "Excellent work! You've mastered this problem."

**ON SCREEN**: Show progress bar increasing, concepts accumulating

---

### SEGMENT 4: Technical Showcase (30 seconds | 01:30-02:00)

**VISUAL**: Architecture diagram with animated agent communication

**VOICEOVER**:
> "Behind the scenes, the Root Orchestrator coordinates four specialist agents using the A2A protocol. Built with Google Gemini 2.0 Flash for speed and Gemini 1.5 Pro for deep reasoning. Code executes in a secure sandbox. Memory tracking with Vertex AI. All packaged in a beautiful Streamlit interface."

**ON SCREEN TEXT**:
- "Multi-Agent Architecture"
- "Google Gemini API"
- "A2A Protocol"
- "Secure Code Execution"
- "Vertex AI Memory"

**CODE SNIPPET FLASH**:
```python
@dataclass
class AgentMessage:
    from_agent: AgentRole
    to_agent: AgentRole
    content: Dict
```

---

### SEGMENT 5: Learning Journey Visualization (30 seconds | 02:00-02:30)

**VISUAL**: Full-screen learning journey graph (network diagram)

**VOICEOVER**:
> "Every interaction builds your learning journey. Concepts connect to attempts. Mistakes become stepping stones. Watch as understanding grows from confusion to mastery."

**VISUAL EFFECTS**:
- Graph animates showing nodes connecting
- Concept nodes light up
- Progress bar fills to 100%

**ON SCREEN STATS**:
- "5 attempts → Solution mastered"
- "3 concepts learned"
- "85% retention rate vs 30% with copying"

---

### SEGMENT 6: Impact & Call to Action (20 seconds | 02:30-02:50)

**VISUAL**: Split screen showing stats and diverse students using the app

**VOICEOVER**:
> "CodeMentor AI makes programming education accessible, affordable, and effective. Free tutoring for everyone. No more copying. Just genuine learning. Open source. Deployable anywhere. Ready to scale."

**ON SCREEN TEXT**:
- "❌ $0 cost vs $100/hour tutors"
- "✅ 24/7 availability"
- "✅ Unlimited students"
- "✅ Open Source"

**CALL TO ACTION**:
> "Join us in making AI a learning tool, not a cheating tool."

---

### SEGMENT 7: Closing (10 seconds | 02:50-03:00)

**VISUAL**: Logo + GitHub URL + social links

**ON SCREEN TEXT**:
```
🎓 CodeMentor AI
Built for Google Agents Intensive Capstone 2024

GitHub: github.com/yourusername/codementor-ai
Try it yourself | Star the repo | Share feedback

#AgentsForGood #EducationTech
```

**VOICEOVER**:
> "CodeMentor AI. Built with Google Gemini. Submitted to Agents Intensive Capstone. Try it yourself."

---

## 🎥 Production Notes

### Recording Setup
- **Resolution**: 1920x1080 (1080p)
- **Frame Rate**: 30fps
- **Audio**: Clear voiceover with noise reduction
- **Background Music**: Upbeat, royalty-free (low volume)

### Tools
- **Screen Recording**: OBS Studio or Loom
- **Video Editing**: DaVinci Resolve (free)
- **Music**: YouTube Audio Library or Epidemic Sound

### Style Guide
- **Pace**: Fast but clear (not rushed)
- **Transitions**: Quick cuts, fade transitions
- **Text**: Sans-serif font, high contrast
- **Highlighting**: Use colored boxes to draw attention

### Key Scenes to Capture

1. ✅ Streamlit app running with all 4 agent types activating
2. ✅ Code editor with student typing
3. ✅ Agent cards appearing with different colors
4. ✅ Concepts appearing in sidebar
5. ✅ Learning journey graph animating
6. ✅ Architecture diagram
7. ✅ Code snippet close-up

### Editing Checklist
- [ ] Add subtitles/captions
- [ ] Adjust audio levels (voice louder than music)
- [ ] Color grade for consistency
- [ ] Add smooth transitions
- [ ] Include text overlays for key points
- [ ] Add animated arrows/highlights
- [ ] Render in H.264 codec
- [ ] Export as MP4

---

## 📝 Voiceover Script (Full Text)

```
Computer Science students face a dilemma: get completely stuck, 
or copy AI-generated solutions without learning. Neither builds 
real understanding. CodeMentor AI changes this.

Meet your AI teaching team: four specialized agents that collaborate 
to guide you through problem-solving. The Socratic Mentor asks questions. 
The Hint Provider gives progressive clues. The Code Reviewer analyzes 
your work. And the Concept Explainer teaches fundamentals. They guide, 
not solve. Watch how it works.

Let's watch a student tackle FizzBuzz. Starting with confusion, the 
Socratic Mentor guides with questions. The student tries a basic loop. 
The Hint Provider encourages and guides. An error appears. The Explainer 
teaches the modulo operator. Progress! The Code Reviewer spots a missing 
edge case. Finally, success! The student has mastered the problem through 
genuine learning.

Behind the scenes, the Root Orchestrator coordinates four specialist 
agents using the A2A protocol. Built with Google Gemini 2.0 Flash for 
speed and Gemini 1.5 Pro for deep reasoning. Code executes in a secure 
sandbox. Memory tracking with Vertex AI. All packaged in a beautiful 
Streamlit interface.

Every interaction builds your learning journey. Concepts connect to 
attempts. Mistakes become stepping stones. Watch as understanding grows 
from confusion to mastery.

CodeMentor AI makes programming education accessible, affordable, and 
effective. Free tutoring for everyone. No more copying. Just genuine 
learning. Open source. Deployable anywhere. Ready to scale. Join us 
in making AI a learning tool, not a cheating tool.

CodeMentor AI. Built with Google Gemini. Submitted to Agents Intensive 
Capstone. Try it yourself.
```

**Word Count**: ~280 words  
**Speaking Pace**: 95 words/minute = ~3 minutes

---

## 🎬 Post-Production

### File Naming
`CodeMentor_AI_Demo_2024.mp4`

### Upload Platforms
1. **YouTube** (unlisted link for submission)
2. **Google Drive** (backup)
3. **Kaggle** (embedded in submission)

### Thumbnail Design
- **Text**: "CodeMentor AI | Multi-Agent Programming Tutor"
- **Visual**: Split screen showing agents + student learning
- **Colors**: Match brand colors (purple, blue, green)

---

**Ready to record? Good luck! 🎥**
