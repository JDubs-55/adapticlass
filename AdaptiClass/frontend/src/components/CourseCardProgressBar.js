import React from 'react';
import styled from 'styled-components';

const ProgressBarWrapper = styled.div`
    width: 100%;
`;

const ProgressBarContainer = styled.div`
  width: 100%;
  border-radius: 5px;
  background-color: red;
  position: relative;
`;

const ProgressBackground = styled.div`
  height: 6px;
  border-radius: 5px;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #E8E9EB;
`

const ProgressFill = styled.div`
  height: 6px;
  border-radius: 5px;
  position: absolute;
  top: 0;
  left: 0;
  width: ${(props) => props.$width || '0%'};
  background-color: ${(props) => props.$color || '#49C96D'};
`;

const TextContainer = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
`;

const Text = styled.body`
    font-size: 14px;
    font-weight: 400;
    color: #595F69;
`

const CourseCardProgressBar = ({ label, percentage }) => {
  let color;

  if (percentage >= 85) {
    color = '#49C96D';
  } else if (percentage >= 75) {
    color = '#FFD240';
  } else if (percentage >= 65) {
    color = '#FF965D';
  } else {
    color = '#FD7972';
  }

  return (
    <ProgressBarWrapper>
      <TextContainer>
        <Text>{label}</Text>
        <Text>{`${percentage}%`}</Text>
      </TextContainer>
      <ProgressBarContainer>
        <ProgressBackground/>
        <ProgressFill $width={`${percentage}%`} $color={color} />
      </ProgressBarContainer>
    </ProgressBarWrapper>
  );
};

export default CourseCardProgressBar;
