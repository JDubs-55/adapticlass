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
  justify-content: flex-start;
  align-items: center;
`;

const Title = styled.div`
  color: #3f434a;
  margin-left: 20px;
  font-size: 20px;
  font-weight: 500;
`;

const DropdownContainer = styled.div`
  position: relative;
`;

const CourseDropdown = styled.div`
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

const CourseButton = styled.button`
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

const FeedbackHeader = ({
  courses,
  currentCourse,
  setCurrentCourse
}) => {
  const [showCourseDropdown, setShowCourseDropdown] = useState(false);
  const courseDropdownRef = useRef(null);
  const navigate = useNavigate();

  //Activity Dropdown Functions
  const toggleCourseDropdown = () => {
    if (courses.length > 1) {
      setShowCourseDropdown(!showCourseDropdown);
    }
  };

  const handleClickOutside = (event) => {
    const dropdownTrigger = document.getElementById(
      "course-dropdown-trigger"
    );
    if (
      courseDropdownRef.current &&
      !courseDropdownRef.current.contains(event.target) &&
      event.target !== dropdownTrigger &&
      !dropdownTrigger.contains(event.target)
    ) {
      setShowCourseDropdown(false);
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);
  
  return (
    <PageHeaderContainer>
        <Title>Feedback</Title>
        <DropdownContainer>
          <CourseDropdown
            onClick={toggleCourseDropdown}
            id="course-dropdown-trigger"
          >
            {currentCourse ? currentCourse["name"] : ""}
            <DownArrowIcon />
          </CourseDropdown>
          <DropdownContent
            $show={showCourseDropdown}
            ref={courseDropdownRef}
          >
            <ButtonsWrapper>
              {currentCourse && courses.map((course) => {
                if (course["id"] !== currentCourse["id"]) {
                  return (
                    <CourseButton
                      key={course["id"]}
                      onClick={() => setCurrentCourse(course)}
                    >
                      {course["name"]}
                    </CourseButton>
                  );
                } else {
                  return null;
                }
              })}
            </ButtonsWrapper>
          </DropdownContent>
        </DropdownContainer>
    </PageHeaderContainer>
  );
};

export default FeedbackHeader;
