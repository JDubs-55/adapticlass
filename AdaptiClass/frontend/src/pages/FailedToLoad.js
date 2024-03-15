import React from "react";
import styled, { keyframes }from "styled-components";
import { RocketIcon } from "../assets/Icons";

const LoadingPageWrapper = styled.div`
  width: 100%;
  flex: 1;
  padding: 20px;
  
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

const Message = styled.body`
    font-size: 14px;
    font-weight: 400;
    color: #595F69;
`;



export const FailedToLoadPage = () => {
  return (
    <LoadingPageWrapper>
      <CenterContainer>
        <RocketIcon/>
        <AppName>AdaptiClass</AppName>
        <Message>Sorry, this content couldn't be loaded...</Message>
      </CenterContainer>
    </LoadingPageWrapper>
  );
};