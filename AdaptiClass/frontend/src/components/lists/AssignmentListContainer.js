import React, {useState} from "react";
import styled from "styled-components";
import { DownArrowLineIcon } from "../../assets/Icons";
import AssignmentListItem from "./AssignmentListItem";

const TodoContainer = styled.div`
  width: calc(100% - 60px);

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 8px;
  margin-top: 30px;
  margin-left: 30px;
  margin-bottom: ${(props)=>props.$isLast ? "30px" : "0"};
`;

const TodoHeader = styled.button`
  width: 100%;
  height: 30px;
  border: none;
  background-color: inherit;

  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;

  margin: 10px 0;

  svg {
    width: 16px;
    height: auto;
    fill: #8a9099;
    transform: ${(props)=>props.$itemsShown ? "scaleY(-1)" : "scaleY(1)"};
  }

  h5 {
    margin: 0;
    font-size: 20px;
    font-weight: 500;
    color: #3f434a;
  }

  p {
    margin: 0;
    font-size: 14px;
    font-weight: 500;
    color: #8a9099;
  }
`;

const AssignmentListContainer = ({
  isLast,
  toggleOnInfoPane,
  data,
  title,
}) => {
  const [showItems, setShowItems] = useState(true); // State to manage visibility of map items
  const numElements = data.length;

  const toggleItemsVisibility = () => {
    setShowItems(!showItems);
  }

  return (
    <TodoContainer $isLast={isLast}>
      <TodoHeader $itemsShown={showItems} onClick={toggleItemsVisibility}>
        <DownArrowLineIcon />
        <h5>{title}</h5>
        <p>{`(${numElements})`}</p>
      </TodoHeader>
      {showItems && data.map((element, index) => (
        <AssignmentListItem
            toggleOnInfoPane={toggleOnInfoPane}
            key={index} 
            data={element}
        />
      ))}
    </TodoContainer>
  );
};

export default AssignmentListContainer;
