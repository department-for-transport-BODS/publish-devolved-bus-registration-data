import React, {  useContext, useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import HelpAndSupport from "../components/HelpAndSupport";
import { Link } from "react-router-dom";
import {IsLoggedInContext} from "../utils/login/LoginProvider";
import  Footer  from "../Layout/Footer";


import {initAll} from "../Javascript/govuk-frontend.min";

const Registration: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);
  // const isLoggedIn = IsLoggedInContext;
  const [isLoaded, setIsLoaded] = React.useState(false); 
  useEffect(() => {
    initAll();
  }, []);
  
  return (
    <>
      <FullColumnLayout title="Home" description="Home" hideCookieBanner={true} isLoggedIn={isLoggedIn}>
        <h1 className="govuk-heading-xl">
          Enhanced Partnerships Registration tool 
        </h1>

        <Link className="govuk-button--secondary govuk-button" to="">
          Download CSV of all registrations
        </Link>

      
        <div className="govuk-accordion" data-module="govuk-accordion" id="accordion-default">
  <div className="govuk-accordion__section">
      <div className="">
    <div className="govuk-accordion__section-header">

      <h2 className="govuk-accordion__section-heading">
        <span className="govuk-accordion__section-button" id="accordion-default-heading-1">
        PC2021320  - GO NORTH WEST LIMITED 
        </span>
      </h2>
        <span className="app-swatch" style={{ backgroundColor: "#1d70b8" }}> </span>
    </div>
      </div>
    <div id="accordion-default-content-1" className="govuk-accordion__section-content">
      <p className="govuk-body">This is the content for Writing well for the web.</p>
    </div>
  </div>
</div>
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default Registration;