import './styles/global.css';
import { Route, Routes } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Callback from './pages/Callback';
import React from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { AppLoader } from './pages/AppLoader';
import { AuthenticationGuard } from './authentication/AuthenticationGuard';
import PathConstants from './routes/pathConstants';

const HomeContent = React.lazy(() => import("./pages/Home"))
const CourseContent = React.lazy(() => import("./pages/Courses"))
const FeedbackContent = React.lazy(() => import("./pages/Feedback"))
const SettingsContent = React.lazy(() => import("./pages/Settings"))

function App() {
  const {isLoading, isAuthenticated} = useAuth0();

  //Wait for the app to load. 
  if (isLoading && !isAuthenticated) {
    return (
        <AppLoader />
    );
  }

  return (
    <Routes>
      <Route path={PathConstants.HOME} element={<AuthenticationGuard component={MainLayout}/>}>
        <Route path={PathConstants.HOME} element={<HomeContent/>}/>
        <Route path={PathConstants.COURSES} element={<CourseContent/>}/>
        <Route path={PathConstants.FEEDBACK} element={<FeedbackContent/>}/>
        <Route path={PathConstants.SETTINGS} element={<SettingsContent/>}/>
        {/* Debug Routes for testing individual components */}
        {/* <Route path={"/testpageloader"} element={<PageLoader/>}/> */}
      </Route>
      <Route path={PathConstants.CALLBACK} element={<Callback/>} />

      {/* Debug Routes for testing individual components */}
      {/* <Route path={"/testapploader"} element={<AppLoader/>} /> */}
    </Routes>
  );
}

export default App;
