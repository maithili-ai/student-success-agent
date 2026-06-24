import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")

def load_progress() -> dict:
    if not os.path.exists(DATA_FILE):
        return {"total_days": 0, "completed_days": 0, "log": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def mark_day_complete(day: int, note: str = "") -> dict:
    progress = load_progress()
    progress.setdefault("total_days", 7)
    progress.setdefault("completed_days", 0)
    progress.setdefault("log", [])
    
    progress["completed_days"] = max(progress["completed_days"], day)
    progress["log"].append({
        "day": day,
        "completed_at": datetime.now().isoformat(),
        "note": note
    })
    percentage = round((progress["completed_days"] / progress["total_days"]) * 100)
    progress["percentage"] = percentage
    
    with open(DATA_FILE, "w") as f:
        json.dump(progress, f, indent=2)
    
    return {
        "completed": f"{progress['completed_days']}/{progress['total_days']} days",
        "progress": f"{percentage}%"
    }
    percentage = round((progress["completed_days"] / progress["total_days"]) * 100) if progress["total_days"] > 0 else 0
    progress["percentage"] = percentage
    with open(DATA_FILE, "w") as f:
        json.dump(progress, f, indent=2)
    return {
        "completed": f"{progress['completed_days']}/{progress['total_days']} days",
        "progress": f"{percentage}%"
    }

def set_total_days(total: int):
    progress = load_progress()
    progress["total_days"] = total
    with open(DATA_FILE, "w") as f:
        json.dump(progress, f, indent=2)

if __name__ == "__main__":
    set_total_days(7)
    print(mark_day_complete(1, "Covered ER diagrams and SQL basics"))
    print(mark_day_complete(2, "Covered normalization"))