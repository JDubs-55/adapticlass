import React from 'react';
import styled from 'styled-components';

const FeedbackWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  width: 400px; 
  height: 180px;
`;

const FeedbackHeader = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-between;
  font-size: 18px;
  margin-bottom: 10px;
`;

const PerformanceRating = styled.div`
  text-align: right;
`;

const FeedbackText = styled.div`
  font-size: 16px;
  color: #333;
  padding: 10px;
  text-align: center;
`;


const InstructorFeedback = ({ feedback }) => {
  return (
    <FeedbackWrapper>
      <FeedbackHeader>
        <div>{feedback.instructorName}</div>
        
        <PerformanceRating>Score: {feedback.score}/10</PerformanceRating>
      </FeedbackHeader>
      <FeedbackText>{feedback.feedback}</FeedbackText>
    </FeedbackWrapper>
  );
};

export default InstructorFeedback;
