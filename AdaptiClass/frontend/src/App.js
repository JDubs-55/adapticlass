import './styles/global.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import routes from './routes';

function App() {

  const router = createBrowserRouter([
    {
      //parent route
      element: <MainLayout/>,
      children: routes
    },
  ])

  return (
    // <Router>
    //   <Container>
    //     <Sidebar>
    //       Sidebar Content
    //     </Sidebar>
    //     <ContentWrapper>
    //       <TopBar>
    //         Top Bar Content
    //       </TopBar>
    //       <Routes>
    //         <Route path="/" element={<HomeContent />} />
    //         <Route path="/courses" element={<CourseContent/>}/>
    //         <Route path="/feedback" element={<FeedbackContent/>}/>
    //         <Route path="/settings" element={<SettingsContent/>}/>
    //       </Routes>
    //     </ContentWrapper>
    //   </Container>
    // </Router>
    <RouterProvider router={router}/>
  );
}

export default App;
