import React, { useState, useEffect, Component } from "react";
import styled from "styled-components";
import Grades from "../components/Grades";
import CourseGrade from "../components/CourseGrade";
import InstructorFeedback from "../components/InstructorFeedbackPane";
import TimeFeedback from "../components/TimeFeedback";
import FeedbackHeader from "../components/FeedbackHeader";
import AssignmentResults from "../components/FeedbackAssignmentResultSummary";
import axios from "axios";


const ComponentWrapper = styled.div`
  width: 100%;
  display: flex;
  
  background-color: #f8f8f8;
`;

const ColumnWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const MainContentWrapper = styled.div`
  width: 100%;
  display: flex;
  height: calc(100vh - 140px);

  display: flex;
  align-items: center;
  justify-content: center;
`;

const MainContent = styled.div`
  width: calc(100% - 40px);
  height: calc(100% - 40px);
  margin: 20px;
  
  display: flex;
  flex-direction:column;
  align-items: flex-start;
  overflow-y: auto;
  gap: 20px;

`;

const Row = styled.div`
  width: 100%;
  display: flex;
  gap: 20px;
`;

const AssignmentDetailCol = styled.div`
  width: calc(100% - 540px);
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const QuestionsContainer = styled.div`
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
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
  const [courses, setCourses] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState(null);

  const [grades, setGrades] = useState(null);
  const [selectedAssignment, setSelectedAssignment] = useState(null);

  const [engagementData, setEngagementData] = useState(null);

  const handleSetCourse = (course) => {
    setSelectedCourse(course);
  };

  const handleSetAssignment = (assignment) => {
    console.log(assignment);
    setSelectedAssignment(assignment);
  };

  const calcLetterGrade = (percentage) => {
      if (percentage >= 97) {
          return 'A+';
      } else if (percentage >= 93) {
          return 'A';
      } else if (percentage >= 90) {
          return 'A-';
      } else if (percentage >= 87) {
          return 'B+';
      } else if (percentage >= 83) {
          return 'B';
      } else if (percentage >= 80) {
          return 'B-';
      } else if (percentage >= 77) {
          return 'C+';
      } else if (percentage >= 73) {
          return 'C';
      } else if (percentage >= 70) {
          return 'C-';
      } else if (percentage >= 67) {
          return 'D+';
      } else if (percentage >= 63) {
          return 'D';
      } else if (percentage >= 60) {
          return 'D-';
      } else {
          return 'F';
      }
  };

  const fetchCourseData = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/enrollments/${sessionStorage.getItem("user_id")}`
      );
      setCourses(response.data);
      setSelectedCourse(response.data[0]);
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const fetchGradeData = async (course_id) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/feedbackpagedata/${course_id}`, { params: { user_id: sessionStorage.getItem("user_id") } });
      setGrades(response.data["grades"]);
      setEngagementData(response.data["engagement_data"]);
      if (response.data["grades"][0]) {
        setSelectedAssignment(response.data["grades"][0]);
      }
      
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    fetchCourseData();
  }, []);

  useEffect(()=>{
    if (selectedCourse){
      fetchGradeData(selectedCourse["id"])
    }
    
  },[selectedCourse])

  return (
    <ComponentWrapper>
      <ColumnWrapper>
        {courses && selectedCourse && (
          <FeedbackHeader
            courses={courses}
            currentCourse={selectedCourse}
            setCurrentCourse={handleSetCourse}
          ></FeedbackHeader>
        )}
        <MainContentWrapper>
          <MainContent>
            <Row>
              {grades && <Grades grades={grades} handleSetAssignment={handleSetAssignment}/>}
              <AssignmentDetailCol>
                {selectedAssignment && <AssignmentResults assessment={selectedAssignment}/>}
                {selectedCourse && <InstructorFeedback instructor={selectedCourse["instructor"]}/>}
              </AssignmentDetailCol>
            </Row>
            <Row>
              {engagementData && <TimeFeedback timeData={engagementData}/>}
              {selectedCourse && <CourseGrade percentage={selectedCourse["grade"]} grade={()=>calcLetterGrade(selectedCourse['grade'])}/>}
            </Row>
            
            
          </MainContent>
        </MainContentWrapper>
      </ColumnWrapper>
    </ComponentWrapper>
  );
};

export default FeedbackContent;
