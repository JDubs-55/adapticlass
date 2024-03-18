import React from "react";
import styled from "styled-components";
import {
  CheckboxUncheckedIcon,
  CheckboxCheckedIcon,
  CheckboxClosedIcon,
  CheckboxSquareIcon,
  CalendarIcon,
} from "../../assets/Icons";

const TodoItem = styled.button`
  width: 100%;
  height: 56px;
  border: none;
  background-color: inherit;

  display: flex;
  align-items: center;
  justify-content: space-between;

  border: solid 1px #e8e9eb;
  border-radius: 20px;

  &:hover {
    background-color: #f8f8f8;
  }
`;

const JustifyLeftContainer = styled.div`
  width: 75%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
`;

const JustifyRightContainer = styled.div`
  width: 25%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
  margin-right: 10px;
`;

const CircleCheckboxWrapper = styled.div`
  display: flex;

  svg {
    width: 22px;
    height: auto;
    margin-left: 10px;
    color: ${(isComplete) => isComplete ? "#304FFD" : "#fff"};
  }
`;

const SquareCheckboxWrapper = styled.div`
  display: flex;

  svg {
    width: 20px;
    height: auto;
    color: #8A9099;
  }
`;

const CalendarWrapper = styled.div`
  display: flex;

  svg {
    width: 20px;
    height: auto;
    color: #8A9099;
  }
`;

const LargeItemLabel = styled.body`
  font-size: 14px;
  font-weight: 400;
  color: #3f434a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
`;

const SmallItemLabel = styled.body`
    font-size: 14px;
    font-weight: 400;
    color: #3f434a;
`;

const AssignmentListItem = ({ data, toggleOnInfoPane }) => {
  const isComplete = data["status"] === "complete";

  const calcCompletionStatus = (elements) => {
    let complete = 0;
    let total = elements.length;
    for (let element of elements) {
      if (element["status"] === "complete") {
        complete += 1;
      }
    }
    return `${complete}/${total}`;
  };

  const formatDate = (jsonDate) => {
    jsonDate = jsonDate.replace(/\s+/, '');

    const date = new Date(jsonDate);
    const options = { month: "short", day: "numeric" };
    const formattedDate = date.toLocaleDateString("en-US", options);
    return formattedDate;
  };

  return (
    <TodoItem onClick={() => toggleOnInfoPane(data)}>
      <JustifyLeftContainer>
        <CircleCheckboxWrapper>
          {isComplete ? <CheckboxClosedIcon isComplete={isComplete}/> : <CheckboxUncheckedIcon/>}
        </CircleCheckboxWrapper>
        <LargeItemLabel>{data["title"]}</LargeItemLabel>
        <SquareCheckboxWrapper>
          <CheckboxSquareIcon />
        </SquareCheckboxWrapper>
        <SmallItemLabel>
          {calcCompletionStatus(data["course_elements"])}
        </SmallItemLabel>
      </JustifyLeftContainer>
      <JustifyRightContainer>
        <CalendarWrapper>
          <CalendarIcon />
        </CalendarWrapper>
        <SmallItemLabel>{formatDate(data["due_date"])}</SmallItemLabel>
      </JustifyRightContainer>
    </TodoItem>
  );
};

export default AssignmentListItem;
