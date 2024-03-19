import React, { useState } from 'react';
import styled from 'styled-components';
import Questions from '../components/Questions';
import ProgressBar from '../components/ProgressBar';
import ChatBox from '../components/Chatbox';
import assignments from '../assignments.json'; 

const MainLayout = styled.div`
  display: flex;
  align-items: flex-start;
  margin: 20px;
  gap: 20px;
`;

const AssignmentsDetail = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const totalQuestions = assignments.length;
  const [quizCompleted, setQuizCompleted] = useState(false);


  return (
    <MainLayout>
      <div>
      <Questions 
        updateCurrentIndex={setCurrentQuestionIndex} 
        totalQuestions={totalQuestions}
        setQuizCompleted={setQuizCompleted} 
      />

      <ProgressBar current={currentQuestionIndex + 1} total={totalQuestions} quizCompleted={quizCompleted} />
      </div>
      <ChatBox/>
    </MainLayout>
  );
};

export default AssignmentsDetail;
