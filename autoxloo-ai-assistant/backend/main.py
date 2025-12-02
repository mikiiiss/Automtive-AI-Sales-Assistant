"""
FastAPI Backend for AutoXloo AI Sales Assistant
Main entry point for the API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from dotenv import load_dotenv

from agents.crew import AutoXlooCrew

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AutoXloo AI Sales Assistant",
    description="Multi-agent AI system for automotive dealership sales",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load inventory data
INVENTORY_PATH = "../data/dealership_inventory.json"
inventory_data = []

try:
    with open(INVENTORY_PATH, 'r') as f:
        inventory_data = json.load(f)
    print(f"✓ Loaded {len(inventory_data)} vehicles from inventory")
except FileNotFoundError:
    print(f"⚠ Warning: Inventory file not found at {INVENTORY_PATH}")
    print("  Run: python scripts/generate_inventory.py")


# Pydantic models
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    actions_taken: List[dict] = []
    agents_used: List[str] = []  # NEW: Track which agents were used
    metadata: dict = {}



# Initialize AutoXloo Crew
crew = AutoXlooCrew(inventory_data)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AutoXloo AI Sales Assistant",
        "inventory_count": len(inventory_data)
    }


@app.get("/api/inventory")
async def get_inventory(limit: int = 20):
    """Get dealership inventory"""
    return {
        "total": len(inventory_data),
        "vehicles": inventory_data[:limit]
    }


@app.get("/api/inventory/{stock_number}")
async def get_vehicle(stock_number: str):
    """Get specific vehicle by stock number"""
    vehicle = next((v for v in inventory_data if v['stock_number'] == stock_number), None)
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return vehicle


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Main chat endpoint - processes customer queries using CrewAI agents
    """
    try:
        # Process message through CrewAI
        result = await crew.process_customer_query(
            message.message,
            conversation_id=message.conversation_id
        )
        
        return ChatResponse(
            response=result['response'],
            conversation_id=result['conversation_id'],
            actions_taken=result.get('actions_taken', []),
            agents_used=result.get('agents_used', []),  # NEW: Pass agents to frontend
            metadata=result.get('metadata', {})
        )
    
    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get dealership and system statistics"""
    return {
        "inventory": {
            "total_vehicles": len(inventory_data),
            "available": sum(1 for v in inventory_data if v.get('available', True)),
            "featured": sum(1 for v in inventory_data if v.get('featured', False)),
        },
        "price_range": {
            "min": min(v['price'] for v in inventory_data) if inventory_data else 0,
            "max": max(v['price'] for v in inventory_data) if inventory_data else 0,
            "avg": sum(v['price'] for v in inventory_data) // len(inventory_data) if inventory_data else 0,
        },
        "categories": _get_category_breakdown(),
    }


def _get_category_breakdown():
    """Helper to get vehicle category breakdown"""
    categories = {}
    for vehicle in inventory_data:
        cat = vehicle.get('category', 'other')
        categories[cat] = categories.get(cat, 0) + 1
    return categories


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
