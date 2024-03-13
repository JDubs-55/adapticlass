import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import axios from "axios";
import PathConstants from "../routes/pathConstants";
import { useAuth0 } from "@auth0/auth0-react";
import { AppLoader } from "../pages/AppLoader";

const RedirectComponent = () => {
  const { isAuthenticated, user } = useAuth0();
  const [userRole, setUserRole] = useState(null);
  const [redirectComponent, setRedirectComponent] = useState(null);

  useEffect(() => {
    if (isAuthenticated) {
      axios
        .get(`http://127.0.0.1:8000/users/${user.sub}/`)
        .then((response) => {
          if (response.status === 200 && response.data) {
            const role = response.data["role"];
            setUserRole(role);

            if (userRole === "student") {
              setRedirectComponent(<Navigate to={PathConstants.STUDENT} />);
            } else if (userRole === "instructor") {
              setRedirectComponent(<Navigate to={PathConstants.INSTRUCTOR} />);
            } else {
              console.error(
                `Unable to navigate to user login for role: ${role}`,
                response.status,
                response.data
              );
            }
          } else {
            console.error(
              "Unexpected response:",
              response.status,
              response.data
            );
          }
        })
        .catch(function (error) {
          if (error.response.status === 404) {
            // Redirect to new user page
            setRedirectComponent(<Navigate to={PathConstants.NEWUSER} />);
          } else {
            console.error("Error getting user information", error);
          }
        });
    }
  }, [isAuthenticated, user, userRole]); // Add dependencies as needed

  if (!isAuthenticated) {
    return <AppLoader />;
  }

  return redirectComponent;
};

export default RedirectComponent;
