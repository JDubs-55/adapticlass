
import React from 'react';
import styled from "styled-components";


const TopBarWrapper = styled.div`
  width: 100%;
  height: 66px;
  background-color: #4285f4; /* Google Blue color for illustration */
  color: #fff;
`;

const TopBar = () => {
    return (
        <TopBarWrapper>Top Bar Content</TopBarWrapper>
    );
};

export default TopBar