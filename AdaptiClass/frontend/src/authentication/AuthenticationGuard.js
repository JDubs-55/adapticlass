import { withAuthenticationRequired } from "@auth0/auth0-react";
import React from "react";
import { AppLoader } from "../pages/helperScreens/AppLoader";

export const AuthenticationGuard = ({ component }) => {
  const Component = withAuthenticationRequired(component, {
    onRedirecting: () => (
      <div className="page-layout">
        <AppLoader />
      </div>
    ),
  });

  return <Component />;
};