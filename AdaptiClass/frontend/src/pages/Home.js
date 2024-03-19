import React from 'react';
import styled from 'styled-components';
import SubjectsPage from '../components/Subjects';
import subjectsData from '../subjects.json';
import TimeChart from '../components/Time';
import timeData from '../time.json';
import Upcoming from '../components/Upcoming';
import toDoData from '../upcoming.json';
import Engagement from '../components/Engagement'; 
import engagementData from '../mockRequests/engagement.json';

const Content = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 20px;
`;

const RowContainer = styled.div`
  display: flex;
`;

const LeftColumn = styled.div`
  display: flex;
  flex-direction: column;
`;

const RightColumn = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: 20px; 
`;

const HomeContent = () => {
  return (
    <Content>
      <RowContainer>
        <LeftColumn>
          <SubjectsPage subjects={subjectsData} />
          <TimeChart time={timeData} />
        </LeftColumn>
        <RightColumn>
          <Upcoming tasks={toDoData} />
          <Engagement engagementData={engagementData} />
        </RightColumn>
      </RowContainer>
    </Content>
  );
};

export default HomeContent;
