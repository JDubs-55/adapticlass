import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const ChatContainer = styled.div`
  width: 20%;
  height: calc(100vh - 220px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
  padding: 20px;
  padding-top: 0;
  border-radius: 8px;
  margin: 20px;
  margin-left: 0;
  background-color: #fff;
`;

const ChatTitle = styled.h2`
  font-size: 1.2em;
  color: #333; 
  margin-bottom: 20px; 
  text-align: center; 
`;

const HorizontalSeparator = styled.div`
  height: 2px;
  width: 100%;
  margin-bottom: 10px;
  background-color: #e8e9eb;
`;

const Messages = styled.div`
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 10px; 
  &::-webkit-scrollbar {
    width: 8px;
    border-radius: 4px;
  }
  &::-webkit-scrollbar-thumb {
    background: #ccc; 
    border-radius: 4px;
  }
  &::-webkit-scrollbar-thumb:hover {
    background: #b3b3b3; 
  }
  &::-webkit-scrollbar-button {
    display: none; 
  }
`;

const InputArea = styled.input`
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  width: calc(100% - 40px);
  background-color: #f0f0f0;
  box-shadow: 0px 3px 6px #00000029;
  outline: none;
  font-size: 0.9em; 
`;

const MessageBubble = styled.div`
  background-color: #f0f0f0;
  border-radius: 20px;
  padding: 10px 20px;
  margin-bottom: 10px;
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: 0px 3px 6px #00000029;

  &:last-child {
    margin-bottom: 0;
  }

  align-self: flex-start;
  background-color: #e0e0e0;

  &.sent {
    align-self: flex-end;
    background-color: #304FFD;
    color: white;
    margin-left: 5%;
  }

  pre {
    background-color: #f5f5f5;
    padding: 10px;
    overflow-x: auto;
  }
  code {
    background-color: #f5f5f5;
    padding: 2px 5px;
    border-radius: 4px;
    font-family: 'Courier New', Courier, monospace;
  }
  strong {
    font-weight: bold;
  }
`;

const Form = styled.form`
  margin-top: auto;
`;

const ChatBox = () => {
  const [messages, setMessages] = useState([]);

  const sendMessage = (event) => {
    event.preventDefault();
    const userMessage = newMessage.trim();
    if (!userMessage) return;
  
    // Display the user's question immediately in the chat
    const messageToShow = { text: userMessage, type: 'sent' };
    setMessages([...messages, messageToShow]);
  
    // Reset the input field
    setNewMessage('');
  
    // Making the call to the Django backend
    axios.post('http://localhost:8000/chat/', { question: userMessage })
      .then(response => {
        // Check for 'solution' in the response data
        if(response.data.solution) {
          const reply = response.data.solution;
          setMessages(messages => [...messages, { text: reply, type: 'received' }]);
        } else if(response.data.error) {
          // If the backend returns an error message, display it
          setMessages(messages => [...messages, { text: response.data.error, type: 'received' }]);
        }
      })
      .catch(error => {
        console.error('Error fetching response:', error);
        // Handle cases where the error response contains an explicit message
        const errorMessage = error.response && error.response.data.error ? error.response.data.error : 'Sorry, there was a problem getting a response.';
        setMessages(messages => [...messages, { text: errorMessage, type: 'received' }]);
      });
  };

  const [newMessage, setNewMessage] = useState('');

  return (
    <ChatContainer>
      <ChatTitle>Need help? Let's solve it together</ChatTitle>
      <HorizontalSeparator/>
      <Messages>
        {messages.map((message, index) => (
          <MessageBubble key={index} className={message.type}>
            <ReactMarkdown>{message.text}</ReactMarkdown>
          </MessageBubble>
        ))}
      </Messages>
      <Form onSubmit={sendMessage}>
        <InputArea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Enter the problem here..."
        />
      </Form>
    </ChatContainer>
  );
};

export default ChatBox;