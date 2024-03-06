import React from 'react';
import styled from 'styled-components';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const EngagementContainer = styled.div`
  width: 634px;
  height: 298px;
  margin-left: 20px;
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  padding: 20px;
`;

const ProgressBarContainer = styled.div`
  width: 45%;
  padding-right: 20px;
  padding-top: 10px;
`;

const EngagementInfo = styled.div`
  width: 45%;
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

const Engagement = ({ engagementData }) => {
  const { disengaged, engaged } = engagementData;
  const total = disengaged + engaged;
  const engagementPercentage = total > 0 ? Math.round((engaged / total) * 100) : 0;

  const getColor = (percentage) => {
    if (percentage >= 80) return '#4caf50';
    if (percentage >= 70) return '#ffeb3b';
    return '#f44336';
  };

  return (
    <EngagementContainer>
      <ProgressBarContainer>
        <CircularProgressbar
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
        />
      </ProgressBarContainer>
      <EngagementInfo>
        <InfoText><strong>Engaged:</strong> {engaged} times</InfoText>
        <InfoText><strong>Disengaged:</strong> {disengaged} times</InfoText>
      </EngagementInfo>
    </EngagementContainer>
  );
};

export default Engagement;
