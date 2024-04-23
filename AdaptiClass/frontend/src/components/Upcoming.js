import React from 'react';
import styled from 'styled-components';
import { FaCheckCircle, FaRegCircle } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';



const UpcomingContainer = styled.div`
  width: 100%; 
  height: 100%; 
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  
  display: flex;
  justify-content: flex-start;
  align-content: center;
  
`;

const ContentWrapper = styled.div`
  width: 90%;
  padding: 20px;
  padding-top: 10px;
  display: flex;
  flex-direction: column;
`

const Task = styled.div`
  width: 100%;
  background: #f9f9f9; 
  border: 1px solid #e0e0e0; 
  border-radius: 15px; 
  padding: 15px; 
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 1.25rem;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); 

  &:not(:last-child) {
    margin-bottom: 10px;
  }
`;

const TaskName = styled.span`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const TaskLabel = styled.p`
  font-family: 'Poppins';
  font-size: 20px;
  color: #3f434a;
  margin: 0;
  margin-left: 5px;
`

const TaskCourseLabel = styled.p`
  font-family: 'Poppins';
  font-size: 16px;
  font-weight: 500;
  color: #8a9099;
  margin: 0;
  margin-left: 5px;
`

const Bubble = styled.span`
  margin-right: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const DueDate = styled.span`
  color: #666;
`;

const parseDate = (dateString) => {
    const [month, day, year] = dateString.split('-').map(num => parseInt(num, 10));
    return new Date(year, month - 1, day); 
  };
  
  const Upcoming = ({ tasks }) => {
    const navigate = useNavigate();

    const handleClick = (course_id, assignment_id) => {
      navigate(`/student/courses/${course_id}/assignment/${assignment_id}`);
    }
  
    return (
      <UpcomingContainer>
        <ContentWrapper>
        <h2 style={{fontFamily: 'Poppins', color: '#3f434a'}}>Assignments</h2>
        {tasks && tasks.map((task, index) => (
          <Task key={index} onClick={() => handleClick(task.course_id, task.assignment_id)}>
            <TaskName>
              <Bubble>
                {task.is_complete ? <FaCheckCircle color="green" /> : <FaRegCircle color="grey" />}
              </Bubble>
              <TaskLabel>{task.name}</TaskLabel>
              <TaskCourseLabel>{task.course}</TaskCourseLabel>
            </TaskName>
            <DueDate>{task.due_date}</DueDate>
          </Task>
        ))}
        {/* {tasks && Array.from({ length: 5 - tasks.length }, (_, i) => (
          <Task key={`placeholder-${i}`} style={{ visibility: 'hidden' }}>
            <TaskName>
              <Bubble>
                <FaRegCircle color="grey" />
              </Bubble>
              Placeholder
            </TaskName>
            <DueDate>Placeholder</DueDate>
          </Task>
        ))} */}
        </ContentWrapper>
      </UpcomingContainer>
    );
  };
  
  export default Upcoming;