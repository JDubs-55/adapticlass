import React from "react";
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
  width: 18.75%;
  @media (min-width: 1440px) {
    width: 270px;
  }

  background-color: #fff;
  color: #fff;

  border-right: 2px solid #ededed;

  display: flex;
  flex-direction: column;
`;

const SidebarHeader = styled.div`
  display: block;
  height: 66px;
  width: 100%;
  // background-color: red;
  display: flex;
  align-items: center;

  svg {
    width: 25px;
    height: 25px;
    margin-right: 12px; /* Adjust the margin to control spacing */
    margin-left: 30px;
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

  background-color: #fff;
  color: #3f434a;
  font-size: 15px;
  border: none;
  cursor: pointer;
  align-items: center;

  /* Style for the SVG icon */
  svg {
    width: 16px;
    height: 16px;
    margin-right: 16px; /* Adjust the margin to control spacing */
    margin-left: 24px;
  }

  &:hover {
    background-color: #f8f8f8;
  }
`;

const Sidebar = () => {
  
  return (
    <SidebarContainer>
      <SidebarHeader>
        <RocketIcon />
        <h3>AdaptiClass</h3>
      </SidebarHeader>
      <Link to={PathConstants.HOME}>
        <SidebarButton>
          <HomeIcon />
          Home
        </SidebarButton>
      </Link>
      <Link to={PathConstants.COURSES}>
        <SidebarButton>
          <CoursesIcon />
          Courses
        </SidebarButton>
      </Link>
      <Link to={PathConstants.FEEDBACK}>
        <SidebarButton>
          <FeedbackIcon />
          Feedback
        </SidebarButton>
      </Link>
      <Link to={PathConstants.SETTINGS}>
        <SidebarButton>
          <SettingsIcon />
          Settings
        </SidebarButton>
      </Link>
    </SidebarContainer>
  );
};

export default Sidebar;
