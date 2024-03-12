import React, { useState } from 'react';
import styled from 'styled-components';
import { RocketIcon } from '../assets/Icons';
import { useAuth0 } from "@auth0/auth0-react";
import axios from 'axios';

const PageWrapper = styled.div`
    height: 100vh;
    max-height: 100vh;
    width: 100%;
    background-color: #304FFD;

    display: flex;
    justify-content: center;
    align-items: center;
`;

const Container = styled.div`
  width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 20px;
`;

const AppNameContainer = styled.div`
    width: 100%;

    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;

    svg {
        width: 40px;
        height: auto;
    }
`

const AppName = styled.h1`
  margin-top: 10px;
  font-size: 24px;
`;

const FormTitle = styled.h3`
    width: 100%;
    text-align: center;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  margin-bottom: 10px;
  color: #8A9099;
  font-size: 14px;
`;

const Input = styled.input`
  margin-bottom: 30px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  color: #3F434A;
`;

const Select = styled.select`
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
`;

const RoleButtonContainer = styled.div`
    
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;

    margin-bottom: 20px;
`;

const RoleButton = styled.button`
  width: calc(50% - 10px);
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 50px;
  border: ${(props)=>(props.selected ? '1px solid #304FFD' : '1px solid #8A9099')};
  background-color: ${(props) => (props.selected ? '#304FFD' : '#fff')};
  color: ${(props) => (props.selected ? '#fff' : '#8A9099')};
  font-size: 15px;
  font-family: Poppins;
  cursor: pointer;
`;

const Button = styled.button`
  padding: 10px 20px;
  border-radius: 50px;
  border: none;
  background-color: #304FFD;
  color: #fff;
  font-size: 15px;
  font-family: Poppins;
  cursor: pointer;
`;

const NewUserDetailsForm = () => {
  const { user } = useAuth0();
  const [displayName, setDisplayName] = useState(user.name);
  const [role, setRole] = useState('student');

  const handleSubmit = (e) => {
    e.preventDefault();

    const data = {
        auth_id: user.sub,
        email: user.email, 
        email_verified: user.email_verified,
        auth0_name: user.name,
        display_name: displayName,
        picture: user.picture,
        role: role,
    }

    //DEBUG
    console.log(data);

    //SEND TO SERVER
    axios.post('http://localhost:3001/adduser', data)
    .then(response => {
        console.log('Data sent successfully:', response.data);
        // Handle response if needed
    })
    .catch(error => {
        console.error('Error sending data:', error);
        // Handle error if needed
    });
  };

  return (
    <PageWrapper>
    <Container>
      <AppNameContainer>
        <RocketIcon/>
        <AppName>AdaptiClass</AppName>
      </AppNameContainer>
      <FormTitle>Update Your User Profile</FormTitle>
      <Form onSubmit={handleSubmit}>
        <Label>Change Display Name</Label>
        <Input
          type="text"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
        />
        <Label>Select A Role</Label>
        <RoleButtonContainer>
          <RoleButton
            type="button"
            selected={role === 'student'}
            onClick={() => setRole('student')}
          >
            Student
          </RoleButton>
          <RoleButton
            type="button"
            selected={role === 'instructor'}
            onClick={() => setRole('instructor')}
          >
            Instructor
          </RoleButton>
        </RoleButtonContainer>
        <Button type="submit">Submit</Button>
      </Form>
    </Container>
    </PageWrapper>
  );
};

export default NewUserDetailsForm;