import React, { useState, useEffect } from "react";
import styled from "styled-components";

const MainLayout = styled.div`
  width: 100%;
  display: flex;
  align-items: flex-start;
  height: calc(100vh - 140px);
  overflow-y: hidden;
  background-color: #f8f8f8;
`;

const LessonActivity = () => {

    return(
        <MainLayout>
            This is Lesson Content
        </MainLayout>

    );
};

export default LessonActivity;
