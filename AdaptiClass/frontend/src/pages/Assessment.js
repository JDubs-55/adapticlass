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

const AssessmentActivity = ({activity_id}) => {

    const [questionData, setQuestionData] = useState([]);

    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [quizCompleted, setQuizCompleted] = useState(false);

    const fetchAssessmentContent = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/questions/${activity_id}/`);
            setQuestionData(response.data);
            console.log(questionData);
        } catch (error) {
            console.log(error);
        }
    };

    useEffect(()=> {
        fetchAssessmentContent();
    },[]);

    return (
        <MainLayout>
          <QuestionsContainer>
            {questionData.length !== 0 && <Questions
              updateCurrentIndex={setCurrentQuestionIndex}
              setQuizCompleted={setQuizCompleted}
              questions={questionData}
            /> }
            {questionData.length !== 0 && <ProgressBar
              current={currentQuestionIndex + 1}
              total={questionData.length}
              quizCompleted={quizCompleted}
            />}
          </QuestionsContainer>
          <ChatBox />
        </MainLayout>
    );
};

export default AssessmentActivity;


