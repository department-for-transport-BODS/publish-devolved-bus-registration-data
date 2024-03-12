import React, {  useContext, useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import HelpAndSupport from "../components/HelpAndSupport";
import { Link } from "react-router-dom";
import {IsLoggedInContext} from "../utils/login/LoginProvider";
import  Footer  from "../Layout/Footer";



const Registration: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);
  // const isLoggedIn = IsLoggedInContext;
  // useEffect(() => {
  //     console.log("Is logged in", isLoggedIn);
  //     // }
  //     }
  // , []);
  
  return (
    <>
      <FullColumnLayout title="Home" description="Home" hideCookieBanner={true} isLoggedIn={isLoggedIn}>
        <h1 className="govuk-heading-xl">
          Enhanced Partnerships Registration tool 
        </h1>

        <Link to="/uploadcsv" className="govuk-link govuk-heading-m">
          Upload a CSV of registered services
        </Link>
        <br />
        <Link to="/view-registrations" className="govuk-link govuk-heading-m">
          View active registrations
        </Link>
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default Registration;