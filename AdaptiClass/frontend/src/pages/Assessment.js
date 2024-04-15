import React, { useState, useEffect } from "react";
import styled from "styled-components";
import Questions from "../components/Questions";
import ProgressBar from "../components/ProgressBar";
import ChatBox from "../components/Chatbox";
import axios from "axios";

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

const AssessmentActivity = ({questions}) => {

    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [quizCompleted, setQuizCompleted] = useState(false);

    return (
        <MainLayout>
          <QuestionsContainer>
            {questions.length !== 0 && <Questions
              updateCurrentIndex={setCurrentQuestionIndex}
              setQuizCompleted={setQuizCompleted}
              questions={questions}
            /> }
            {questions.length !== 0 && <ProgressBar
              current={currentQuestionIndex + 1}
              total={questions.length}
              quizCompleted={quizCompleted}
            />}
          </QuestionsContainer>
          <ChatBox />
        </MainLayout>
    );
};

export default AssessmentActivity;


