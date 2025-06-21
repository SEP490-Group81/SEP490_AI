from typing import List, Optional

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
