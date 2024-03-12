import axios from 'axios';

const getStudentByEmail = async (email) => {
    try {
        const response = await axios.get(`http://localhost:3001/students/`, {
            params: {
                email: email,
            }
        });
        return response.data;
    } catch (error) {
        // Handle error
        console.error('Error fetching student by email:', error);
        throw error;
    }
};

// Usage
const email = 'one@email.com'; // Replace with actual email
getStudentByEmail(email)
    .then(student => console.log('Student:', student))
    .catch(error => console.error('Error:', error));
