# AutoXloo AI Sales Assistant - Frontend

Modern React + TypeScript frontend for the AI Sales Assistant.

## Features

- **Chat Interface**: Real-time chat with AI agents
- **Dashboard**: Analytics and inventory overview
- **Responsive Design**: Works on all devices
- **Modern UI**: Tailwind CSS with premium styling

## Tech Stack

- React 18
- TypeScript
- Vite 4 (compatible with Node 18)
- Tailwind CSS
- TanStack Query (React Query)
- Axios

## Quick Start

```bash
# Install dependencies (already done)
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

The frontend will run at `http://localhost:5173`

## Project Structure

```
src/
├── components/      # Reusable components (future)
├── pages/
│   ├── ChatInterface.tsx    # AI chat interface
│   └── Dashboard.tsx        # Analytics dashboard
├── hooks/           # Custom hooks (future)
├── utils/           # Utilities (future)
├── App.tsx          # Main app component
├── main.tsx         # Entry point
└── index.css        # Global styles
```

## API Integration

The frontend proxies `/api/*` requests to the backend at `http://localhost:8000`.

Make sure the FastAPI backend is running before starting the frontend.

## Usage

1. **Start Backend**:
   ```bash
   cd ../backend
   python3 main.py
   ```

2. **Start Frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**: Navigate to `http://localhost:5173`

## Features

### Chat Interface
- Send messages to AI agents
- View conversation history
- See AI reasoning and actions
- Quick action suggestions
- Real-time responses

### Dashboard
- Total vehicles and availability
- Price range statistics
- Category breakdown
- Recent listings table
- AI status indicator

## Environment

The frontend automatically proxies API requests to the backend via Vite's proxy configuration.
