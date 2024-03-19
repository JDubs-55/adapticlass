import React from "react";
import styled from "styled-components";

import { SettingsIcon, UserIcon, LogoutIcon } from "../assets/Icons";
import { useNavigate } from "react-router-dom";
import PathConstants from "../routes/pathConstants";
import { useAuth0 } from "@auth0/auth0-react";

const DropdownContainer = styled.div`
  margin: 8px 20px;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
`;

const ProfileInformationContainer = styled.div`
  width: 100%;
  height: 43px;
  margin: 15px 10px;

  display: flex;
  align-items: center;
  justify-content: flex-start;

  img {
    width: 40px;
    height: 40px;
    border-radius: 100%;
  }
`;

const ProfileInformationLabelContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin-left: 10px;
`;

const Username = styled.p`
  margin: 0;
  font-size: 15px;
`;

const Role = styled.p`
  margin: 0;
  font-size: 13px;
  color: #8a9099;
`;

const HorizontalSeparator = styled.div`
  height: 1px;
  width: 100%;
  background-color: #e8e9eb;
  margin: 8px 0;
`;

const DropdownButton = styled.button`
  padding: 4px 0;
  border: none;
  cursor: pointer;

  width: 100%;
  height: 40px;
  border-radius: 14px;
  font-size: 15px;
  background-color: #fff;
  color: #8a9099;

  display: flex;
  align-items: center;
  justify-content: flex-start;

  &:hover {
    background-color: #f8f8f8;
    color: #3f434a;
  }

  svg {
    margin-left: 15px;
    margin-right: 10px;
    width: 15px;
    height: auto;
  }
`;

const UserProfileDropdown = ({ image, name, role, toggleDropdown }) => {
  const navigate = useNavigate();
  const { logout } = useAuth0();

  const handleButtonClick = (route) => {
    toggleDropdown();
    navigate(route);
  };

  const handleLogout = () => {
    toggleDropdown();
    logout({ returnTo: PathConstants.HOME });
  };

  return (
    <DropdownContainer>
      <ProfileInformationContainer>
        <img src={image} alt="Profile" />
        <ProfileInformationLabelContainer>
          <Username>{name}</Username>
          <Role>{role}</Role>
        </ProfileInformationLabelContainer>
      </ProfileInformationContainer>
      <HorizontalSeparator />
      <DropdownButton onClick={() => handleButtonClick(PathConstants.SETTINGS)}>
        <UserIcon />
        My Profile
      </DropdownButton>
      <DropdownButton onClick={() => handleButtonClick(PathConstants.SETTINGS)}>
        <SettingsIcon />
        Settings
      </DropdownButton>
      <HorizontalSeparator />
      <DropdownButton onClick={handleLogout}>
        <LogoutIcon />
        Logout
      </DropdownButton>
    </DropdownContainer>
  );
};

export default UserProfileDropdown;
