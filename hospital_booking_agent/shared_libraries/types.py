from typing import Dict, List, Optional

from google.genai import types
from pydantic import BaseModel, Field

json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

class PatientProfile(BaseModel):
    """Model representing a patient's profile."""
    name: str = Field(description="The full name of the patient.")
    date_of_birth: str = Field(description="The date of birth of the patient in YYYY-MM-DD format.")
    phone: Optional[str] = Field(description="The phone number of the patient.")
    email: Optional[str] = Field(description="The email address of the patient.")
    address: Optional[str] = Field(description="The physical address of the patient.")

class SymtomInputSchema(BaseModel):
    """Input schema for symptoms."""
    symptom: str = Field(description="A detailed description of the symptoms the patient is experiencing.")

class ServiceLoaderInput(BaseModel):
    service_code: str

# Định nghĩa schema input
class SpecialtyInput(BaseModel):
    reason: str

# Định nghĩa schema output
class SpecialtyOutput(BaseModel):
    specialties: List[str]

# Timeline Tool Schemas
class TimelineInput(BaseModel):
    specialty: str
    hospital_id: str

class TimelineOutput(BaseModel):
    available_slots: List[str]

# Doctor Tool Schemas
class DoctorInput(BaseModel):
    specialty: str
    constraints: Dict[str, str]  # hoặc Dict[str, Any] nếu constraint phức tạp

class DoctorOutput(BaseModel):
    doctor_id: str
    doctor_name: str

# Hospital Services Agent Schemas
class HospitalServicesInput(BaseModel):
    hospital_id: str

class HospitalServicesOutput(BaseModel):
    services: List[str]