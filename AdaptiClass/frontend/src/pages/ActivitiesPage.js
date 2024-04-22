import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import { useParams } from "react-router-dom";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { BackArrowIcon, DownArrowIcon } from "../assets/Icons";
import ActivityHeader from "../components/ActivitiesPageHeader";
import AssessmentActivity from "./Assessment";
import LessonActivity from "./Lesson";
import ExerciseActivity from "./Exercise";
import { PageLoader } from "./helperScreens/PageLoader";
import { FailedToLoadPage } from "./helperScreens/FailedToLoad";


const Container = styled.div`
  width: 100%;
  display: flex;
  background-color: #fff;
`;

const ColumnWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const AssignmentsDetail = ({webgazerToggle, webgazerActive}) => {
  const navigate = useNavigate();
  
  let { course_id, assignment_id } = useParams();
  const [assignmentData, setAssignmentData] = useState(null);
  const [currentActivity, setCurrentActivity] = useState(null);
  const [activityData, setActivityData] = useState(null);

  const backButtonCallback = () => {
    return navigate(-1);
  }
  
  const toggleCurrentActivity = (activity) => {
    if (currentActivity){
      //Change the current activity. 
      setCurrentActivity(activity);
    }
  };

  //Corresponds to activity data state var
  const updateQuestionData = (index, updatedQuestion) => {
    setActivityData((prevQuestions) => {
      const newQuestions = [...prevQuestions];
      newQuestions[index] = updatedQuestion;
      return newQuestions;
    });
  };

  const loadActivity = () => {
    if (currentActivity === null || activityData === null) {
      return <PageLoader/>;
    }

    if (currentActivity['type'] === "Lesson") {
      return <LessonActivity/>;
    } else if (currentActivity['type']=== "Exercise") {
      return <ExerciseActivity/>
    } else if (currentActivity['type']=== "Assessment"){
      return <AssessmentActivity questions={activityData} currentActivity={currentActivity} updateQuestionData={updateQuestionData}/>
    } else {
      return <FailedToLoadPage/>
    }
  }

  //Fetch Assignment Data
  const fetchAssignmentData = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/student/assignment/${assignment_id}/`,
        { params: { user_id: sessionStorage.getItem("user_id") } }
      );
      setAssignmentData(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const fetchActivityData = async () => {
    if (currentActivity){
      try {
        const response = await axios.get(`http://127.0.0.1:8000/userquestions/${currentActivity['id']}/`, { params: { user_id: sessionStorage.getItem("user_id") } });
        setActivityData(response.data);
      } catch (error) {
        console.log(error);
      }
    }
  };

  
  useEffect(() => {
    
    fetchAssignmentData();
  
  }, []);

  useEffect(()=> {
    console.log(assignmentData);
    if (assignmentData){
      //Get the first incomplete activity to start
      for (let i =0; i<assignmentData["activities"].length; i++){
        if (!assignmentData['activities'][i]["is_complete"]) {
          setCurrentActivity(assignmentData['activities'][i]);
          break;
        }
      }
      
      if (currentActivity === null) {
        setCurrentActivity(assignmentData["activities"][0]);
      }
    }
    
  },[assignmentData]);

  useEffect(()=>{
    if (currentActivity) {
      fetchActivityData();
    }
    
  }, [currentActivity]);

  useEffect(()=>{
    console.log(activityData);
  }, [activityData]);

  return (
    <Container>
      <ColumnWrapper>
        {assignmentData && currentActivity &&
        <ActivityHeader 
          backButtonCallback={backButtonCallback}
          course_name={assignmentData['course_name']}
          assignment_id={assignment_id}
          title={assignmentData['title']}
          activities={assignmentData['activities']}
          currentActivity={currentActivity}
          toggleCurrentActivity={toggleCurrentActivity}
          webgazerActive={webgazerActive}
          webgazerToggle={webgazerToggle}
        />}
        {loadActivity()}
      </ColumnWrapper>
    </Container>
  );
};

export default AssignmentsDetail;
