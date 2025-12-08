from sys import modules

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import Base
from app.db.session import db
from app.routers import auth, students, courses, course_type, role_routes, modules, user_router, course_category, course_chapter_routes, organization, session, semester, student_batches_router, student_batch_assignments, student_course_progress_router, transcript_routes, discussions_router, course_assignments
import app.models
# Create tables at startup
Base.metadata.create_all(bind=db.engine)


app = FastAPI(title="LMS API (OOP)")

from fastapi.staticfiles import StaticFiles


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "LMS OOP API running"}
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(course_type.router)
app.include_router(role_routes.router)

app.include_router(modules.router)
app.include_router(user_router.router)
app.include_router(course_category.router)
app.include_router(course_chapter_routes.router)
app.include_router(organization.router)
app.include_router(session.router)
app.include_router(semester.router)
app.include_router(student_batches_router.router)
app.include_router(student_batch_assignments.router)
app.include_router(student_course_progress_router.router)
app.include_router(transcript_routes.router)
app.include_router(discussions_router.router)
app.include_router(course_assignments.router)
