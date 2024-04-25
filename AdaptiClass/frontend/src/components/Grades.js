import React from 'react';
import styled from 'styled-components';

const ComponentWrapper = styled.div`
  background-color: #fff; 
  border-radius: 10px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); 

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
`;

const ComponentTitle = styled.h5`
  color: #3f434a;
  font-family: 'Poppins';
  font-weight: bold;
  font-size: 24px;
  margin: 0;
  margin-left: 30px;
  margin-top: 30px;
  margin-bottom: 20px;
  align-self: flex-start;
`;

const GradeListContainerWrapper = styled.div`
  padding: 20px;
  padding-top: 0;

  display: flex;
  flex-direction:column;
  justify-content: center;
  align-items: center;
`;

const GradeListContainer = styled.div`
  width: 440px;
  height: 638px;
  padding-left: 20px;
  padding-right: 20px;
  overflow-y: auto; 

  // Custom scrollbar styles
  scrollbar-width: thin;
  scrollbar-color: #ccc #f0f0f0;
  &::-webkit-scrollbar {
    width: 8px;
  }
  &::-webkit-scrollbar-track {
    background: #f0f0f0;
  }
  &::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 4px;
  }
`;

const GradeItem = styled.button`
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  cursor: pointer;
  outline: inherit;

  width: 100%;

  background-color: #F9F9F9; 
  border-radius: 8px; 
  border: solid 1px #F9F9F9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); 
  padding: 12px 16px; 
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;


  &:hover {
    border: solid 1px #8A9099;
  }

  &:last-child {
    margin-bottom: 0; 
  }
`;

const GradeTitle = styled.div`
  display: flex;
  align-items: center;
  font-size: 14px; 
`;

const GradeIcon = styled.span`
  width: 24px; 
  height: 24px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  color: white;
  margin-right: 10px;
  background-color: ${(props) => (props.$color ? props.$color : '#FD7972')};
`;

const GradeInfo = styled.div`
  display: flex;
  flex-direction: column;
`;

const GradeScore = styled.span`
  font-size: 14px;
  font-weight: 500;
  font-family: 'Poppins'
  color: #333;
  margin-left: 4px;
`;

const Grade = ({ assignment, letterGrade, color, handleClick}) => (
  <GradeItem onClick={()=>handleClick(assignment)}>
    <GradeTitle>
      <GradeIcon $color={color}>{letterGrade}</GradeIcon>
      {assignment.title}
    </GradeTitle>
    <GradeScore>{assignment.grade}%</GradeScore>
  </GradeItem>
);

const Grades = ({ grades, handleSetAssignment }) => {

  const calcLetterGrade = (percentage) => {
    if (percentage >= 97) {
        return 'A+';
    } else if (percentage >= 93) {
        return 'A';
    } else if (percentage >= 90) {
        return 'A-';
    } else if (percentage >= 87) {
        return 'B+';
    } else if (percentage >= 83) {
        return 'B';
    } else if (percentage >= 80) {
        return 'B-';
    } else if (percentage >= 77) {
        return 'C+';
    } else if (percentage >= 73) {
        return 'C';
    } else if (percentage >= 70) {
        return 'C-';
    } else if (percentage >= 67) {
        return 'D+';
    } else if (percentage >= 63) {
        return 'D';
    } else if (percentage >= 60) {
        return 'D-';
    } else {
        return 'F';
    }
};
  const getColor = (grade) => {
    const firstLetter = grade.charAt(0);
    switch (firstLetter) {
      case 'A':
        return '#49C96D';
      case 'B':
        return '#009EB2';
      case 'C':
        return '#FFD240';
      case 'D':
        return '#FF965D';
      case 'F':
        return '#FD7972';
      default:
        return '#FD7972';
    }
  }

  return (
    <ComponentWrapper>
      <ComponentTitle>Grades</ComponentTitle>
      <GradeListContainerWrapper>
        <GradeListContainer>
        {grades.map((assignment, index) => (
          <Grade
          key={index}
          assignment={assignment}
          letterGrade={calcLetterGrade(assignment.grade)}
          color={getColor(calcLetterGrade(assignment.grade))}
          handleClick={handleSetAssignment}
        />
        ))}
    </GradeListContainer>

      </GradeListContainerWrapper>
    
    </ComponentWrapper>
  );
};

export default Grades;
