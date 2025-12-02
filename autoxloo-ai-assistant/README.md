# 🚗 AutoXloo AI Sales Assistant

> **A next-generation automotive sales platform powered by multi-agent AI, demonstrating real-time collaboration between specialized AI agents for vehicle discovery, lead qualification, and appointment scheduling.**

![Multi-Agent Workflow](https://img.shields.io/badge/Multi--Agent-CrewAI-blue)
![Vector Search](https://img.shields.io/badge/Vector%20Search-Pinecone-green)
![LLM](https://img.shields.io/badge/LLM-DeepSeek-orange)
![Framework](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-61dafb)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)

---

## ✨ Key Features

### 🤖 **Multi-Agent AI System**
- **Research Agent**: Semantic vehicle search with Pinecone RAG
- **Lead Qualifier**: Customer need analysis and CRM integration
- **Scheduling Agent**: Appointment booking with calendar tools

### 📊 **Real-Time Workflow Visualization**
- Visual flowchart showing agent collaboration
- Animated transitions between agents with arrow indicators
- Only displays when agents are actively working

### 🎯 **Smart Response Formatting**
- Concise, scannable responses (~150 words)
- Markdown tables with gradient headers and hover effects
- Bullet-point summaries for quick decision-making

### 🔍 **Semantic Search**
- 40-vehicle knowledge base with detailed specifications
- Vector embeddings via Sentence Transformers
- Pinecone for fast similarity search

### 🛠️ **Real Agent Tools**
- `check_calendar_availability()` - Find open time slots
- `create_crm_lead()` - Log customer information
- `book_test_drive()` - Schedule appointments
- `send_confirmation_email()` - Automated confirmations
- `get_vehicle_details()` - Inventory lookup

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  • Chat Interface  • Agent Workflow UI  • Dashboard     │
└────────────────────┬────────────────────────────────────┘
                     │ REST API
┌────────────────────▼────────────────────────────────────┐
│                   FastAPI Backend                        │
│  • Multi-Agent Orchestration  • Query Routing           │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼─────┐ ┌───▼──────────┐
│   CrewAI     │ │Pinecone│ │ DeepSeek LLM │
│ Multi-Agent  │ │ Vector │ │   API        │
│   System     │ │   DB   │ │              │
└──────────────┘ └────────┘ └──────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 18+**
- **API Keys**: DeepSeek API, Pinecone API

### 1. Clone & Setup

```bash
git clone <repository-url>
cd autoxloo-ai-assistant

# Copy environment template
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate data & index to Pinecone
python3 ../scripts/fetch_nhtsa_data.py
python3 ../scripts/generate_inventory.py
python3 ../scripts/build_knowledge_base.py
python3 ../scripts/setup_pinecone.py

# Start backend
python3 main.py
```

Backend runs at: `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 📖 Usage Examples

### Example 1: Vehicle Search
**User**: "Show me SUVs under $35k"

**Response**:
| Vehicle | Price | Safety | MPG |
|---------|-------|--------|-----|
| 2024 Subaru Forester | $18,368 | 5★ | 30 |

**Top Pick**: 2024 Subaru Forester
- Excellent safety rating
- Great fuel economy
- Under budget

**Workflow**: Research Agent → Complete ✓

---

### Example 2: Interest-Based Search
**User**: "I need a safe family SUV"

**Response**: Detailed comparison table with 3 vehicles

**Workflow**: Research Agent → Lead Qualifier → Complete ✓

---

### Example 3: Appointment Booking
**User**: "Schedule a test drive"

**Response**: "✓ Test drive request created. Confirmation: TD-ABC12345"

**Workflow**: Scheduling Agent → Complete ✓

---

## 💻 API Documentation

### Chat Endpoint

```http
POST /api/chat
Content-Type: application/json

{
  "message": "Show me Honda under $45k",
  "conversation_id": "optional-uuid"
}
```

**Response:**
```json
{
  "response": "I recommend the 2024 Honda Pilot...",
  "conversation_id": "uuid",
  "agents_used": ["research", "qualifier"],
  "actions_taken": [...]
}
```

### Other Endpoints

- `GET /api/inventory` - List all vehicles
- `GET /api/inventory/:stock_number` - Get vehicle details
- `GET /api/stats` - Inventory statistics

---

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **CrewAI** - Multi-agent orchestration
- **LangChain** - LLM tooling and agents
- **Pinecone** - Vector database
- **Sentence Transformers** - Local embeddings
- **DeepSeek API** - Large language model

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **React Query** - State management
- **ReactMarkdown** - Response rendering
- **Lucide React** - Icons

### Data
- **NHTSA API** - Real vehicle data (40 models)
- **50 Dealership Listings** - Augmented inventory
- **40 Detailed Specs** - Knowledge base

---

## 📁 Project Structure

```
autoxloo-ai-assistant/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── agents/
│   │   ├── crew.py            # Multi-agent system
│   │   └── tools.py           # Agent tools
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ChatInterface.tsx
│   │   │   └── Dashboard.tsx
│   │   ├── components/
│   │   │   └── AgentWorkflow.tsx
│   │   └── index.css
│   └── package.json
├── data/
│   ├── nhtsa_vehicles.json     # Real vehicle data
│   ├── dealership_inventory.json
│   ├── vehicle_knowledge_base.json
│   └── knowledge_corpus.txt
├── scripts/
│   ├── fetch_nhtsa_data.py
│   ├── generate_inventory.py
│   ├── build_knowledge_base.py
│   └── setup_pinecone.py
├── .env.example
├── .gitignore
└── README.md
```

---

## 🎯 Demo Scenarios

### CEO Demo Flow

1. **Welcome Message** → Chat opens with greeting
2. **Vehicle Discovery**: "Show me safe SUVs under $40k"
   - Watch Research Agent activate
   - See table with 3 options
3. **Express Interest**: "I'm interested in the Honda CR-V"
   - See Research → Qualifier workflow
   - Get personalized recommendation
4. **Book Appointment**: "Schedule a test drive"
   - See Scheduling Agent light up
   - Receive confirmation number

---

## 🔧 Configuration

### Environment Variables

```bash
# LLM Configuration
DEEPSEEK_API_KEY=your_deepseek_key
OPENAI_API_KEY=fallback_if_needed
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com

# Vector Database
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=autoxloo-vehicles
```

---

## 🤝 Contributing

This is a demo project for interview/showcase purposes. For production use:
1. Add authentication
2. Implement real CRM integration
3. Add database for persistence
4. Deploy with proper scaling
5. Add comprehensive testing

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **CrewAI** for multi-agent orchestration
- **Pinecone** for vector search
- **DeepSeek** for LLM API
- **NHTSA** for vehicle data

---

## 📞 Contact

Built by **[Your Name]** for **Webxloo CEO Interview**

- Portfolio: [your-portfolio.com]
- LinkedIn: [your-linkedin]
- Email: [your-email]

---

**⭐ If you found this project interesting, please star the repo!**
