from datetime import datetime
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Modern Parking System - Kenya")

# Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend HTML directly at the root URL so Render acts as a complete website
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "../Frontend/index.html")
    if os.path.exists(frontend_path):
        with open(frontend_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Frontend index.html not found. Please check file path.</h3>"

class PaymentRequest(BaseModel):
    plate_number: str
    payment_method: str  # "M-Pesa", "Card", "Cash"
    amount_paid: float

# In-memory audit trail for demonstration
audit_logs = []

@app.post("/exit/pay")
def process_payment(data: PaymentRequest):
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