"""
Agent Tools - Real capabilities for CrewAI agents
"""
from langchain.tools import tool
from datetime import datetime, timedelta
import json
import os
from typing import Dict, Optional
import random


class AgentTools:
    """Collection of tools for AI agents"""
    
    LEADS_FILE = "../data/crm_leads.json"
    APPOINTMENTS_FILE = "../data/appointments.json"
    
    @staticmethod
    def _load_json(filepath: str):
        """Load JSON file or return empty list"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return []
    
    @staticmethod
    def _save_json(filepath: str, data):
        """Save data to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


@tool
def check_calendar_availability(preferred_date: str = "", preferred_time: str = "") -> str:
    """
    Check calendar availability for test drive appointments.
    Args:
        preferred_date: Date in format 'YYYY-MM-DD' or day name (Monday, Tuesday, etc)
        preferred_time: Time preference (morning, afternoon, specific time like '2pm')
    Returns:
        Available time slots
    """
    # Mock calendar check - returns realistic availability
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    times = ["9:00 AM", "10:30 AM", "1:00 PM", "3:00 PM", "5:00 PM"]
    
    # Generate some "available" slots
    available_slots = []
    for day in random.sample(days, 3):
        time = random.choice(times)
        available_slots.append(f"{day} at {time}")
    
    result = f"✓ Calendar checked. Available slots:\n"
    for i, slot in enumerate(available_slots, 1):
        result += f"{i}. {slot}\n"
    
    return result


@tool
def create_crm_lead(customer_name: str, interest: str, budget: str = "Not specified", 
                    timeline: str = "Not specified", contact_info: str = "") -> str:
    """
    Create a new lead in the CRM system.
    Args:
        customer_name: Customer's name
        interest: What they're interested in (vehicle type, specific model)
        budget: Budget range
        timeline: Purchase timeline
        contact_info: Email or phone
    Returns:
        Confirmation with lead ID
    """
    leads = AgentTools._load_json(AgentTools.LEADS_FILE)
    
    lead = {
        "lead_id": f"LEAD-{len(leads) + 1001}",
        "customer_name": customer_name,
        "interest": interest,
        "budget": budget,
        "timeline": timeline,
        "contact_info": contact_info,
        "created_at": datetime.now().isoformat(),
        "status": "new"
    }
    
    leads.append(lead)
    AgentTools._save_json(AgentTools.LEADS_FILE, leads)
    
    return f"✓ Lead created in CRM: {lead['lead_id']}"


@tool
def book_test_drive(customer_name: str = "Valued Customer", 
                    vehicle_model: str = "Selected Vehicle", 
                    date_time: str = "To be confirmed",
                    contact_info: str = "") -> str:
    """
    Book a test drive appointment.
    Args:
        customer_name: Customer's name (optional)
        vehicle_model: Vehicle they want to test drive (optional)
        date_time: Appointment date and time (optional)
        contact_info: Email or phone for confirmation (optional)
    Returns:
        Confirmation with appointment ID
    """
    appointments = AgentTools._load_json(AgentTools.APPOINTMENTS_FILE)
    
    import uuid
    confirmation_number = f"TD-{str(uuid.uuid4())[:8].upper()}"
    
    appointment = {
        "confirmation_number": confirmation_number,
        "customer_name": customer_name,
        "vehicle_model": vehicle_model,
        "date_time": date_time,
        "contact_info": contact_info,
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "location": "AutoXloo Premium Dealership, 123 Main St"
    }
    
    appointments.append(appointment)
    AgentTools._save_json(AgentTools.APPOINTMENTS_FILE, appointments)
    
    return f"✓ Test drive request created. Confirmation: {confirmation_number}. Our team will contact you to confirm details."


@tool
def send_confirmation_email(email: str, appointment_details: str) -> str:
    """
    Send appointment confirmation email.
    Args:
        email: Customer email address
        appointment_details: Details to include in confirmation
    Returns:
        Status of email send
    """
    # Mock email - in production would use SendGrid
    print(f"📧 EMAIL SENT to {email}")
    print(f"Subject: Your Test Drive Appointment Confirmed")
    print(f"Details: {appointment_details}")
    
    return f"✓ Confirmation email sent to {email}"


@tool
def get_vehicle_details(stock_number: str) -> str:
    """
    Get detailed information about a specific vehicle.
    Args:
        stock_number: Vehicle stock number (e.g., AX10001)
    Returns:
        Vehicle details
    """
    # This would query the inventory
    return f"✓ Retrieved details for vehicle {stock_number}"


# Export all tools
AGENT_TOOLS = [
    check_calendar_availability,
    create_crm_lead,
    book_test_drive,
    send_confirmation_email,
    get_vehicle_details
]
