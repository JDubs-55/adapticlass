import React from 'react';
import styled from 'styled-components';

const Content = styled.div`
  flex: 1;
  padding: 20px;
`;

const FeedbackContent = () => {
    return (
        <Content>
            <h1>Feedback Page</h1>
            <p>This is where feedback components go</p>
        </Content>
    );
};

export default FeedbackContent;