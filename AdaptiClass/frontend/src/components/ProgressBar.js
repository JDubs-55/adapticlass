import React from 'react';
import styled from 'styled-components';

const ProgressBarContainer = styled.div`
  width: calc(100%-40px);
  background-color: #e0e0e0;
  border-radius: 20px;
  margin-left: 20px;
  margin-right: 20px;
`;

const Filler = styled.div`
  height: 20px;
  width: ${({ percentage }) => `${percentage}%`};
  background-color: #304FFD;
  border-radius: inherit;
  transition: width 0.5s ease-in-out;
`;

const ProgressBar = ({ current, total, quizCompleted }) => {
    let percentage;
    if (quizCompleted) {
      percentage = 100; 
    } else {
      percentage = ((current - 1) / total) * 100;
    }
  
    return (
      <ProgressBarContainer>
        <Filler percentage={percentage} />
      </ProgressBarContainer>
    );
  };
  
  
  

export default ProgressBar;
