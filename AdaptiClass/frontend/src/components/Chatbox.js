import React, { useState } from 'react';
import styled from 'styled-components';

const ChatContainer = styled.div`
  width: 300px;
  height: calc(100vh - 100px);
  max-height: 800px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
`;

const ChatTitle = styled.h2`
  font-size: 1.2em;
  color: #333; 
  margin-bottom: 20px; 
  text-align: center; 
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
    background-color: #4caf50;
    color: white; 
  }
`;



const Form = styled.form`
  margin-top: auto;
`;

const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
  
    const sendMessage = (event) => {
      event.preventDefault();
      if (!newMessage.trim()) return;
      setMessages([...messages, newMessage]);
      setNewMessage('');
    };
  
    return (
      <ChatContainer>
        <ChatTitle>Need help? Ask me a question</ChatTitle>
        <Messages>
          {messages.map((message, index) => (
            <MessageBubble key={index}>{message}</MessageBubble>
          ))}
        </Messages>
        <Form onSubmit={sendMessage}>
          <InputArea
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type your message..."
          />
        </Form>
      </ChatContainer>
    );
  };
  
  

export default ChatBox;

/* const sendMessage = async (event) => {
   event.preventDefault();
    if (!newMessage.trim()) return;
  
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: newMessage }),
      });
  
      if (response.ok) {
        const data = await response.json();
  */