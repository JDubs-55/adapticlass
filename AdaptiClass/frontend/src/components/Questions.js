import React, { useState, useEffect } from 'react';
import styled, { css } from 'styled-components';
import assignments from '../mockRequests/assignments.json';

const Wrapper = styled.div`
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
  margin: 20px;
  width: 100%;
  max-width: 800px; // Original size
  padding: 20px; // Padding moved from Content to Wrapper
  position: relative; 
`;

const ProblemNumber = styled.h2`
  font-size: 1em;
  font-weight: normal;
  color: #333;
  margin-bottom: 0.5em;
`;

const ProblemContainer = styled.div`
  background-color: #fff;
  border-radius: 8px;
  padding: 1em;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
  margin-bottom: 1em;
`;

const ProblemText = styled.p`
  color: #666;
  font-size: 0.9em;
`;

const FormWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ButtonWrapper = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%; // Ensure this wrapper fills its parent so buttons can use max-width effectively
`;

const Input = styled.input`
  border: 2px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-top: 1em;
  box-sizing: border-box;
  width: 100%;
`;

const SubmitButton = styled.button`
  background-color: #304FFD;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 0.9em;
  width: 100%;
  margin-top: 0.5em;
  &:hover {
    background-color: #3949ab;
  }
`;

const StatusIndicator = styled.div`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  right: 20px;
  top: 20px;
  ${props => props.isCorrect === null && css`
    background-color: #ccc;
  `}
  ${props => props.isCorrect === true && css`
    background-color: green;
    &:after {
      content: '✔';
    }
  `}
  ${props => props.isCorrect === false && css`
    background-color: red;
    &:after {
      content: '✖';
    }
  `}
`;

const NextButton = styled(SubmitButton)`
  background-color: #4CAF50; 
  &:hover {
    background-color: #45a049;
  }
  margin-top: 10px; 
`;

const CompletedButton = styled(SubmitButton)`
  background-color: #008000; // A green color to indicate completion
  &:hover {
    background-color: #006400; // Darker green on hover
  }
`;

const Questions = ({ updateCurrentIndex, totalQuestions, setQuizCompleted }) => {
  const [currentProblemIndex, setCurrentProblemIndex] = useState(0);
  const [currentProblem, setCurrentProblem] = useState(assignments[currentProblemIndex]);
  const [userAnswer, setUserAnswer] = useState('');
  const [isCorrect, setIsCorrect] = useState(null);

  useEffect(() => {
    setCurrentProblem(assignments[currentProblemIndex]);
    updateCurrentIndex(currentProblemIndex); 
  }, [currentProblemIndex, updateCurrentIndex]);

  const handleSubmit = (event) => {
    event.preventDefault();
    const answerIsCorrect = userAnswer === currentProblem.answer;
    setIsCorrect(answerIsCorrect);
  
    if (answerIsCorrect) {
      if (currentProblemIndex === assignments.length - 1) {
        setQuizCompleted(true);
      }
    }
  };

  const handleNextProblem = () => {
    const nextIndex = currentProblemIndex + 1;
    if (nextIndex < assignments.length) {
      setCurrentProblemIndex(nextIndex);
      setIsCorrect(null);
      setUserAnswer('');
    } else {
        // Edit Completed button function
      console.log("Completed all problems.");
      setQuizCompleted(true); 
    }
  };
  
  


    return (
    <Wrapper>
      <ProblemNumber>Problem {currentProblem?.id}</ProblemNumber>
      <ProblemContainer>
        <ProblemText>{currentProblem?.problem}</ProblemText>
      </ProblemContainer>
      <FormWrapper>
        <form onSubmit={handleSubmit}>
          <ButtonWrapper>
            <Input
              type="text"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="Type something"
            />
            <SubmitButton type="submit">Submit</SubmitButton>
            {isCorrect && currentProblemIndex < assignments.length - 1 && (
              <NextButton onClick={handleNextProblem}>Next</NextButton>
            )}
            {isCorrect && currentProblemIndex === assignments.length - 1 && (
              <CompletedButton onClick={() => console.log("Quiz Completed!")}>Completed</CompletedButton>
            )}
          </ButtonWrapper>
        </form>
      </FormWrapper>
      <StatusIndicator isCorrect={isCorrect} />
    </Wrapper>
  );
};

export default Questions;