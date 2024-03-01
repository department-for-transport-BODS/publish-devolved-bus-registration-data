import { useState, useEffect, useCallback } from "react";
import { AuthUser } from "@aws-amplify/auth";
import { getCurrentUser } from "aws-amplify/auth";
const useUser = () => {
  const [userData, setUserData] = useState({} as AuthUser);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  useEffect(() => {
    const fetchUserData = async () => {
      const fetchUserData = async () => {
        try {
          const user = await getCurrentUser();
          if (user) {
            setUserData(user);
            setIsLoggedIn(true);
          }
        } catch (error) {
          window.location.replace("/login");
          console.error("Error fetching user data:", error);
        }
      };

      fetchUserData();
    };

    fetchUserData();
  }, []);

  const login = useCallback(() => window.location.replace("/login"), []);

  return { userData, isLoggedIn, login };
};

export default useUser;
