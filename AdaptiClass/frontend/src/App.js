import './styles/global.css';
import { Route, Routes, Navigate} from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Callback from './pages/Callback';
import React, {useState} from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { AppLoader } from './pages/AppLoader';
import { AuthenticationGuard } from './authentication/AuthenticationGuard';
import PathConstants from './routes/pathConstants';
import AxiosExample from './components/Axios';
import NewUserDetailsForm from './pages/NewUser';
import axios from 'axios';
import { withAuthenticationRequired } from "@auth0/auth0-react";

const HomeContent = React.lazy(() => import("./pages/Home"))
const CourseContent = React.lazy(() => import("./pages/Courses"))
const FeedbackContent = React.lazy(() => import("./pages/Feedback"))
const SettingsContent = React.lazy(() => import("./pages/Settings"))

function App() {
  const { isAuthenticated, isLoading, loginWithRedirect, user } = useAuth0();
  const [userExists, setUserExists] = useState(false);
  const [userRole, setUserRole] = useState('');


  //Wait for the app to load. 
  if (isLoading && !isAuthenticated) {
    return (
        <AppLoader />
    );
  }

  const getRedirectComponent = () => {
    if (isAuthenticated) {
      //Check whether the user is a new user
      try {
        const response = axios.get(`http://127.0.0.1:8000/userexists`, {
                params: {
                    auth_id: user.sub,
                }
            });
        setUserExists(response.data["exists"]);
      } catch (error) {
        console.error('Error checking whether the user exists', error);
        throw error;
      }
      //get more info from the user if they are new, otherwise get their role and navigate to the right page
      if (!userExists) {
        return <Navigate to={PathConstants.NEWUSER}/>;
      } else {
        //Get user's info
        try {
          const response = axios.get(`http://127.0.0.1:8000/userinfo`, {
              params: {
                  auth_id: user.sub,
              }
            });
          setUserRole(response.data["role"]);
        } catch (error) {
          console.error("Error getting the user's role");
        }

        if (userRole === 'student') {
          return <Navigate to={PathConstants.STUDENT}/>
        } else if (userRole === 'instructor') {
          return <Navigate to={PathConstants.INSTRUCTOR}/>
        }

      }
    } else {
      loginWithRedirect();
      return <div>Test</div>;
    }
  };

  return (
    <Routes>
      <Route path={PathConstants.NEWUSER} element={<AuthenticationGuard component={NewUserDetailsForm}/>}/>
      <Route path={PathConstants.STUDENT} element={<AuthenticationGuard component={MainLayout}/>}>
        <Route path={PathConstants.HOME} element={<HomeContent/>}/>
        <Route path={PathConstants.COURSES} element={<CourseContent/>}/>
        <Route path={PathConstants.FEEDBACK} element={<FeedbackContent/>}/>
        <Route path={PathConstants.SETTINGS} element={<SettingsContent/>}/>
      </Route>
      <Route path={PathConstants.TEACHER} element={<AuthenticationGuard component={MainLayout}/>}>
        <Route path={PathConstants.HOME} element={<div>Teacher Home Component</div>}/>
        <Route path={PathConstants.COURSES} element={<div>Teacher Courses Component</div>}/>
        <Route path={PathConstants.FEEDBACK} element={<div>Teacher Feedback Component</div>}/>
        <Route path={PathConstants.SETTINGS} element={<div>Teacher Settings Component</div>}/>
        
      </Route>
      <Route path="/axiostest" element={<AxiosExample emailToGet="three@email.com"/>}/>
      <Route path="/" element={<AuthenticationGuard component={getRedirectComponent}/>}/>
      {/* <Route path={PathConstants.CALLBACK} element={<Callback/>} /> */}

      {/* Debug Routes for testing individual components */}
      {/* <Route path={"/testapploader"} element={<AppLoader/>} /> */}
    </Routes>
  );
}

export default App;
