import React, { useState, useEffect } from "react";
import styled, { css } from "styled-components";

const Wrapper = styled.div`
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  width: calc(100%-80px);
  padding: 20px;
  margin: 20px;
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
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
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
  justify-content: center;
  align-items: center;
`;

const Input = styled.input`
  border: 2px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-top: 1em;
  box-sizing: border-box;
  width: 50%;
`;

const SubmitButton = styled.button`
  background-color: #304ffd;
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
  ${(props) =>
    props.$isCorrect === null &&
    css`
      background-color: #ccc;
    `}
  ${(props) =>
    props.$isCorrect === true &&
    css`
      background-color: green;
      &:after {
        content: "✔";
      }
    `}
  ${(props) =>
    props.$isCorrect === false &&
    css`
      background-color: red;
      &:after {
        content: "✖";
      }
    `}
`;

const NextButton = styled(SubmitButton)`
  width: 25%;
  background-color: #304ffd;
  &:hover {
    background-color: #304ffd;
  }
  margin-top: 10px;
`;

const CompletedButton = styled(SubmitButton)`
  background-color: #008000; // A green color to indicate completion
  &:hover {
    background-color: #006400; // Darker green on hover
  }
`;

const Questions = ({ updateCurrentIndex, setQuizCompleted, questions, updateQuestionData}) => {
  const [currentProblemIndex, setCurrentProblemIndex] = useState(0);
  const [currentProblem, setCurrentProblem] = useState(
    questions[currentProblemIndex]
  );
  const [userAnswer, setUserAnswer] = useState(questions[currentProblemIndex]["user_answer"]);
  const [isCorrect, setIsCorrect] = useState(null);

  useEffect(() => {
    setCurrentProblem(questions[currentProblemIndex]);
    updateCurrentIndex(currentProblemIndex);
  }, [currentProblemIndex, updateCurrentIndex]);
  
  const handleNextProblem = () => {

    // Update the user's answer for the current question
    const updatedQuestion = { ...questions[currentProblemIndex] };
    updatedQuestion.user_answer = userAnswer;
    
    // Check if the answer is correct
    const answerIsCorrect = userAnswer === currentProblem.answer;
    setIsCorrect(answerIsCorrect);
    updatedQuestion.is_correct = answerIsCorrect;
    updatedQuestion.is_answered = true;

    updateQuestionData(currentProblemIndex, updatedQuestion);

    const nextIndex = currentProblemIndex + 1;

    if (nextIndex < questions.length) {
      setCurrentProblemIndex(nextIndex);
      setUserAnswer(questions[nextIndex]["user_answer"]);
    } else {
      console.log("Completed all problems.");
      setQuizCompleted(true);
    }
  };

  return (
    <Wrapper>
      <ProblemNumber>Problem {currentProblemIndex + 1}</ProblemNumber>
      <ProblemContainer>
        <ProblemText>{currentProblem?.question}</ProblemText>
      </ProblemContainer>
      <FormWrapper>
          <ButtonWrapper>
            {questions[currentProblemIndex]["is_answered"] ? (
              <Input
                disabled
                type="text"
                value={userAnswer}
              />
            ) : (
              <Input
                type="text"
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Type something"
              />
            )}
            {currentProblemIndex < questions.length - 1 ? (
              <NextButton onClick={handleNextProblem}>Next</NextButton>
            ) : (<NextButton onClick={handleNextProblem}>Submit</NextButton>)}
          </ButtonWrapper>
      </FormWrapper>
      <StatusIndicator $isCorrect={isCorrect} />
    </Wrapper>
  );
};

export default Questions;
