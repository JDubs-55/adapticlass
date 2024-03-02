import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";
import { useAuth0 } from "@auth0/auth0-react";
import { DownArrowIcon } from "../assets/Icons";
import UserProfileDropdown from "./UserProfileDropdown";

// Define styled components
const ProfileSectionWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 5px;
  padding: 6px 10px;
  border-radius: 14px;
  background-color: ${({ show }) => (show ? "#f8f8f8" : "#fff")};
`;

const ProfileSectionContainer = styled.div`
  margin-right: 30px;
  height: 66px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const ProfileHeader = styled.div`
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  img {
    width: 40px;
    height: 40px;
    border-radius: 100%;
  }

  svg {
    width: 8px;
    height: auto;
    fill: #3f434a;
  }
`;

const Username = styled.body`
  font-size: 15px;
`;

const DropdownContent = styled.div`
  display: ${({ show }) => (show ? "block" : "none")};
  position: absolute;
  top: 105%; /* Position below the header */
  right: 0;
  z-index: 1000;
  background-color: white;
  border: 1px solid #e8e9eb;
  border-radius: 14px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a subtle shadow for depth */

  min-width: 260px;
  width: max-content;
`;

const TopBarUserProfile = () => {
  const { user, isAuthenticated } = useAuth0();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  const handleClickOutside = (event) => {
    const dropdownTrigger = document.getElementById("dropdown-trigger"); // Use the actual ID or class of your trigger element
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target) &&
      event.target !== dropdownTrigger &&
      !dropdownTrigger.contains(event.target)
    ) {
      setShowDropdown(false);
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []); // Cleanup the event listener on component unmount

  if (!isAuthenticated) {
    return null; // Don't render anything if the user is not authenticated
  }

  return (
    <ProfileSectionContainer>
      <ProfileSectionWrapper show={showDropdown}>
        <ProfileHeader onClick={toggleDropdown} id="dropdown-trigger">
          <img src={user.picture} alt="Profile" />
          <Username>{user.name}</Username>
          <DownArrowIcon />
        </ProfileHeader>
        <DropdownContent show={showDropdown} ref={dropdownRef}>
          <UserProfileDropdown
            image={user.picture}
            name={user.name}
            role={"Student"}
            toggleDropdown={toggleDropdown}
          />
        </DropdownContent>
      </ProfileSectionWrapper>
    </ProfileSectionContainer>
  );
};

export default TopBarUserProfile;
