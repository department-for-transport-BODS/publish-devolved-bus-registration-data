import React, { Dispatch, createContext, useEffect, useState } from "react";
import { useAuthenticator } from "@aws-amplify/ui-react";
import {
  signIn,
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
  signOutHandler?: () => void;
};
export const IsLoggedInContext = createContext<UserLoggedIn>({
  signIn: signIn,
});
const CustomProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const cookies = new Cookies();
  const signOutHandler = () => {
    cookies.remove("stage_id")
    signOut();
    setIsLoggedIn(false);
    window.location.reload();
  };

  const { signOut } = useAuthenticator((context: { user: any }) => [
    context.user,
  ]);
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
      .catch((error) => {
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
