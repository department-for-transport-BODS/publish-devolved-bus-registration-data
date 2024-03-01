import React, {  useContext, useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import HelpAndSupport from "../components/HelpAndSupport";
import { Link } from "react-router-dom";
import {IsLoggedInContext} from "../utils/login/LoginProvider";



const Home: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);
  // const isLoggedIn = IsLoggedInContext;
  useEffect(() => {
      console.log("Is logged in", isLoggedIn);
      // }
      }
  , []);
  
  return (
    <>
      <FullColumnLayout title="Home" description="Home" hideCookieBanner={true} isLoggedIn={isLoggedIn}>
        <h1 className="govuk-heading-xl">
          Enhanced Partnerships Registration tool
        </h1>
        <p className="govuk-body">
          This service is for uploading enhanced partnership registrations data
          for public transport services, excluding rail, in England.
        </p>
        <div>
          <p>The service can be used by:</p>
          <ul className="govuk-list govuk-list--bullet govuk-!-margin-left-2">
            <li>Enhanced partnerships in England</li>
            <li>Franchises in England</li>
          </ul>
        </div>
        <div>
          <p>Use this service to:</p>
          <ul className="govuk-list govuk-list--bullet govuk-!-margin-left-2">
            <li>Register enhanced partnership bus</li>
            <li>View enhanced partnerships registered services</li>
          </ul>
        </div>
        <div>
          <Link
            to={isLoggedIn ? "/uploadcsv" : "/login"}
            className="govuk-button govuk-button--start"
            data-module="govuk-button"
          >
            Start now
            <svg
              className="govuk-button__start-icon"
              xmlns="http://www.w3.org/2000/svg"
              width="17.5"
              height="19"
              viewBox="0 0 33 40"
              aria-hidden="true"
              focusable="false"
            >
              <path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" />
            </svg>
          </Link>
        </div>
        <HelpAndSupport />
      </FullColumnLayout>
    </>
  );
};

export default Home;