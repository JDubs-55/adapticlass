import React from 'react';
import styled from 'styled-components';

const Content = styled.div`
  width: 100%;
  flex: 1;
  padding: 20px;
`;

const SettingsContent = () => {
    return (
        <Content>
            <h1>Settings Page</h1>
            <p>This is where settings components go</p>
        </Content>
    );
};

export default SettingsContent;