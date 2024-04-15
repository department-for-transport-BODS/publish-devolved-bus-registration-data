import React, {  useContext, useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import HelpAndSupport from "../components/HelpAndSupport";
import { Link } from "react-router-dom";
import {IsLoggedInContext} from "../utils/login/LoginProvider";
import  Footer  from "../Layout/Footer";
import { v4 as uuidv4 } from "uuid";
import { TITLE } from "../utils/contants";

const Registration: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);
  // const isLoggedIn = IsLoggedInContext;
  // useEffect(() => {
  //     console.log("Is logged in", isLoggedIn);
  //     // }
  //     }
  // , []);
  const LINKS = [
  {
    url: "/upload-csv",
    text: "Upload a CSV of registered services",
  },
  {
    url: "/view-registrations",
    text: "View active registrations",
  },
  {
    url: "/find-registered-services",
    text: "Find registered services",
  },
]
  
  return (
    <>
      <FullColumnLayout title="Registrations" description="Home" hideCookieBanner={true} isLoggedIn={isLoggedIn}>
        <h1 className="govuk-heading-xl">
          {TITLE} 
        </h1>
        {LINKS.map((value) => {
          return (
              <Link to={value.url} className="govuk-link govuk-heading-m govuk-!-margin-bottom-7" key={uuidv4()}>
                {value.text}
              </Link>
          );
        })}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default Registration;