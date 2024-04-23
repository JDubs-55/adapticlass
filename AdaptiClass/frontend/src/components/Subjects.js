import styled from "styled-components";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import { useNavigate } from 'react-router-dom';

const GridContainer = styled.div`
  width: 100%;
  display: flex;
  gap: 20px;
  justify-content: flex-start;
`;

const ClickableSubjectContainer = styled.button`
  width: 16%;
  background: #fff;
  border-radius: 20px; 
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);

  display: flex;
  justify-content: space-between; 
  align-items: center;

  height: 120px;
  border: none; 
  cursor: pointer; 
  margin: 0; 
  outline: none; 
  text-align: left; 
  &:hover {
    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
  }
`;

const SubjectTitle = styled.h2`
  width: 40%;
  font-size: 18px;
  color: #3f434a;
  margin: 0;
  margin-left: 20px;

`;

const PercentageChange = styled.div`
  color: ${(props) => props.$isPositive ? '#4caf50' : '#f44336'};
  font-size: 14px;
  margin-top: 4px;
`;

const ProgressBarContainer = styled.div`
  width: 80px; 
  height: 80px; 
  margin-right: 20px;
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



const Subject = ({ course_id, name, percentage}) => {
    const progressBarColor = getProgressBarColor(percentage);
    const navigate = useNavigate();
  
    const handleClick = () => {

      navigate(`/student/courses/${course_id}`);
    };
  
    return (
      <ClickableSubjectContainer onClick={handleClick}>
        
        <SubjectTitle>{name}</SubjectTitle>        
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

  const getButtonSize = (subjects) => {
    return `calc(${200/subjects.length}% - ${(subjects.length-1)*20}px)`;
  };

  return (
    <GridContainer>
      {subjects && subjects.map((subject, index) => (
        <Subject
          key={subject.course_id}
          course_id={subject.course_id}
          name={subject.name}
          percentage={subject.percentage}
        />
      ))}
    </GridContainer>
  );
};

export default SubjectsPage;
