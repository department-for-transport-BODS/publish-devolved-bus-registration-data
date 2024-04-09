import React from "react"; // Import the 'React' module

import { getCurrentUser } from "aws-amplify/auth";
import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function RequireAuth({
  component: Component,
  ...rest
}: {
  component: React.ComponentType<any>;
}) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [state, setState] = useState("loading");
  const navigate = useNavigate();
  const location = useLocation();
  useEffect(() => {
    // Fetch user data from an API or perform any necessary logic here
    // For example:
    const fetchUserData = async () => {
      try {
        const user = await getCurrentUser();
        if (user) {
          setIsLoggedIn(true);
          setState("authenticated");
        }
      } catch (error) {
        // get current page
        // remove("/" from the location.pathname)
        const currentPath = location.pathname.substring(1);
        // window.location.replace("/login");
        navigate(`/login?to=${currentPath}`, {
          state: { error: "You are not logged in" },
        });
        console.error("Error fetching user data: ", error);
      }
    };

    fetchUserData();
  }, []);

  /* If in loading state, return loading message while waiting for 
        isValidToken to complete */
  if (state === "loading") {
    return null;
  }

  return <Component isLoggedIn={isLoggedIn} {...rest} />;
}

export default RequireAuth;
