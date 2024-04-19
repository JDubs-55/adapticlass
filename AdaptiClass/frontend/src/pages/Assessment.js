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

const AssessmentActivity = ({questions, currentActivity, updateQuestionData}) => {

    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [quizCompleted, setQuizCompleted] = useState(false);

    const saveAssessment = async () => {
        try {

            const response = await axios.put(`http://127.0.0.1:8000/userquestions/${currentActivity['id']}/`, questions, { params: { user_id: sessionStorage.getItem("user_id") } });
            console.log(response);
          } catch (error) {
            console.log(error);
        }
    };

    const setActivityComplete = async (grade) => {
        try {
            const response = await axios.put('http://127.0.0.1:8000/activitycompleted/', null, { params: { user_id: sessionStorage.getItem("user_id"), activity_id: currentActivity['id'], grade: grade }});
            console.log(response);
        } catch (error) {
            console.log(error);
        }
    };

    //If the component is unloaded, save the state of all the questions. 
    useEffect(()=>{

        return () => {
            if (!quizCompleted){
                saveAssessment();
            }
            
        };
    },[]);

    //If the quiz was submitted, make each answer immutable and save
    useEffect(()=>{
        if (quizCompleted) {
            
            var correctCount = 0;
            
            for (let i=0; i<questions.length; i++){
                if (questions[i]['is_correct']){
                    correctCount++;
                }
            }
            const grade = 100* (correctCount/questions.length);

            saveAssessment();
            setActivityComplete(grade);
        }
    },[quizCompleted]);

    return (
        <MainLayout>
          <QuestionsContainer>
            {questions.length !== 0 && <Questions
              updateCurrentIndex={setCurrentQuestionIndex}
              setQuizCompleted={setQuizCompleted}
              questions={questions}
              updateQuestionData={updateQuestionData}
              
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


