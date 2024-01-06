 
from fastapi import FastAPI, HTTPException
from mongoengine import (
    connect,
    disconnect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    IntField
)
import json
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    mongo_uri = f'mongodb://mongo:27017/fast-api-database'
    # Set the correct parameters to connect to the database
    connect("fast-api-database", host=mongo_uri, port=27017)


@app.on_event("shutdown")
def shutdown_db_client():
    # Set the correct parameters to disconnect from the database
    disconnect("fast-api-database")


# Helper functions to convert MongeEngine documents to json

def course_to_json(course):
    course = json.loads(course.to_json())
    course["students"] = list(map(lambda dbref: str(dbref["$oid"]), course["students"]))
    course["id"] = str(course["_id"]["$oid"])
    course.pop("_id")
    return course


def student_to_json(student):
    student = json.loads(student.to_json())
    student["id"] = str(student["_id"]["$oid"])
    student.pop("_id")
    return student

# Schema

class Student(Document):
    # Implement the Student schema according to the instructions
    name  = StringField(required=True)
    student_number = IntField()


class Course(Document):
    # Implement the Course schema according to the instructions
    name = StringField(required=True)
    description = StringField()
    tags = ListField(StringField())
    students = ListField(ReferenceField(Student))
    

# Input Validators

class CourseData(BaseModel):
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    students: Optional[List[str]] = None


class StudentData(BaseModel):
    name: str
    student_number: Optional[int] = None


# Student routes
# Complete the Student routes similarly as per the instructions provided in A+
@app.post("/students", status_code=201)
def create_student(student: StudentData):
    new_student = Student(**student.dict()).save()
    student_return = student_to_json(new_student)
    return {"message": "Student successfully created", "id": student_return["id"]}

@app.get("/students/{student_id}")
def get_student_id(student_id: str):
    student = Student.objects.get(id=student_id)
    return student_to_json(student)

@app.put("/students/{student_id}", status_code=200)
def update_student(student_id: str, student: StudentData):
    Student.objects.get(id=student_id).update(**student.dict())
    return {"message": "Student successfully updated"}

@app.delete("/students/{student_id}", status_code=200)
def delete_student(student_id: str):
    Student.objects(id=student_id).delete()
    return {"message": "Student successfully deleted"}

# Course routes
# Complete the Course routes similarly as per the instructions provided in A+
@app.post("/courses", status_code=201)
def create_course(course_data: CourseData):
    course = Course(
        name=course_data.name,
        description=course_data.description,
        tags=course_data.tags
    )
    for student_id in course_data.students:
        student = Student.objects(id=student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        course.students.append(student)
    course.save()
    return {"message": "Course successfully created", "id": str(course.id)}

@app.get("/courses")
def get_courses(tag: Optional[str] = None, studentName: Optional[str] = None):
    try:
        query = {}
        if tag:
            query["tags"] = tag
        if studentName:
            student = Student.objects(name=studentName).first()
            if not student:
                raise HTTPException(status_code=404, detail=f"Student with name '{studentName}' not found")
            query["students"] = student
        courses = Course.objects(**query)
        return [course_to_json(course) for course in courses]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses/{course_id}", status_code=200)
async def get_course_id(course_id):
    course = course_to_json(Course.objects.get(id=course_id))
    # course["students"] = course["students"][0]["$oid"]
    return course

@app.delete("/courses/{course_id}")
def delete_course(course_id: str):
    course = Course.objects(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.delete()
    return {"message": "Course successfully deleted"}

@app.put("/courses/{course_id}", status_code=200)
async def update_course(course_id, course: CourseData):
    Course.objects.get(id=course_id).update(**course.dict())
    return { "message": "Course successfully updated"}

