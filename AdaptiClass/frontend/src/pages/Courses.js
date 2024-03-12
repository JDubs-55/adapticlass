import React, { useState, useEffect, useMemo } from "react";
import styled from "styled-components";
//import { FilterIcon } from "../assets/Icons";
import CourseCard from "../components/CourseCard";
import courseData from "../mockRequests/courses.json";

const Content = styled.div`
  width: 100%;
  flex-grow: 1;
  background-color: #f8f8f8;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const PageHeader = styled.div`
  width: calc(100% - 36px); /* 18px on both sides */
  margin: 0 18px; /* 18px on both sides */
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const PageHeaderLabel = styled.h4`
  color: black;
  font-size: 28px;
`;

// const FilterButton = styled.button`
//   height: 40px;
//   width: 40px;
//   background-color: #fff;
//   border: none;
//   padding: 0;
//   border-radius: 14px;
//   display: flex;
//   justify-content: center;
//   align-items: center;

//   svg {
//     width: 20px;
//     height: 20px;
//   }
// `;

const CourseControls = styled.div`
  width: calc(100% - 36px); /* 18px on both sides */
  margin: 0 18px; /* 18px on both sides */
  box-sizing: border-box; /* Include padding and border in the total width */

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;

  height: 40px;
`;

const ControlsButtonContainer = styled.div`
  display: flex;
  gap: 10px;
`;

const ControlsFilterButton = styled.button`
  border: none;
  padding: 0;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background-color: #f8f8f8;
  gap: 5px;
  border-bottom: ${(props) =>
    props.$active ? "1px solid #304FFD" : "1px solid transparent"};
  transition: border-color 0.3s ease;
  padding-bottom: 8px;

  &:hover {
    border-bottom: 1px solid #304ffd;
  }
`;

const ButtonLabelText = styled.body`
  font-size: 15px;
  color: #8a9099;
`;

const ButtonLabelCount = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;

  border-radius: 6px;
  padding: 2px 10px;
  background-color: #e8e9eb;

  body {
    color: #8a9099;
    font-size: 10px;
    font-weight: 600px;
  }
`;

const HorizontalSeparator = styled.div`
  height: 1px;
  width: 100%;
  background-color: #e8e9eb;
`;

const CoursesCardContainer = styled.div`
  width: calc(100% - 36px); /* 18px on both sides */
  margin: 0 18px; /* 18px on both sides */
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: center;
  gap: 18px;
  margin-top: 18px;
  overflow-y: auto;
  max-height: 594px;
`;

const CourseContent = () => {
  const [jsonData, setJsonData] = useState(null);
  const [filterType, setFilterType] = useState("Current");

  //Retrieve data from server
  useEffect(() => {
    const fakeApiCall = async () => {
      setJsonData(courseData);
    };

    fakeApiCall();
  }, []);

  //Filter Json for Courses with status=="Completed"
  const completedCourses = useMemo(
    () => jsonData?.filter((course) => course.status === "Completed") || [], 
    [jsonData]
  );
    
  //Filter Json for Courses with status=="Completed"
  const currentCourses = useMemo(
    () => jsonData?.filter((course) => course.status === "Current") || [],
    [jsonData]
  );
  
  //Update the courses to display
  const displayedCourses = useMemo(() => {
    // Set the displayed courses based on the selected filter type
    return filterType === 'Completed' ? completedCourses : currentCourses;
  }, [filterType, currentCourses, completedCourses]);

  //Handle when the user switches between viewing their current and completed courses
  const handleFilterChange = (newFilterType) => {
    setFilterType(newFilterType);
    console.log(displayedCourses);
  };

  return (
    <Content>
      <PageHeader>
        <PageHeaderLabel>Courses</PageHeaderLabel>
        {/* <FilterButton>
          <FilterIcon />
        </FilterButton> */}
      </PageHeader>
      <CourseControls>
        <ControlsButtonContainer>
          <ControlsFilterButton
            $active={filterType === "Current"}
            onClick={() => handleFilterChange("Current")}
          >
            <ButtonLabelText>Current</ButtonLabelText>
            <ButtonLabelCount>
              <body>{currentCourses ? currentCourses.length : 0}</body>
            </ButtonLabelCount>
          </ControlsFilterButton>
          <ControlsFilterButton
            $active={filterType === "Completed"}
            onClick={() => handleFilterChange("Completed")}
          >
            <ButtonLabelText>Completed</ButtonLabelText>
            <ButtonLabelCount>
              <body>{completedCourses ? completedCourses.length : 0}</body>
            </ButtonLabelCount>
          </ControlsFilterButton>
        </ControlsButtonContainer>
        <HorizontalSeparator />
      </CourseControls>
      <CoursesCardContainer>
        {displayedCourses.map((course) => (
          <CourseCard key={course.id} data={course}/>
        ))}
      </CoursesCardContainer>
    </Content>
  );
};

export default CourseContent;