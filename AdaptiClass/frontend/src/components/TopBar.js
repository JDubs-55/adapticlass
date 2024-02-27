import React from "react";
import styled from "styled-components";
import {CollapseMenuIcon} from "../assets/Icons";

const TopBarWrapper = styled.div`
  width: 100%;
  height: 66px;
  background-color: #fff;
  border-bottom: 2px solid #ededed;
  color: #3f434a;
`;

const TopBarContent = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  
`;

const CollapseMenuButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;

  border: none;
  background-color: #fff;

  svg {
    width: 20px;
    height: 20px;
    margin-left: 30px;
  }
`;

const TopBar = ({toggleSidebar}) => {
  return (
    <TopBarWrapper>
      <TopBarContent>
        <CollapseMenuButton onClick={toggleSidebar}><CollapseMenuIcon/></CollapseMenuButton>
        <h3>Top Bar Content</h3>
      </TopBarContent>
    </TopBarWrapper>
  );
};

export default TopBar;
