import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import { BackArrowIcon, DownArrowIcon } from "../assets/Icons";
import axios from "axios";
import { useNavigate } from "react-router-dom";

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
  font-family: "Poppins";
  text-align: center;
  color: #fff;

  &.next {
    border: solid 2px #e8e9eb;
    color: #8a9099;
    background-color: #fff;

    &:hover {
      background-color: #e8e9eb;
    }
  }

  &.finish {
    border: solid 2px #49c96d;
    color: #fff;
    background-color: #49c96d;

    &:hover {
      border: solid 2px #20a144;
      background-color: #20a144;
    }
  }
`;

const WebGazerButton = styled.button`
  margin: 10px 0;
  padding: 10px 20px;
  border: solid 2px #304ffd;
  background-color: ${(props) => (props.$webgazerActive ? "#fff" : "#304ffd")};
  border-radius: 14px;

  display: flex;
  justify-content: center;
  align-items: center;

  font-weight: 500;
  font-size: 16px;
  font-family: "Poppins";
  text-align: center;
  color: ${(props) => (props.$webgazerActive ? "#304ffd" : "#fff")};
`;

const ActivityHeader = ({
  backButtonCallback,
  course_name,
  assignment_id,
  title,
  activities,
  currentActivity,
  toggleCurrentActivity,
  webgazerActive,
  webgazerToggle,
}) => {
  const [showActivityDropdown, setShowActivityDropdown] = useState(false);
  const activityDropdownRef = useRef(null);
  const navigate = useNavigate();

  //Activity Dropdown Functions
  const toggleActivityDropdown = () => {
    if (activities.length > 1) {
      setShowActivityDropdown(!showActivityDropdown);
    }
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

  useEffect(() => {
    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  const allActivitiesComplete = () => {
    if (!activities){
        return false;
    }

    var res = true;
    for(let i =0; i<activities.length; i++){
        if (!activities[i]['is_complete']){
            res = false;
        }
    }
    return res;
  };

  const getNextIncompleteActivity = () => {
    if (!activities){
        return currentActivity;
    }

    for(let i = 0; i<activities.length; i++){
        if (activities[i]['id'] != currentActivity['id']){
            return activities[i];
        }
    }

    return currentActivity;
  };

  const nextClicked = () => {
    console.log("Clicked");
    var nextActivity = getNextIncompleteActivity();
    console.log(nextActivity);
    if (!nextActivity || nextActivity===currentActivity) {
        console.log("No next activity");
        return;
    }
    console.log(nextActivity);
    toggleCurrentActivity(nextActivity);
  }

  const assignmentFinished = async () => {
    try {
      const response = await axios.put('http://127.0.0.1:8000/assignmentcompleted/', null, { params: { user_id: sessionStorage.getItem("user_id"), assignment_id: assignment_id }});
      console.log(response);

      if (response.status == 202) {
        navigate(-1);
      } 
    } catch (error) {
      console.log(error)
    }
  };
  
  return (
    <PageHeaderContainer>
      <AssignmentInfoHeaderContainer>
        <BackIconContainer onClick={backButtonCallback}>
          <BackArrowIcon />
        </BackIconContainer>
        <AssignmentTitle>{`${course_name} - ${title}`}</AssignmentTitle>
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
              {activities.map((activity) => {
                if (activity["id"] !== currentActivity["id"]) {
                  return (
                    <ActivityButton
                      key={activity["id"]}
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
        <WebGazerButton
          disabled={!currentActivity}
          $webgazerActive={webgazerActive}
          onClick={() => webgazerToggle()}
        >
          Toggle Webgazer
        </WebGazerButton>
        {allActivitiesComplete() ? <SubmitButton className="finish" onClick={assignmentFinished}>Finish</SubmitButton> : <SubmitButton className="next" onClick={nextClicked}>Next</SubmitButton>}
      </ButtonControlsContainer>
    </PageHeaderContainer>
  );
};

export default ActivityHeader;
