"use client";

import { useEffect, useState } from "react";
import { Authenticator } from "@aws-amplify/ui-react";
import App from "../App";
import CustomProvider from "../utils/login/LoginProvider";

export default function AppClient() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }

  return (
    <Authenticator.Provider>
      <CustomProvider>
        <App />
      </CustomProvider>
    </Authenticator.Provider>
  );
}