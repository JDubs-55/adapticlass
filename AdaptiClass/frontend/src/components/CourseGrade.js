import React from 'react';
import styled from 'styled-components';

const CircleWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 10px;
  padding: 10px;
  background-color: #fff;
  border-radius: 10px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  width: 180px; 
  height: 180px; 
  justify-content: center;
`;

const CircleBackground = styled.svg`
  transform: rotate(-90deg);
  border-radius: 50%;
`;

const TextContainer = styled.div`
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 160px;
  width: 160px;
`;

const GradeText = styled.div`
  font-size: 32px;
  color: #333;
`;

const PercentageText = styled.div`
  font-size: 20px;
  color: #333;
  margin-top: 4px;
`;

const CourseGrade = ({ grade, percentage }) => {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const offset = ((100 - percentage) / 100) * circumference;

  const getColor = () => {
    if (percentage >= 80) return '#4CAF50'; // Green
    else if (percentage >= 70) return '#FFEB3B'; // Yellow
    else return '#F44336'; // Red
  };

  return (
    <CircleWrapper>
      <CircleBackground width="160" height="160">
        <circle
          stroke="#e6e6e6"
          strokeWidth="14"
          fill="transparent"
          r={radius}
          cx="80"
          cy="80"
        />
        <circle
          stroke={getColor()}
          strokeWidth="14"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          fill="transparent"
          r={radius}
          cx="80"
          cy="80"
        />
      </CircleBackground>
      <TextContainer>
        <GradeText>{grade}</GradeText>
        <PercentageText>{percentage}%</PercentageText>
      </TextContainer>
    </CircleWrapper>
  );
};

export default CourseGrade;
