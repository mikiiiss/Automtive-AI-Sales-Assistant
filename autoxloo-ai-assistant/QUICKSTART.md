# AutoXloo AI Sales Assistant - Quick Start Guide

## 🚀 Setup (5 minutes)

### 1. Configure API Key

Create `.env` file from template:
```bash
cd /home/miki/Summer_projects/Webxloo/autoxloo-ai-assistant
cp .env.example .env
```

Edit `.env` and add your **DeepSeek API key**:
```bash
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com
```

### 2. Install Backend Dependencies

```bash
cd backend
pip3 install -r requirements.txt --user
```

### 3. Start Backend

```bash
cd backend
python3 main.py
```

Backend will run at: `http://localhost:8000`

### 4. Start Frontend (another terminal)

```bash
cd frontend
npm run dev
```

Frontend will run at: `http://localhost:5173`

## 🎯 Test It

Open `http://localhost:5173` and try:
- "Show me SUVs under $35k"
- "Does the CR-V have blind spot monitoring?"
- "Schedule a test drive for the Honda Civic"

## 📊 What You Have

- **Backend**: FastAPI + CrewAI multi-agent system
- **Frontend**: React chat interface + dashboard
- **Data**: 50 real vehicles from NHTSA + detailed specs
- **AI**: 3 specialized agents (Research, Scheduling, Qualifier)

## 🔑 Getting DeepSeek API Key

1. Go to https://platform.deepseek.com/
2. Sign up / Log in
3. Navigate to API Keys
4. Create new key
5. Copy to `.env` file

**Why DeepSeek?**
- Faster than GPT-4
- Much cheaper (~90% cost savings)
- OpenAI-compatible API

---

**Ready to impress the CEO!** 🎉
