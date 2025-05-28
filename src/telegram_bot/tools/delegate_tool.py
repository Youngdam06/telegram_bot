from pydantic import BaseModel
from enum import Enum
from crewai.tools import tool

# Enum untuk daftar coworker yang valid
class CoworkerEnum(str, Enum):
    schedule_agent = "schedule_agent"
    manager = "manager"

# Schema untuk validasi input
class DelegateWorkSchema(BaseModel):
    task: str
    context: str
    coworker: CoworkerEnum  

# Fungsi untuk mendelegasikan tugas
@tool
def delegate_work(task: str, context: str, coworker: str):
    """Delegates a specific task to a coworker."""
    if coworker == CoworkerEnum.manager:
        return "Manager cannot receive delgated tasks."
    return f"Delegating task: '{task}' to {coworker.value} with context: {context}"
