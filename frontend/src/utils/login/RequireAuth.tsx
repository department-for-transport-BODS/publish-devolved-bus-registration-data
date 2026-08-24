import React from "react"; // Import the 'React' module

import { getCurrentUser } from "aws-amplify/auth";
import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

function RequireAuth({
  component: Component,
  requiredAccess: _requiredAccess,
}: {
  component: React.ComponentType<{ isLoggedIn?: boolean }>;
  requiredAccess?: string;
}) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [state, setState] = useState("loading");
  const navigate = useNavigate();
  const location = useLocation();
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const user = await getCurrentUser();
        if (user) {
            setIsLoggedIn(true);
            setState("authenticated");
        }
      } catch (error) {
        const currentPath = location.pathname.substring(1);
        navigate(`/login?to=${currentPath}`, {
          state: { error: "You are not logged in" },
        });
        console.error("Error fetching user data: ", error);
      }
    };

    fetchUserData();
  }, [location.pathname, navigate]);

  if (state === "loading") {
    return null;
  }

  return <Component isLoggedIn={isLoggedIn} />;
}

export default RequireAuth;
