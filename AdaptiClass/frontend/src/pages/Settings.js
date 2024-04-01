import React from 'react';
import styled from 'styled-components';

const Content = styled.div`
  width: 100%;
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; 
  background: #f7f7f7; 
`;

const Title = styled.h1`
  font-weight: bold;
  margin: 0 0 24px 0;
  color: #3949ab; 
  text-transform: uppercase;
  letter-spacing: 1.5px; 
`;

const Subtitle = styled.h2`
  font-weight: 600; 
  margin: 32px 0 20px 0;
  color: #3949ab; 
  text-transform: uppercase; 
  letter-spacing: 1.2px; 
`;

const AboutText = styled.p`
  font-size: 18px; 
  max-width: 800px; 
  color: #333; 
  line-height: 1.6; 
  margin-bottom: 30px; 
`;

const TeamList = styled.div`
  max-width: 800px;
  width: 100%;
  text-align: center; 
`;

const TeamMember = styled.div`
  font-size: 16px; 
  color: #555; 
  margin: 10px 0;
  padding: 10px 0;
  border-bottom: 1px solid #ddd; 
`;

const AboutUsContent = () => {
    return (
        <Content>
            <Title>About AdaptiClass</Title>
            <AboutText>
                At AdaptiClass, we empower students with a unique educational experience
                that adapts to their individual learning needs. Our platform is built on
                the promise of personalized learning, offering AI-powered lessons and 
                practice problems, alongside attentive tracking technology to maximize 
                engagement and comprehension.
            </AboutText>
            <Subtitle>Meet the Team</Subtitle>
            <TeamList>
                <TeamMember>Syed Naser Ashraf - Front End Developer</TeamMember>
                <TeamMember>Kyle Chamblee - Back End Developer</TeamMember>
                <TeamMember>Mary Klawa - Quality Assurance Engineer</TeamMember>
                <TeamMember>Shalini Patel - Database Administrator</TeamMember>
                <TeamMember>Johnathan Weller - Front End Developer</TeamMember>
            </TeamList>
        </Content>
    );
};

export default AboutUsContent;
