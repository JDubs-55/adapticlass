import styled from "styled-components";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
 
const GridContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 317px);
  gap: 20px;
  justify-content: flex-start;
`;

const ClickableSubjectContainer = styled.button`
  background: #fff;
  border-radius: 20px; 
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between; 
  align-items: center;
  padding: 10px 20px; 
  height: 120px;
  width: 317px;
  border: none; 
  cursor: pointer; 
  width: 100%; 
  margin: 0; 
  outline: none; 
  text-align: left; 
  &:hover {
    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
  }
`;


const SubjectInfo = styled.div`
  text-align: left;
`;

const SubjectTitle = styled.h2`
  font-size: 18px;
  color: #333;
  margin: 0;
`;

const PercentageChange = styled.div`
  color: ${props => props.isPositive ? '#4caf50' : '#f44336'};
  font-size: 14px;
  margin-top: 4px;
`;

const ProgressBarContainer = styled.div`
  width: 80px; 
  height: 80px; 
`;


const getProgressBarColor = (percentage) => {
  if (percentage > 79) {
    return '#4caf50'; 
  } else if (percentage > 69) {
    return '#ffeb3b';
  } else {
    return '#f44336'; 
  }
};



const Subject = ({ name, percentage, change }) => {
    const progressBarColor = getProgressBarColor(percentage);
  
  
    const handleClick = () => {
      // For now just log to the console
      console.log(`Clicked on ${name}`);
    };
  
    return (
      <ClickableSubjectContainer onClick={handleClick}>
        <SubjectInfo>
          <SubjectTitle>{name}</SubjectTitle>
          <PercentageChange isPositive={change >= 0}>
            {change > 0 ? `↑ ${change}%` : (change < 0 ? `↓ ${Math.abs(change)}%` : '')}
          </PercentageChange>
        </SubjectInfo>
        <ProgressBarContainer>
          <CircularProgressbar
            value={percentage}
            text={`${percentage}%`}
            styles={buildStyles({
              pathColor: progressBarColor,
              textColor: progressBarColor,
              trailColor: '#d6d6d6',
            })}
          />
        </ProgressBarContainer>
      </ClickableSubjectContainer>
    );
};



const SubjectsPage = ({ subjects }) => {
  return (
    <GridContainer>
      {subjects.map((subject, index) => (
        <Subject
          key={index}
          name={subject.name}
          percentage={subject.percentage}
          change={subject.change}
        />
      ))}
    </GridContainer>
  );
};

export default SubjectsPage;
