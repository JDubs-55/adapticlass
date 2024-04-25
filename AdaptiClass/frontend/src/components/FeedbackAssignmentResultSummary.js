import React from 'react';
import styled from 'styled-components';
import {useNavigate} from 'react-router-dom';

const ComponentWrapper = styled.div`
  width: 100%;
  height: 60%;
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
  font-family: 'Poppins';
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
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 70px;
`;

const AssignmentRow = styled.div`
  width: calc(100% - 60px);
  height: 200px;
  margin-left: 30px;
  margin-right: 30px;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
`;

const AssignmentRowItem = styled.div`
  display:flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const RowItemMainLabel = styled.h6`
  color: #3f434a;
  font-family: 'Poppins';
  font-weight: 500;
  font-size: 36px;
  margin: 0;
  margin: 10px 20px;
`;

const RowItemSubLabel = styled.p`
  color: #8A9099;
  font-family: 'Poppins';
  font-weight: 400;
  font-size: 24px;
  margin: 0;
  margin: 10px 20px;
`;

const VerticalSeparator = styled.div`
  width: 2px;
  height: 100%; /* Adjust the height as needed */
  background-color: #E8E9EB; /* Adjust the color as needed */
`;


const SeeAssignmentButton = styled.button`
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  cursor: pointer;
  outline: inherit;

  width: calc(100% - 60px);
  background-color: rgba(48, 79, 253, 0.2);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const SeeAssignmentButtonLabel = styled.p`
  font-family: 'Poppins';
  font-weight: 500;
  font-size: 20px;
  color: #304FFD;
  margin: 0;
  margin-top: 10px;
  margin-bottom: 10px;
`;



const PieChartContainer = styled.svg`
  width: 200px;
  height: 200px;
`;

const Slice = styled.circle`
  fill: transparent;
  stroke-width: 40;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  transition: stroke-dashoffset 0.3s;
`;

const PieChart = ({ correct, incorrect }) => {
  const total = correct + incorrect;
  const percentage1 = total === 0 ? 0 : (correct / total) * 100;
  const percentage2 = total === 0 ? 100 :(incorrect / total) * 100;

  const radius = 80;
  const circumference = 2 * Math.PI * radius;
  const offset2 = percentage1 === 100 ? 0 : circumference - (percentage2 / 100) * circumference;
  const dashLength1 = (percentage1 / 100) * circumference;
  const dashLength2 = (percentage2 / 100) * circumference;

  return (
    <PieChartContainer>
      

      <Slice
        cx="100"
        cy="100"
        r={radius}
        stroke="#304FFD"
        strokeWidth={40}
        strokeDasharray={`${dashLength1} ${circumference - dashLength1}`}
      />
      <Slice
        cx="100"
        cy="100"
        r={radius}
        stroke="#FF965D"
        strokeWidth={40}
        strokeDasharray={`${dashLength2} ${circumference - dashLength2}`}
        strokeDashoffset={-offset2}
      />
    </PieChartContainer>
  );
};


const AssignmentResults = ({ assessment }) => {
  const navigate = useNavigate();

  const handleSeeSubmissionClick = () => {
    navigate(`/student/courses/${assessment.course_id}/assignment/${assessment.assignment_id}`);
  }

  return (
    <ComponentWrapper>
      <ComponentTitle>Assignment Results</ComponentTitle>
      <MainContentWrapper>
        <MainContent>
          <AssignmentRow>
            <AssignmentRowItem>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="0.174561" width="16" height="16" rx="2" fill="#304FFD"/>
              </svg>
              <RowItemMainLabel>{assessment.num_correct} questions</RowItemMainLabel>
              <RowItemSubLabel>Correct</RowItemSubLabel>
            </AssignmentRowItem>
            <VerticalSeparator/>
            <AssignmentRowItem>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="0.174561" width="16" height="16" rx="2" fill="#FF965D"/>
              </svg>
              <RowItemMainLabel>{assessment.num_questions-assessment.num_correct} questions</RowItemMainLabel>
              <RowItemSubLabel>Incorrect</RowItemSubLabel>
            </AssignmentRowItem>
            <PieChart correct={assessment.num_correct} incorrect={assessment.num_questions-assessment.num_correct}/>
          </AssignmentRow>
          <SeeAssignmentButton onClick={handleSeeSubmissionClick}>
            <SeeAssignmentButtonLabel>See Submission</SeeAssignmentButtonLabel>
          </SeeAssignmentButton>
        </MainContent>
      </MainContentWrapper>
    </ComponentWrapper>
  );
};

export default AssignmentResults;
