import React from "react";
import styled from "styled-components";
import {
  CrossoutIcon,
  ZapIcon,
  CalendarIcon,
  CheckboxClosedIcon,
  CheckboxUncheckedIcon,
} from "../assets/Icons";
import CompletionBar from "./CompletionBar";

const ComponentWrapper = styled.div`
  width: 100%;

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 20px;
`;

const ButtonContainer = styled.div`
  width: 100%;
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const CloseButton = styled.button`
  margin: 0;
  padding: 0;
  border: none;
  background-color: #fff;
  margin-left: 20px;
  display: flex;

  svg {
    width: 20px;
    height: auto;
    color: #595f69;
  }
`;

const StartButton = styled.button`
  width: 130px;
  margin: 0;
  padding: 5px;
  border: none;
  background-color: #304ffd;
  border-radius: 14px;
  margin-right: 30px;

  display: flex;
  justify-content: flex-start;
  align-items: center;

  svg {
    width: 20px;
    height: auto;
    color: #fff;
    margin-left: 8px;
  }

  body {
    flex-grow: 1;
    font-weight: 500;
    font-size: 15px;
    text-align: center;
    margin-right: 8px;
    color: #fff;
  }
`;

const AssignmentTitle = styled.div`
  width: 100%;

  h5 {
    margin: 0;
    margin-top: 10px;
    margin-left: 20px;
    font-weight: 500;
    font-size: 20px;
    text-wrap: balance;
    text-align: left;
  }
`;

const TwoColWrapper = styled.div`
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 30px;
`;

const DueDateContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 16px;
  margin-left: 20px;

  body {
    font-weight: 500;
    font-size: 14px;
    color: #595f69;
  }
`;
const DueDate = styled.div`
  width: 100%;
  border: solid 1px #ededed;
  border-radius: 14px;

  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;

  padding: 8px 0;

  svg {
    width: 20px;
    height: auto;
    color: #3f434a;
    margin-left: 15px;
  }

  body {
    font-size: 14px;
    color: #3f434a;
    margin-right: 15px;
  }
`;

const InstructorContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 16px;

  body {
    font-weight: 500;
    font-size: 14px;
    color: #595f69;
  }
`;
const Instructor = styled.div`
  width: 100%;
  border: solid 1px #ededed;
  border-radius: 14px;

  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;

  padding: 8px 0;

  img {
    width: 20px;
    height: auto;
    border-radius: 50%;
    margin-left: 15px;
  }

  body {
    font-size: 14px;
    color: #3f434a;
    margin-right: 15px;
  }
`;

const AssignmentDescriptionWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 16px;
`;

const AssignmentDescriptionLabel = styled.body`
  font-weight: 500;
  font-size: 14px;
  color: #595f69;
  margin-left: 20px;
  margin-right: 20px;
`;

const AssignmentDescriptionText = styled.body`
  font-size: 14px;
  color: #595f69;
  text-wrap: wrap;
  text-align: left;
  margin-left: 20px;
  margin-right: 20px;
`;

const ClassCompletionWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 15px;
`;

const ClassCompletionLabel = styled.body`
  font-weight: 500;
  font-size: 14px;
  color: #595f69;
  margin-left: 20px;
`;

const CompletionBarWrapper = styled.div`
  width: calc(100% - 40px);
  margin-left: 20px;

  display: flex;
  align-items: center;
  justify-content: center;
`;

const CompletionElement = styled.div`
  width: calc(100% - 40px);
  margin-left: 20px;

  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;

  svg {
    width: 18px;
    height: auto;
    color: #304ffd;
  }

  body {
    font-size: 14px;
    color: #3f434a;
  }
`;

const AssignmentInfoPane = ({
  data,
  instructorName,
  instructorImage,
  toggleOffInfoPane,
}) => {
  const completionBarPercent = (elements) => {
    let complete = 0;
    let total = elements.length;
    for (let element of elements) {
      if (element["status"] === "complete") {
        complete += 1;
      }
    }
    return `${Math.floor((complete / total) * 100)}%`;
  };

  const convertJsonDate = (jsonDate) => {
    jsonDate = jsonDate.replace(/\s+/, "");

    const date = new Date(jsonDate);
    const options = {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "numeric",
      hour12: true,
    };
    const formattedDate = date.toLocaleDateString("en-US", options);
    return formattedDate;
  };

  return (
    <ComponentWrapper>
      <ButtonContainer>
        <CloseButton onClick={toggleOffInfoPane}>
          <CrossoutIcon />
        </CloseButton>
        <StartButton>
          <ZapIcon />
          <body>Start</body>
        </StartButton>
      </ButtonContainer>
      <AssignmentTitle>
        <h5>{data["title"]}</h5>
      </AssignmentTitle>
      <TwoColWrapper>
        <DueDateContainer>
          <body>DUE DATE</body>
          <DueDate>
            <CalendarIcon />
            <body>
              {data["due_date"] ? convertJsonDate(data["due_date"]) || "" : ""}
            </body>
          </DueDate>
        </DueDateContainer>
        <InstructorContainer>
          <body>INSTRUCTOR</body>
          <Instructor>
            <img src={instructorImage} alt="Instructor" />
            <body>{instructorName}</body>
          </Instructor>
        </InstructorContainer>
      </TwoColWrapper>
      <AssignmentDescriptionWrapper>
        <AssignmentDescriptionLabel>DESCRIPTION</AssignmentDescriptionLabel>
        <AssignmentDescriptionText>
          {data["description"]}
        </AssignmentDescriptionText>
      </AssignmentDescriptionWrapper>
      <ClassCompletionWrapper>
        <ClassCompletionLabel>{`Class Completion (${
          data["course_elements"]
            ? completionBarPercent(data["course_elements"]) || "0%"
            : "0%"
        })`}</ClassCompletionLabel>
        <CompletionBarWrapper>
          <CompletionBar
            width={
              data["course_elements"]
                ? completionBarPercent(data["course_elements"]) || "0%"
                : "0%"
            }
          />
        </CompletionBarWrapper>
        {data["course_elements"] &&
          data["course_elements"].map((element) => (
            <CompletionElement>
              {element["status"] === "complete" ? (
                <CheckboxClosedIcon />
              ) : (
                <CheckboxUncheckedIcon />
              )}
              <body>{element["title"]}</body>
            </CompletionElement>
          ))}
      </ClassCompletionWrapper>
    </ComponentWrapper>
  );
};

export default AssignmentInfoPane;
