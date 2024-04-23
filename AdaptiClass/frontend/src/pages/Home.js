import React, {useState, useEffect} from 'react';
import styled from 'styled-components';
import SubjectsPage from '../components/Subjects';
import subjectsData from '../mockRequests/subjects.json'
import TimeChart from '../components/Time';
import timeData from '../mockRequests/time.json';
import Upcoming from '../components/Upcoming';
import toDoData from '../mockRequests/upcoming.json';
import Engagement from '../components/Engagement'; 
import engagementData from '../mockRequests/engagement.json';
import axios from "axios";

const Content = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 20px;
  gap: 20px;
  max-height: calc(100vh-66px);
`;

const SubjectHeader = styled.div`
  width: 100%;
  display: flex;
  align-items: start;
  justify-content: center;
`;

const DataContent = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
`;

const UpcomingWrapper = styled.div`
  width: 50%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
`;
const RightColumn = styled.div`
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
`;

const HomeContent = () => {

  const [homeData, setHomeData] = useState({});

  const fetchHomeData = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/homepagedata/`, { params: { user_id: sessionStorage.getItem("user_id") } });
      setHomeData(response.data);
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(()=>{

    fetchHomeData();

  },[]);




  return (
    <Content>
      <SubjectHeader>
        {homeData && <SubjectsPage subjects={homeData['enrollments']} />}
      </SubjectHeader>
      <DataContent>
        <UpcomingWrapper>
          {homeData && <Upcoming tasks={homeData['upcoming']} />}
        </UpcomingWrapper>
        <RightColumn>
          {homeData && <TimeChart time={homeData['time_data']} total_time={homeData['total_time']} total_time_prev_week={homeData['total_time_prev_week']}/>}
          {homeData &&  <Engagement engaged_time={homeData['engaged_time']} total_time={homeData['total_time']}/>}
        </RightColumn>
      
      </DataContent>
    </Content>
  );
};

export default HomeContent;
