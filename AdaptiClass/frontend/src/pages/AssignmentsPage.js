import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import AssignmentListContainer from "../components/lists/AssignmentListContainer";
import AssignmentInfoPane from "../components/AssignmentInfoPane";
import assignmentData from "../mockRequests/assignmentsBasic.json";
import axios from "axios";

const Container = styled.div`
  width: 100%;
  display: flex;
  background-color: #fff;
`;

const ColumnWrapper = styled.div`
  width: ${(props) => (props.$showInfoPane ? "60%" : "100%")};
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const PageHeader = styled.div`
  width: 100%;
  height: 66px;

  border-bottom: 2px solid #ededed;
  background-color: #fff;

  display: flex;
  align-items: center;
  justify-content: flex-start;

  h5 {
    color: #3f434a;
    margin-left: 30px;
    font-size: 20px;
    font-weight: 500;
  }
`;

const ListContainer = styled.div`
  height: calc(100vh - 136px);
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  overflow-y: auto;
`;

const InfoPaneContainer = styled.div`
  width: ${(props) =>
    props.$showInfoPane
      ? "40%"
      : "0"}; /* Adjust width based on info pane visibility */
  min-width: ${(props) =>
    props.$showInfoPane
      ? "500px"
      : "0"}; /* Adjust width based on info pane visibility */
  display: ${(props) =>
    props.$showInfoPane
      ? "block"
      : "none"}; /* Show/hide based on info pane visibility */
  border-left: 2px solid #ededed;
`;

const AssignmentPage = () => {
  let { course_id } = useParams();
  const [assignmentData, setAssignmentData] = useState(null)
  const [inProgressAssignmentData, setInProgressAssignmentData] = useState([]);
  const [upcomingAssignmentData, setUpcomingAssignmentData] = useState([]);
  const [completedAssignmentData, setCompletedAssignmentData] = useState([]);
  const [courseData, setCourseData] = useState(null);
  const [showInfoPane, setShowInfoPane] = useState(false);
  const [infoPaneData, setInfoPaneData] = useState({});

  //Retrieve data from server
  useEffect(() => {
    const fetchAssignmentData = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/student/assignments/${course_id}/`,
          { params: { user_id: sessionStorage.getItem("user_id") } }
        );
        setAssignmentData(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    const fetchCourseData = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/courses/${course_id}/`
        );
        setCourseData(response.data);
      } catch (error) {
        console.log(error);
      }
    };

    fetchCourseData();
    
    fetchAssignmentData();

  }, []);

  useEffect(()=>{
    if (assignmentData){
      var inprogress = [];
      var upcoming = [];
      var completed = [];

      assignmentData.forEach((assignment) => {
        if (assignment["status"] === "In Progress") {
          //Append to inprogress list.
          inprogress.push(assignment)
          
        } else if (assignment["status"] === "Upcoming") {
          //Append to upcoming list.
          upcoming.push(assignment)
          
        } else if (assignment["status"] === "Completed") {
          completed.push(assignment)
        } else {
          console.log(
            `Got unexpected assignment status: ${assignment["status"]}`
          );
        }
      });

      setInProgressAssignmentData(inprogress);
      setUpcomingAssignmentData(upcoming);
      setCompletedAssignmentData(completed);
    }

  },[assignmentData]);

  const toggleOnInfoPane = (data) => {
    setShowInfoPane(true);
    setInfoPaneData(data);
  };

  const toggleOffInfoPane = () => {
    setShowInfoPane(false);
  };

  return (
    <Container>
      <ColumnWrapper $showInfoPane={showInfoPane}>
        <PageHeader>
          <h5>{courseData ? courseData["name"] : ""}</h5>
        </PageHeader>
        <ListContainer>
          <AssignmentListContainer
            isLast={false}
            toggleOnInfoPane={toggleOnInfoPane}
            title="In Progress"
            data={inProgressAssignmentData}
          />
          <AssignmentListContainer
            isLast={false}
            toggleOnInfoPane={toggleOnInfoPane}
            title="Upcoming"
            data={upcomingAssignmentData}
          />
          <AssignmentListContainer
            isLast={true}
            toggleOnInfoPane={toggleOnInfoPane}
            title="Completed"
            data={completedAssignmentData}
          />
        </ListContainer>
      </ColumnWrapper>
      <InfoPaneContainer $showInfoPane={showInfoPane}>
        <AssignmentInfoPane
          toggleOffInfoPane={toggleOffInfoPane}
          data={infoPaneData}
          instructorName={
            courseData ? courseData["instructor"]["display_name"] || "" : ""
          }
          instructorImage={
            courseData ? courseData["instructor"]["picture"] || "" : ""
          }
        />
      </InfoPaneContainer>
    </Container>
  );
};

export default AssignmentPage;
