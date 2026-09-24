from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Modern Parking System - Kenya")
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pydantic import BaseModel
from datetime import datetime

from fastapi.responses import HTMLResponse
import os

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    # Looks for index.html in the Frontend folder relative to backend
    frontend_path = os.path.join(os.path.dirname(__file__), "../Frontend/index.html")
    if os.path.exists(frontend_path):
        with open(frontend_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Frontend index.html not found. Please check file path.</h3>"

class PaymentRequest(BaseModel):
    plate_number: str
    payment_method: str  # "M-Pesa", "Card", "Cash"
    amount_paid: float

# In-memory audit trail for demonstration (or use your database model)
audit_logs = []

@app.post("/exit/pay")
def process_payment(data: PaymentRequest):
    # Simulate payment processing and barrier release
    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "plate_number": data.plate_number,
        "method": data.payment_method,
        "amount_kes": data.amount_paid,
        "status": "Confirmed & Barrier Opened"
    }
    audit_logs.append(audit_record)
    return {
        "message": f"Payment of KES {data.amount_paid} received via {data.payment_method}.",
        "barrier": "OPEN",
        "receipt": audit_record
    }

@app.get("/admin/audit-logs")
def get_audit_logs():
    total_collection = sum(log["amount_kes"] for log in audit_logs)
    return {
        "total_revenue_kes": total_collection,
        "transaction_count": len(audit_logs),
        "records": audit_logs
    }

app = FastAPI(title="Modern Parking System - Kenya")

# Enable CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for local testing)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ... (keep the rest of your existing slot and vehicle code below this)

# Data Structure: Representing parking slots using a List/Array
# True = Available, False = Occupied (or tracking vehicle details)
TOTAL_SLOTS = 10
parking_slots = {i: {"is_occupied": False, "vehicle_plate": None, "entry_time": None} for i in range(1, TOTAL_SLOTS + 1)}

# Active parking records (Hash Map / Dictionary for O(1) lookups by plate)
active_vehicles = {}

class VehicleEntry(BaseModel):
    plate_number: str

@app.get("/slots")
def get_parking_slots():
    """Visual display of parking slots available"""
    return {
        "total_slots": TOTAL_SLOTS,
        "slots": parking_slots
    }

@app.post("/entry")
def vehicle_entry(data: VehicleEntry):
    """Algorithm: Find first available slot and record arrival"""
    plate = data.plate_number.upper()
    
    # Check if vehicle is already parked
    if plate in active_vehicles:
        raise HTTPException(status_code=400, detail="Vehicle is already inside the parking system.")

    # Find the first available slot (Linear Search Algorithm: O(N))
    available_slot = None
    for slot_id, details in parking_slots.items():
        if not details["is_occupied"]:
            available_slot = slot_id
            break
            
    if available_slot is None:
        raise HTTPException(status_code=400, detail="Parking is full! No slots available.")
    
    # Record entry details
    entry_time = datetime.now()
    parking_slots[available_slot] = {
        "is_occupied": True,
        "vehicle_plate": plate,
        "entry_time": entry_time.isoformat()
    }
    
    active_vehicles[plate] = {
        "slot_id": available_slot,
        "entry_time": entry_time
    }
    
    return {
        "message": f"Barrier Open. Welcome! Assigned to Slot {available_slot}",
        "slot_id": available_slot,
        "plate_number": plate,
        "entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/exit")
def vehicle_exit(data: VehicleEntry):
    """Algorithm: Calculate total time spent and fee (KES), then open barrier"""
    plate = data.plate_number.upper()
    
    if plate not in active_vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found in active parking records.")
    
    record = active_vehicles[plate]
    slot_id = record["slot_id"]
    entry_time = record["entry_time"]
    
    # Calculate duration
    exit_time = datetime.now()
    duration_seconds = (exit_time - entry_time).total_seconds()
    hours = duration_seconds / 3600
    
    # Fee calculation logic: e.g., KES 100 per hour (minimum KES 50)
    rate_per_hour = 100
    fee = max(50, round(hours * rate_per_hour, 2))
    
    # Free up the slot
    parking_slots[slot_id] = {
        "is_occupied": False,
        "vehicle_plate": None,
        "entry_time": None
    }
    del active_vehicles[plate]
    
    return {
        "message": "Payment confirmed. Barrier Open. Goodbye!",
        "plate_number": plate,
        "slot_id": slot_id,
        "duration_hours": round(hours, 2),
        "amount_to_pay_kes": fee,
        "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S")
    }
@app.get("/")
def read_root():
    return {"message": "Modern Parking System API is running successfully"}