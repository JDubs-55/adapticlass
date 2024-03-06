# AdaptiClass Backend

## Endpoints
### Student Model
```students/``` <br>
(GET) - Returns a list of all current students. <br>
(POST) - Allows for the creation of a new student.
- The request should take the form of:
```
{
    "name": "StudentName",
    "email": "StudentEmail"
}
```

```students/<str:email>/``` <br>
(GET) - Returns the information of the individual student matching the email passed in the endpoint. <br>
(PUT) - Allows for editing the student's information.
- (<b>NOTE:</b> The email must be provided to alter the student's information.)
- The request to edit the name should take the form of:
```
{
    "name": "NewName",
    "email": "StudentEmail"
}
```
(DELETE) - Deletes the student.
<br>
<br>

### Instructor Model
```instructors/``` <br>
(GET) - Returns a list of all current instructors. <br>
(POST) - Allows for the creation of a new instructor.
- The request should take the form of:
```
{
    "name": "InstructorName",
    "email": "InstructorEmail"
}
```

```instructors/<str:email>/``` <br>
(GET) - Returns the information of the individual instructor matching the email passed in the endpoint. <br>
(PUT) - Allows for editing the student's information.
- (<b>NOTE:</b> The email must be provided to alter the instructor's information.)
- The request to edit the name should take the form of:<br>
```
{
    "name": "NewName",
    "email": "InstructorEmail"
}
```
(DELETE) - Deletes the instructor.
<br>
<br>

### Course Model
```courses/``` <br>
(GET) - Returns all courses along with their information. <br>
(POST) - Allows for the creation of a new course.
- (<b>NOTE</b>: Creating a course requires the course name and instructor's email.)
- The request should take the form of:
```
{
    "name":"CourseName",
    "instructor":"InstructorEmail"
}
```

```courses/<str:name>/``` <br>
(GET) - Returns the information about the individual course whose name is passed in the endpoint. <br>
(PUT) - Allows for the editing of the course name and instructor. Also allows for the addition of new student(s).
- The request to edit the course name should take the form of:
```
{
    "name":"NewCourseName"
}
```
- The request to edit the instructor should take the form of:
```
{
    "instructor":"NewInstructorEmail"
}
```
- The request to add students to the course should take the form of:<br>
```
{
    "students":"StudentEmail"
}
```
```
{
    "students":["Student1Email", "Student2Email", ...]
}
```
(DELETE) - Deletes the course and all course information.

```courses/<str:name>/removestudents/``` <br>
(GET) - Returns the information about the individual course whose name is passed in the endpoint. <br>
(PUT) - Removes student(s) from the course.
- The request to remove student(s) should take the form of:
```
{
    "students":"StudentEmail"
}
```
```
{
    "students":["Student1Email", "Student2Email", ...]
}
```
