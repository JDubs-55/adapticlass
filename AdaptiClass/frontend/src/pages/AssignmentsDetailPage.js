import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import Questions from "../components/Questions";
import ProgressBar from "../components/ProgressBar";
import ChatBox from "../components/Chatbox";
import assignments from "../mockRequests/assignments.json";
import { useParams } from "react-router-dom";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { BackArrowIcon, DownArrowIcon } from "../assets/Icons";

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

const MainLayout = styled.div`
  width: 100%;
  display: flex;
  align-items: flex-start;
  height: calc(100vh - 140px);
  overflow-y: hidden;
  background-color: #f8f8f8;
`;

const QuestionsContainer = styled.div`
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
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

const AssignmentsDetail = ({webgazerToggle, webgazerActive, setUserAndActivityID}) => {
  const navigate = useNavigate();
  const [showActivityDropdown, setShowActivityDropdown] = useState(false);
  const activityDropdownRef = useRef(null);

  let { course_id, assignment_id } = useParams();
  const [assignmentData, setAssignmentData] = useState({});
  const [currentActivity, setCurrentActivity] = useState(null);

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const totalQuestions = assignments.length;
  const [quizCompleted, setQuizCompleted] = useState(false);

  //Activity Dropdown Functions
  const toggleActivityDropdown = () => {
    if (assignmentData["activities"].length > 1) {
      setShowActivityDropdown(!showActivityDropdown);
    }
  };

  const toggleCurrentActivity = (activity) => {
    setCurrentActivity(activity);
    setUserAndActivityID(sessionStorage.get('user_id'), currentActivity['id']);
  };

  const handleClickOutside = (event) => {
    const dropdownTrigger = document.getElementById(
      "activity-dropdown-trigger"
    );
    if (
      activityDropdownRef.current &&
      !activityDropdownRef.current.contains(event.target) &&
      event.target !== dropdownTrigger &&
      !dropdownTrigger.contains(event.target)
    ) {
      setShowActivityDropdown(false);
    }
  };

  //Fetch Assignment Data
  const fetchAssignmentData = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/student/assignment/${assignment_id}/`,
        { params: { user_id: sessionStorage.getItem("user_id") } }
      );
      setAssignmentData(response.data);

      //Get the first incomplete activity to start
      response.data["activities"].forEach((activity) => {
        if (!activity["is_complete"]) {
          setCurrentActivity(activity);
        }
      });

      if (currentActivity === null) {
        setCurrentActivity(response.data["activities"][0]);
      }

      console.log(assignmentData);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleClickOutside);

    fetchAssignmentData();
    if (sessionStorage.get('user_id') !== null && currentActivity) {
      setUserAndActivityID(sessionStorage.get('user_id'), currentActivity['id']);
    }
    

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  return (
    <Container>
      <ColumnWrapper>
        <PageHeaderContainer>
          <AssignmentInfoHeaderContainer>
            <BackIconContainer onClick={() => navigate(-1)}>
              <BackArrowIcon />
            </BackIconContainer>
            <AssignmentTitle>
              {assignmentData
                ? `${assignmentData["course_name"]} - ${assignmentData["title"]}`
                : ""}
            </AssignmentTitle>
            <DropdownContainer>
              <ActivityDropdown
                onClick={toggleActivityDropdown}
                id="activity-dropdown-trigger"
              >
                {currentActivity ? currentActivity["type"] : ""}
                <DownArrowIcon />
              </ActivityDropdown>
              <DropdownContent
                $show={showActivityDropdown}
                ref={activityDropdownRef}
              >
                <ButtonsWrapper>
                  {assignmentData["activities"] &&
                    assignmentData["activities"].map((activity) => {
                      if (activity["id"] !== currentActivity["id"]) {
                        return (
                          <ActivityButton
                            onClick={() => toggleCurrentActivity(activity)}
                          >
                            {activity["type"]}
                          </ActivityButton>
                        );
                      } else {
                        return null;
                      }
                    })}
                </ButtonsWrapper>
              </DropdownContent>
            </DropdownContainer>
          </AssignmentInfoHeaderContainer>
          <ButtonControlsContainer>
            <WebGazerButton $webgazerActive={webgazerActive} onClick={webgazerToggle}>Toggle Webgazer</WebGazerButton>
            <SubmitButton className="next">Submit</SubmitButton>
          </ButtonControlsContainer>
        </PageHeaderContainer>
        <MainLayout>
          <QuestionsContainer>
            <Questions
              updateCurrentIndex={setCurrentQuestionIndex}
              totalQuestions={totalQuestions}
              setQuizCompleted={setQuizCompleted}
            />

            <ProgressBar
              current={currentQuestionIndex + 1}
              total={totalQuestions}
              quizCompleted={quizCompleted}
            />
          </QuestionsContainer>
          <ChatBox />
        </MainLayout>
      </ColumnWrapper>
    </Container>
  );
};

export default AssignmentsDetail;
