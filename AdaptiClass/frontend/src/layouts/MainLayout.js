import React, { useState, useEffect } from "react";
import { Suspense } from "react";
import { Outlet } from "react-router-dom";
import styled from "styled-components";

import Sidebar from "../components/Sidebar";
import TopBar from "../components/TopBar";

import { PageLoader } from "../pages/PageLoader";

const Container = styled.div`
  display: flex;
  height: 100vh;
  overflow-x: hidden;
`;

const ContentWrapper = styled.div`
  height: 100vh;
  display: flex;
  flex-direction: column;
  flex: 1;
`;

const MainLayout = () => {
  //**Collapsable Sidebar**
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  //For button in top bar.
  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  //For screen size change.
  const handleResize = () => {
    // Update the collapsed state based on the screen width
    setSidebarCollapsed(window.innerWidth <= 1000);
  };

  //Detect screen size change.
  useEffect(() => {
    // Set initial collapsed state on mount
    handleResize();

    // Add event listener for window resize
    window.addEventListener("resize", handleResize);

    // Clean up the event listener on component unmount
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);
  //**End Collapsable Sidebar Functionality**

  return (
    <Container>
      <Sidebar collapsed={sidebarCollapsed} />
      <ContentWrapper>
        <TopBar toggleSidebar={toggleSidebar} />
        <Suspense fallback={<PageLoader />}>
          <Outlet />
        </Suspense>
      </ContentWrapper>
    </Container>
  );
};

export default MainLayout;
