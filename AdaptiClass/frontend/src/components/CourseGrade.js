import React from "react";
import styled from "styled-components";

const ComponentWrapper = styled.div`
  width: 40%;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const ComponentTitle = styled.h5`
  color: #3f434a;
  font-family: "Poppins";
  font-weight: bold;
  font-size: 24px;
  margin: 0;
  margin-left: 30px;
  margin-top: 30px;
  margin-bottom: 20px;
  align-self: flex-start;
`;

const MainContentWrapper = styled.div`
  width: 100%;
  padding-top: 0;

  display: flex;
  justify-content: center;
  align-items: center;
`;

const MainContent = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const CircleWrapper = styled.div`
  position: relative;
  width: 400px; /* Adjust the size of the circle wrapper */
  height: 400px; /* Adjust the size of the circle wrapper */
`;

const CircleBackground = styled.svg`
  transform: rotate(-90deg);
`;

const TextContainer = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
`;

const PercentageText = styled.p`
  color: #3F434A;
  font-family: "Poppins";
  font-weight: 500;
  font-size: 32px;
  margin:0;
`;

const GradeText = styled.p`
  color: #8A9099;
  font-family: "Poppins";
  font-weight: 500;
  font-size: 28px;
  margin:0;
`;

const CourseGrade = ({ grade, percentage }) => {
  const radius = 175;
  const circumference = 2 * Math.PI * radius;
  const offset = ((100 - percentage) / 100) * circumference;

  const getColor = () => {
    if (percentage >= 80) return "#49C96D"; // Green
    else if (percentage >= 70) return "#FFD240"; // Yellow
    else return "#FD7972"; // Red
  };

  return (
    <ComponentWrapper>
      <ComponentTitle>Course Grade</ComponentTitle>
      <MainContentWrapper>
        <MainContent>
          <CircleWrapper>
          <CircleBackground
              viewBox="0 0 400 400" // Set viewBox to scale the SVG
              width="400"
              height="400"
            >
              <circle
                stroke="#e6e6e6"
                strokeWidth="20"
                fill="transparent"
                r={radius}
                cx="200"
                cy="200"
              />
              <circle
                stroke={getColor()}
                strokeWidth="20"
                strokeDasharray={circumference}
                strokeDashoffset={offset}
                strokeLinecap="round"
                fill="transparent"
                r={radius}
                cx="200"
                cy="200"
              />
            </CircleBackground>
            <TextContainer>
              <PercentageText>{percentage}%</PercentageText>
              <GradeText>{grade}</GradeText>
              
            </TextContainer>
          </CircleWrapper>
        </MainContent>
      </MainContentWrapper>
    </ComponentWrapper>
  );
};

export default CourseGrade;
