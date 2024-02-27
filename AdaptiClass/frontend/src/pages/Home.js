import React from 'react';
import styled from 'styled-components';

const Content = styled.div`
  width: 100%;
  flex: 1;
  padding: 20px;
`;

const HomeContent = () => {
    return (
        <Content>
            <h1>Home Page</h1>
            <p>This is where home components go</p>
        </Content>
    );
};

export default HomeContent;