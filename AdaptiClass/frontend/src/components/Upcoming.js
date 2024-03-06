import React from 'react';
import styled from 'styled-components';
import { FaCheckCircle, FaRegCircle } from 'react-icons/fa'; 

const UpcomingContainer = styled.div`
  width: 634px; 
  height: 360px; 
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  padding: 20px;
  margin-left: 20px; 
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`;

const Task = styled.div`
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
`;

const Bubble = styled.span`
  margin-right: 0.5rem;
`;

const DueDate = styled.span`
  color: #666;
`;

const parseDate = (dateString) => {
    const [month, day, year] = dateString.split('-').map(num => parseInt(num, 10));
    return new Date(year, month - 1, day); 
  };
  
  const Upcoming = ({ tasks }) => {
    const sortedTasks = tasks
      .sort((a, b) => parseDate(a.dueDate) - parseDate(b.dueDate))
      .slice(0, 4); 
  
    return (
      <UpcomingContainer>
        <h2>Upcoming Assignments</h2>
        {sortedTasks.map((task, index) => (
          <Task key={index} onClick={() => console.log("Clicked on task: ", task.name)}>
            <TaskName>
              <Bubble>
                {task.completed ? <FaCheckCircle color="green" /> : <FaRegCircle color="grey" />}
              </Bubble>
              {task.name}
            </TaskName>
            <DueDate>{task.dueDate}</DueDate>
          </Task>
        ))}
        {Array.from({ length: 5 - tasks.length }, (_, i) => (
          <Task key={`placeholder-${i}`} style={{ visibility: 'hidden' }}>
            <TaskName>
              <Bubble>
                <FaRegCircle color="grey" />
              </Bubble>
              Placeholder
            </TaskName>
            <DueDate>Placeholder</DueDate>
          </Task>
        ))}
      </UpcomingContainer>
    );
  };
  
  export default Upcoming;