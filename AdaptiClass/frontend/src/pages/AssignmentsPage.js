import React, { useState, useEffect } from "react";
import styled from "styled-components";
import AssignmentListContainer from "../components/lists/AssignmentListContainer";
import AssignmentInfoPane from "../components/AssignmentInfoPane";
import assignmentData from "../mockRequests/assignmentsBasic.json";

const Container = styled.div`
  width: 100%;
  display: flex;
  background-color: #fff;
`;

const ColumnWrapper = styled.div`
  width: ${(props) => (props.$showInfoPane ? "60%" : "100%")};
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
`;

const PageHeader = styled.div`
  width: 100%;
  height: 66px;

  border-bottom: 2px solid #ededed;
  background-color: #fff;

  display: flex;
  align-items: center;
  justify-content: flex-start;

  h5 {
    color: #3f434a;
    margin-left: 30px;
    font-size: 20px;
    font-weight: 500;
  }
`;

const ListContainer = styled.div`
  max-height: calc(100vh - 136px);
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  overflow-y: auto;
`;

const InfoPaneContainer = styled.div`
  width: ${(props) =>
    props.$showInfoPane
      ? "40%"
      : "0"}; /* Adjust width based on info pane visibility */
  min-width: ${(props) =>
    props.$showInfoPane
        ? "500px"
        : "0"}; /* Adjust width based on info pane visibility */
  display: ${(props) =>
    props.$showInfoPane
      ? "block"
      : "none"}; /* Show/hide based on info pane visibility */
  border-left: 2px solid #ededed;

`;

const AssignmentPage = () => {
  const [jsonData, setJsonData] = useState({});
  const [showInfoPane, setShowInfoPane] = useState(false);
  const [infoPaneData, setInfoPaneData] = useState({});

  //Retrieve data from server
  useEffect(() => {
    const fakeApiCall = async () => {
      setJsonData(assignmentData);
    };

    fakeApiCall();
  }, []);

  const toggleOnInfoPane = (data) => {
    setShowInfoPane(true);
    setInfoPaneData(data);
  };

  const toggleOffInfoPane = () => {
    setShowInfoPane(false);
  };

  return (
    <Container>
      <ColumnWrapper $showInfoPane={showInfoPane}>
        <PageHeader>
          <h5>{jsonData ? jsonData["title"] : ""}</h5>
        </PageHeader>
        <ListContainer>
          <AssignmentListContainer
            isLast={false}
            toggleOnInfoPane={toggleOnInfoPane}
            title="In Progress"
            data={jsonData ? jsonData["in_progress"] || [] : []}
          />
          <AssignmentListContainer
            isLast={false}
            toggleOnInfoPane={toggleOnInfoPane}
            title="Upcoming"
            data={jsonData ? jsonData["upcoming"] || [] : []}
          />
          <AssignmentListContainer
            isLast={true}
            toggleOnInfoPane={toggleOnInfoPane}
            title="Completed"
            data={jsonData ? jsonData["completed"] || [] : []}
          />
        </ListContainer>
      </ColumnWrapper>
      <InfoPaneContainer $showInfoPane={showInfoPane}>
        <AssignmentInfoPane
          toggleOffInfoPane={toggleOffInfoPane}
          data={infoPaneData}
          instructorName={jsonData ? jsonData["instructor"] || "" : ""}
          instructorImage={jsonData ? jsonData["instructor_image"] || "" : ""}
        />
      </InfoPaneContainer>
    </Container>
  );
};

export default AssignmentPage;
