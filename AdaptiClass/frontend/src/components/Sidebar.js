import React, { useState } from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import {
  RocketIcon,
  HomeIcon,
  CoursesIcon,
  FeedbackIcon,
  SettingsIcon,
} from "../assets/Icons";
import PathConstants from "../routes/pathConstants";

const SidebarContainer = styled.div`
  will-change: width;
  width: ${(props) => (props.$collapsed ? "76px" : "270px")};
  //NOTE: Transition here is causing problems.
  overflow: hidden;
  border-right: 2px solid #ededed;
  display: flex;
  flex-direction: column;
`;

const SidebarHeader = styled.div`
  display: flex;
  height: 66px;
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0px;

  svg {
    width: 26px;
    height: 26px;
    margin-right: 13px; /* Adjust the margin to control spacing */
    margin-left: 25px;
  }

  h3 {
    font-size: 18px;
    color: #3f434a;
  }
`;

const SidebarButton = styled.button`
  display: flex;
  height: 56px;
  width: 100%;

  background-color: ${(props) => (props.$active ? "#f8f8f8" : "#fff")};
  color: #3f434a;
  font-size: 15px;
  border: none;
  cursor: pointer;
  align-items: center;
  padding: 0px;

  svg {
    width: 20px;
    height: 20px;
    margin-left: 28px;
    margin-right: 16px;
    fill: #8a9099;
  }

  &:hover {
    background-color: #f8f8f8;
  }
`;

const Sidebar = ({ collapsed }) => {
  const [activeButton, setActiveButton] = useState(0);

  return (
    <SidebarContainer $collapsed={collapsed}>
      <SidebarHeader>
        <RocketIcon />
        {!collapsed && <h3>AdaptiClass</h3>}
      </SidebarHeader>
      <Link to={PathConstants.HOME}>
        <SidebarButton $active={activeButton === 0} onClick={() => setActiveButton(0)}>
          <HomeIcon />
          {!collapsed && "Home"}
        </SidebarButton>
      </Link>
      <Link to={PathConstants.COURSES}>
        <SidebarButton $active={activeButton === 1} onClick={() => setActiveButton(1)}>
          <CoursesIcon />
          {!collapsed && "Courses"}
        </SidebarButton>
      </Link>
      <Link to={PathConstants.FEEDBACK}>
        <SidebarButton $active={activeButton === 2} onClick={() => setActiveButton(2)}>
          <FeedbackIcon />
          {!collapsed && "Feedback"}
        </SidebarButton>
      </Link>
      <Link to={PathConstants.SETTINGS}>
        <SidebarButton $active={activeButton === 3} onClick={() => setActiveButton(3)}>
          <SettingsIcon />
          {!collapsed && "Settings"}
        </SidebarButton>
      </Link>
    </SidebarContainer>
  );
};

export default Sidebar;
