import React from 'react';
import styled from 'styled-components';

const GradesContainer = styled.div`
  width: 300px;
  height: calc(6 * 60px); 
  padding: 20px;
  background-color: #fff; 
  border-radius: 10px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); 
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

const GradeItem = styled.div`
  background-color: #F9F9F9; 
  border-radius: 8px; 
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); 
  padding: 12px 16px; 
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px; 
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
  
  background-color: ${({ grade }) => {
    if (grade.startsWith('A')) return '#4CAF50';
    if (grade.startsWith('B')) return '#FFEB3B';
    if (grade.startsWith('C')) return '#FF9800';
    if (grade.startsWith('D')) return '#FF5722';
    if (grade.startsWith('F')) return '#F44336';
    return '#BDBDBD';
  }};
`;

const GradeInfo = styled.div`
  display: flex;
  flex-direction: column;
`;

const GradeScore = styled.span`
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-left: 4px;
`;

const Grade = ({ title, score, grade }) => (
  <GradeItem>
    <GradeTitle>
      <GradeIcon grade={grade}>{grade}</GradeIcon>
      {title}
    </GradeTitle>
    <GradeScore>{score}</GradeScore>
  </GradeItem>
);

const Grades = ({ grades }) => {
  return (
    <GradesContainer>
      <h2>Grades</h2>
      {grades.map((grade, index) => (
        <Grade
          key={index}
          title={grade.title}
          score={grade.score}
          grade={grade.grade}
        />
      ))}
    </GradesContainer>
  );
};

export default Grades;
