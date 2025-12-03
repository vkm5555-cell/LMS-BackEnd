from .base import BaseRepository
from app.models.student import Student

class StudentRepository(BaseRepository[Student]):
    def __init__(self):
        super().__init__(Student)
