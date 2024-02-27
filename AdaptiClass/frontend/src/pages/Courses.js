import React from 'react';
import styled from 'styled-components';

const Content = styled.div`
  width: 100%;
  flex: 1;
  padding: 20px;
`;

const CourseContent = () => {
    return (
        <Content>
            <h1>Courses Page</h1>
            <p>This is where course components go</p>
        </Content>
    );
};

export default CourseContent;