import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import Questions from "../components/Questions";
import ProgressBar from "../components/ProgressBar";
import ChatBox from "../components/Chatbox";

const MainLayout = styled.div`
  width: 100%;
  display: flex;
  align-items: flex-start;
  height: calc(100vh - 140px);
  overflow-y: hidden;
  background-color: #f8f8f8;
`;

const QuestionsContainer = styled.div`
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const ExerciseActivity = () => {

    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const totalQuestions = 3;
    const [quizCompleted, setQuizCompleted] = useState(false);

    return (
        <MainLayout>
          <QuestionsContainer>
            <Questions
              updateCurrentIndex={setCurrentQuestionIndex}
              totalQuestions={totalQuestions}
              setQuizCompleted={setQuizCompleted}
            />
            <ProgressBar
              current={currentQuestionIndex + 1}
              total={totalQuestions}
              quizCompleted={quizCompleted}
            />
          </QuestionsContainer>
          <ChatBox />
        </MainLayout>
    );
};

export default ExerciseActivity;


