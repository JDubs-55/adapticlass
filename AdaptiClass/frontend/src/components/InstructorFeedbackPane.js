import React from 'react';
import styled from 'styled-components';

const ComponentWrapper = styled.div`
  width: 100%;
  height: 40%;
  background-color: #fff; 
  border-radius: 10px; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); 

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const ComponentHeaderWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin: 0;
  margin-left: 30px;
  margin-top: 30px;
  margin-bottom: 20px;
  align-self: flex-start;
`;

const InstructorImage = styled.img`
  width: 64px;
  height: auto;
  border-radius: 20px;
`;

const ComponentTitleWrapper = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  margin-left: 10px;
`;

const ComponentTitle = styled.h5`
  color: #3f434a;
  font-family: 'Poppins';
  font-weight: bold;
  font-size: 24px;
  margin: 0;
  
  align-self: flex-start;
`;

const ComponentSubTitle = styled.p`
  color: #595F69;
  font-family: 'Poppins';
  font-weight: 400;
  font-size: 18px;
  margin: 0;
`;

const MainContentWrapper = styled.div`
  width: 100%;
  padding-top: 0;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;

`;

const MainContent = styled.div`
  margin-left: 30px;
`;

const FeedbackText = styled.p`
  color: #595F69;
  font-family: 'Poppins';
  font-weight: 400;
  font-size: 14px;
  margin: 0;
`



const InstructorFeedback = ({ feedback, instructor }) => {
  return (
    <ComponentWrapper>
      <ComponentHeaderWrapper>
        <InstructorImage src={instructor.picture}/>
        <ComponentTitleWrapper>
          <ComponentTitle>Instructor Feedback</ComponentTitle>
          <ComponentSubTitle>{instructor.display_name}</ComponentSubTitle>
        </ComponentTitleWrapper>
      </ComponentHeaderWrapper>
      <MainContentWrapper>
        <MainContent>
          <FeedbackText>This is some feedback for the student on this assignment</FeedbackText>
        </MainContent>
      </MainContentWrapper>
    </ComponentWrapper>
  );
};

export default InstructorFeedback;
