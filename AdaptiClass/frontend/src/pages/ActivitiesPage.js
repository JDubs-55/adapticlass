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

const PageHeaderContainer = styled.div`
  width: 100%;
  height: 66px;

  border-bottom: 2px solid #ededed;
  background-color: #fff;

  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const AssignmentInfoHeaderContainer = styled.div`
  display: flex;
  align-items: center;
  jusitfy-content: flex-start;
`;

const BackIconContainer = styled.div`
  display: flex;
  align-items: center;

  svg {
    width: 20px;
    height: auto;
    fill: #3f434a;
    margin-left: 30px;
  }

  svg:hover {
    cursor: pointer;
  }
`;

const AssignmentTitle = styled.div`
  color: #3f434a;
  margin-left: 20px;
  font-size: 20px;
  font-weight: 500;
`;

const DropdownContainer = styled.div`
  position: relative;
`;

const ActivityDropdown = styled.div`
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10px;
  gap: 5px;

  color: #8a9099;
  font-size: 18px;
  font-weight: 500;
`;

const DropdownContent = styled.div`
  display: ${(props) => (props.$show ? "block" : "none")};
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  z-index: 1000;
  background-color: white;
  border: 1px solid #e8e9eb;
  border-radius: 14px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: max-content;
`;

const ButtonsWrapper = styled.div`
  margin: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
`;

const ActivityButton = styled.button`
  padding: 10px;
  border: none;
  cursor: pointer;

  width: 100%;
  height: 40px;
  border-radius: 14px;
  background-color: #fff;

  color: #8a9099;
  font-size: 18px;
  font-weight: 500;

  display: flex;
  align-items: center;
  justify-content: flex-start;

  &:hover {
    background-color: #f8f8f8;
    color: #3f434a;
  }
`;

const ButtonControlsContainer = styled.div`
  display: flex;
  gap: 10px;
`;

const SubmitButton = styled.button`
  margin: 10px 0;
  padding: 10px 20px;
  border: none;
  background-color: #304ffd;
  border-radius: 14px;
  margin-right: 20px;

  display: flex;
  justify-content: center;
  align-items: center;

  font-weight: 500;
  font-size: 16px;
  font-family: 'Poppins';
  text-align: center;
  color: #fff;

  &.next {
    border: solid 2px #E8E9EB;
    color: #8A9099;
    background-color: #fff;

    &:hover {
      background-color: #E8E9EB;
    }
  }

  &.finish {
    border: solid 2px #49C96D;
    color: #fff;
    background-color: #49C96D;

    &:hover {
      border: solid 2px #20A144;
      background-color: #20A144;
    }
  }
  

`;

const WebGazerButton = styled.button`
  margin: 10px 0;
  padding: 10px 20px;
  border: solid 2px #304ffd;
  background-color: ${(props)=>(props.$webgazerActive ? "#fff" : "#304ffd")};
  border-radius: 14px;

  display: flex;
  justify-content: center;
  align-items: center;

  font-weight: 500;
  font-size: 16px;
  font-family: 'Poppins';
  text-align: center;
  color: ${(props)=>(props.$webgazerActive ? "#304ffd" : "#fff")};
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

  const loadActivity = () => {
    if (currentActivity === null || activityData === null) {
      return <PageLoader/>;
    }

    if (currentActivity['type'] === "Lesson") {
      return <LessonActivity/>;
    } else if (currentActivity['type']=== "Exercise") {
      return <ExerciseActivity/>
    } else if (currentActivity['type']=== "Assessment"){
      return <AssessmentActivity questions={activityData}/>
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
        const response = await axios.get(`http://127.0.0.1:8000/questions/${currentActivity['id']}/`);
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
