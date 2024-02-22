import React from 'react';
import { Suspense } from 'react';
import { Outlet } from 'react-router-dom';
import styled from 'styled-components';

import Sidebar from '../components/Sidebar';
import TopBar from '../components/TopBar';

const Container = styled.div`
  display: flex;
  height: 100vh;
`;

const ContentWrapper = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
`;

const MainLayout = () => {
  // const [collapsed, setCollapsed] = useState(false);

  // const toggleSidebar = () => {
  //   setCollapsed(!collapsed);
  // };

  return (
    <Container>
      <Sidebar/>
      <ContentWrapper>
        <TopBar/>
        <Suspense fallback={<div>Loading...</div>}>
          <Outlet/>
        </Suspense>
      </ContentWrapper>
    </Container>
  );
};

export default MainLayout;