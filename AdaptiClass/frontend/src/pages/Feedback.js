import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Grades from '../components/Grades';
import CourseGrade from '../components/CourseGrade';
import InstructorFeedback from '../components/InstructorFeedback';
import TimeFeedback from '../components/TimeFeedback'; 

const Content = styled.div`
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
`;

const DropdownContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
  position: absolute;
  right: 0;
  top: 70px;
  z-index: 1000;
`;

const Select = styled.select`
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  min-width: 150px;
`;

const TopSection = styled.div`
  display: flex;
  justify-content: flex-start;
  align-items: flex-start; 
  gap: 20px; 
`;

const BottomSection = styled.div`
  display: flex;
  justify-content: flex-start;
  align-items: flex-start; 
  gap: 20px; 
  margin-top: 20px; 
`;


const FeedbackContent = () => {
    const [courses, setCourses] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState('');
    const [grades, setGrades] = useState([]);
    const [overallGrade, setOverallGrade] = useState('');
    const [overallPercent, setOverallPercent] = useState(0);
    const [instructorFeedback, setInstructorFeedback] = useState(null);

    useEffect(() => {
        import('../mockRequests/feedback.json')
            .then(module => {
                const courseData = module.default.courses; 
                setCourses(courseData);
                if (courseData.length > 0) {
                    setSelectedCourse(courseData[0].id);
                }
            });
    }, []);
    
    useEffect(() => {
        const currentCourse = courses.find(course => course.id === selectedCourse);
        if (currentCourse) {
            setGrades(currentCourse.grades || []);
            setOverallGrade(currentCourse.overallGrade || '');
            setOverallPercent(currentCourse.overallPercent || 0);
            setInstructorFeedback(currentCourse.instructorFeedback || null);
        }
    }, [selectedCourse, courses]);

    const handleCourseChange = (event) => {
        setSelectedCourse(event.target.value);
    };

    return (
        <Content>
            <DropdownContainer>
                <Select value={selectedCourse} onChange={handleCourseChange}>
                    {courses.map(course => (
                        <option key={course.id} value={course.id}>{course.name}</option>
                    ))}
                </Select>
            </DropdownContainer>
            <TopSection>
        <CourseGrade grade={overallGrade} percentage={overallPercent} />
        {instructorFeedback && (
          <InstructorFeedback feedback={instructorFeedback} />
        )}
      </TopSection>
      <BottomSection>
        <Grades grades={grades} />
        {selectedCourse && (
          <TimeFeedback timeData={courses.find(course => course.id === selectedCourse)?.timeSpentPerDay || {}} />
        )}
      </BottomSection>
    </Content>
  );
};

export default FeedbackContent;