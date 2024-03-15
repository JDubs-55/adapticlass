import React from "react";
import styled from "styled-components";
import CourseCardProgressBar from "./CourseCardProgressBar";
import { Link } from "react-router-dom";
import PathConstants from "../routes/pathConstants";

const CourseCardWrapper = styled.div`
  width: 302px;
  height: 222px;
  background-color: #fff;
  border-radius: 14px;
  padding: 24px;

  display: flex;
  flex-direction: column;
  gap: 23px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a subtle shadow for depth */
`;

const CourseInformationContainer = styled.div`
  width: 100%;

  display: flex;
  align-items: center;
  justify-content: flex-start;
`;

const CourseImageContainer = styled.div`
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;

  img {
    width: 36px;
    height: 36px;
  }
`;

const CourseInformationLabelContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: start;
  margin-left: 10px;

`;

const CourseName = styled.body`
  font-size: 18px;
  font-weight: 600;
  color: #3f434a;
`;

const CourseInstructor = styled.body`
  font-size: 14px;
  color: #595f69;
`;

const CourseDescription = styled.body`
  color: #595F69;
  font-size: 14px;
  font-weight: 400;
`;

const CourseCard = ({data}) => {
  return (
    <Link to={`${data.id}`}>
    <CourseCardWrapper>
      <CourseInformationContainer>
        <CourseImageContainer>
            <img src={data.course_image} alt="Profile" />
        </CourseImageContainer>
        <CourseInformationLabelContainer>
          <CourseName>{data.name}</CourseName>
          <CourseInstructor>{data.instructor}</CourseInstructor>
        </CourseInformationLabelContainer>
      </CourseInformationContainer>
      <CourseDescription>{data.description}</CourseDescription>
      <CourseCardProgressBar label="Average Grade" percentage={data.grade}></CourseCardProgressBar>
    </CourseCardWrapper>
    </Link>
  );
};

export default CourseCard;
