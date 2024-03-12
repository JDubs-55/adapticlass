import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Container = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
`

const AxiosExample = ({emailToGet}) => {
    const [studentData, setStudentData] = useState({});
    
    useEffect(() => {
        try {
            const response = axios.get(`http://127.0.0.1:8000/students/`, {
                params: {
                    email: emailToGet,
                }
            });
            
            console.log(response);
            setStudentData(response.data);
        } catch (error) {
            // Handle error
            console.error('Error fetching student by email:', error);
            throw error;
        }
    }, [studentData]);
    
    return (
        <Container>
            Test
        </Container>
    );

};

export default AxiosExample;
