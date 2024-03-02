import React, { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import PathConstants from '../routes/pathConstants';

const Callback = () => {
  const { isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
  const navigate = useNavigate();

  useEffect(() => {
    const handleRedirectCallback = async () => {
      if (!isAuthenticated && !isLoading && !error) {
        try {
          // Retrieve the access token silently
          await getAccessTokenSilently();
        } catch (error) {
          console.error('Error retrieving access token:', error);
          navigate(PathConstants.HOME);
        }
      }
    };

    handleRedirectCallback();
  }, [isAuthenticated, isLoading, error, getAccessTokenSilently, navigate]);

  return (
    <div>
      {isLoading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
};

export default Callback;