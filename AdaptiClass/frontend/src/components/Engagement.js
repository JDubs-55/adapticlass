import React from 'react';
import styled from 'styled-components';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const ComponentWrapper = styled.div`
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;
  gap: 10px;

  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  max-height: 445px;

`;

const EngagementHeader = styled.h2`
  color: #3f434a;
  font-family: 'Poppins';
  font-weight: bold;
  font-size: 24px;
  margin: 0;
  margin-left: 20px;
  margin-top: 20px;

`;

const EngagementContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-evenly;
`;

const ProgressBarContainer = styled.div`
  width: 30%;
  padding: 30px;

`;

const EngagementInfo = styled.div`
  width: 40%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
  padding-left: 20px;
`;

const InfoText = styled.p`
  margin: 5px 0;
  font-size: 1.1em;
`;

const Engagement = ({ engaged_time, total_time }) => {
  
  const engagementPercentage = engaged_time && total_time ? Math.round((engaged_time / total_time) * 100) : 0;

  const getColor = (percentage) => {
    if (percentage >= 80) return '#49C96D';
    if (percentage >= 70) return '#FFD240';
    return '#FD7972';
  };

  return (
    <ComponentWrapper>
      <EngagementHeader>Engagement</EngagementHeader>
      <EngagementContainer>
        <ProgressBarContainer>
          {engaged_time && total_time && <CircularProgressbar
            value={engagementPercentage}
            text={`${engagementPercentage}%`}
            styles={buildStyles({
              pathColor: getColor(engagementPercentage),
              textColor: '#3F434A',
              trailColor: '#d6d6d6',
              backgroundColor: '#3e98c7',
              textSize: '16px',
              pathTransitionDuration: 0.5,
            })}
          />}
        </ProgressBarContainer>
        <EngagementInfo>
          {engaged_time && total_time && <InfoText><strong>Engaged:</strong> {`${Math.floor(engaged_time/60)}h ${engaged_time%60}min`} </InfoText>}
          {engaged_time && total_time && <InfoText><strong>Total:</strong> {`${Math.floor(total_time/60)}h ${total_time%60}min`} </InfoText>}
        </EngagementInfo>
      </EngagementContainer>
    </ComponentWrapper>
  );
};

export default Engagement;
