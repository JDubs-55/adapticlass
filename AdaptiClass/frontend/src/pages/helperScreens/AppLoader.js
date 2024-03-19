import React from "react";
import styled, { keyframes }from "styled-components";
import { RocketIcon } from "../../assets/Icons";

const LoadingPageWrapper = styled.div`
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const CenterContainer = styled.div`
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items:center;

  svg {
    width: 50px;
    height: auto;
  }
`;

const AppName = styled.h1`
  margin-top: 10px;
  font-size: 24px;
`;

const rotate = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const LoadingSymbol = styled.div`
  margin-top: 20px;
  border: 4px solid #ccc;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  animation: ${rotate} 1s linear infinite;
`;

export const AppLoader = () => {
  return (
    <LoadingPageWrapper>
      <CenterContainer>
        <RocketIcon/>
        <AppName>AdaptiClass</AppName>
        <LoadingSymbol/>
      </CenterContainer>
    </LoadingPageWrapper>
  );
};