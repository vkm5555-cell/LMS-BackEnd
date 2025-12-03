from pydantic import BaseModel
from typing import List

class StudentBatchAssignmentCreate(BaseModel):
    student_ids: List[int]