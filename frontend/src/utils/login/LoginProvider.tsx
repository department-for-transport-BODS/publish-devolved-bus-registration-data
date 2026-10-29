import React, { Dispatch, createContext, useEffect, useState } from "react";
import {
  signIn,
  signOut,
  type SignInInput,
  getCurrentUser,
  SignInOutput,
} from "aws-amplify/auth";
import Cookies from "universal-cookie";
export type UserLoggedIn = {
  isLoggedIn?: boolean;
  setIsLoggedIn?: Dispatch<boolean>;
  signOut?: () => void;
  signIn: (input: SignInInput) => Promise<SignInOutput>;
  signOutHandler?: () => Promise<void>;
};
export const IsLoggedInContext = createContext<UserLoggedIn>({
  signIn: signIn,
});
const CustomProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const cookies = new Cookies();
  const signOutHandler = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error("Sign out failed", error);
    } finally {
      cookies.remove("stage_id");
      cookies.remove("access-type");
      setIsLoggedIn(false);
      window.location.reload();
    }
  };

  const userLoggedIN = {
    isLoggedIn: isLoggedIn,
    setIsLoggedIn: setIsLoggedIn,
    signOutHandler: signOutHandler,
    signIn: signIn,
  };

  useEffect(() => {
    getCurrentUser()
      .then(() => {
        setIsLoggedIn(true);
      })
      .catch((_error) => {
        setIsLoggedIn(false);
      });
  }, []);
  return (
    <IsLoggedInContext.Provider value={userLoggedIN}>
      {children}
    </IsLoggedInContext.Provider>
  );
};

export default CustomProvider;
