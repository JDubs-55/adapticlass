import "./styles/global.css";
import { Route, Routes } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { AppLoader } from "./pages/helperScreens/AppLoader";
import { AuthenticationGuard } from "./authentication/AuthenticationGuard";
import PathConstants from "./routes/pathConstants";
import NewUserDetailsForm from "./pages/helperScreens/NewUser";
import RedirectComponent from "./authentication/RedirectComponent";
import { FailedToLoadPage } from './pages/helperScreens/FailedToLoad';
import WebGazerComponent from "./pages/helperScreens/WebGazerComponent";

const HomeContent = React.lazy(() => import("./pages/Home"));
const CourseContent = React.lazy(() => import("./pages/Courses"));
const FeedbackContent = React.lazy(() => import("./pages/Feedback"));
const SettingsContent = React.lazy(() => import("./pages/Settings"));
const AssignmentPage = React.lazy(() => import("./pages/AssignmentsPage"));
const AssignmentsDetailPage = React.lazy(() => import("./pages/AssignmentsDetailPage"));

function App() {
  const { isAuthenticated, isLoading } = useAuth0();

  //Wait for the app to load.
  if (isLoading && !isAuthenticated) {
    return <AppLoader />;
  }

  return (
    <Routes>
      <Route path={PathConstants.NEWUSER} element={<NewUserDetailsForm />} />
      <Route
        path={PathConstants.STUDENT}
        element={<AuthenticationGuard component={MainLayout} />}
      >
        <Route path={PathConstants.HOME} element={<HomeContent />} />
        <Route path={PathConstants.COURSES} element={<CourseContent />} />
        <Route path={`${PathConstants.COURSES}/:course_id`} element={<AssignmentPage/>} />
        <Route path={`${PathConstants.COURSES}/:course_id/${PathConstants.ASSIGNMENT}/:assignment_id`} element={<WebGazerComponent component={AssignmentsDetailPage}/>}/>
        <Route path={PathConstants.FEEDBACK} element={<FeedbackContent />} />
        <Route path={PathConstants.SETTINGS} element={<SettingsContent />} />
        <Route path={PathConstants.ERROR} element={<FailedToLoadPage/>}/>
      </Route>
      <Route
        path={PathConstants.INSTRUCTOR}
        element={<AuthenticationGuard component={MainLayout} />}
      >
        <Route path={PathConstants.HOME} element={<HomeContent />} />
        <Route path={PathConstants.COURSES} element={<CourseContent />} />
        <Route path={`${PathConstants.COURSES}/:course_id`} element={<AssignmentPage/>} />
        <Route path={`${PathConstants.COURSES}/:course_id/${PathConstants.ASSIGNMENT}/:assignment_id`} element={<WebGazerComponent component={AssignmentsDetailPage}/>}/>
        <Route path={PathConstants.FEEDBACK} element={<FeedbackContent />} />
        <Route path={PathConstants.ERROR} element={<FailedToLoadPage/>}/>
        <Route
          path={PathConstants.SETTINGS}
          element={<div>Teacher Settings Component</div>}
        />
        <Route path={PathConstants.ERROR} element={<FailedToLoadPage/>}/>
      </Route>
      <Route
        path="/"
        element={<AuthenticationGuard component={RedirectComponent} />}
      />
      {/* <Route path={PathConstants.CALLBACK} element={<Callback/>} /> */}

      {/* Debug Routes for testing individual components */}
      {/* <Route path={"/testapploader"} element={<AppLoader/>} /> */}
    </Routes>
  );
}

export default App;
