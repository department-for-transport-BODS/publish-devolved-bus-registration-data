import React, {  useContext, useEffect, useState } from "react";
import { FullColumnLayout, TwoThirdsLayout } from "../Layout/Layout";
import HelpAndSupport from "../components/HelpAndSupport";
import { Link } from "react-router-dom";
import {IsLoggedInContext} from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";



const ContactUs: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);


  
  return (
    <>
      <TwoThirdsLayout title="Home" description="Home" hideCookieBanner={true} isLoggedIn={isLoggedIn}>
        <h1 className="govuk-heading-xl">
        Contact the Enhanced Partnerships Service team
        </h1>
        <p className="govuk-heading-m">
        Feedback and support 
        </p>
        <div className="govuk-!-font-size-19 govuk-!-margin-bottom-9">
        <p className="">
        If you are experiencing technical issues, or if you have any suggestions, comments or criticisms, please contact the Enhanced Partnerships Service team through one of the channels below.
        </p>
        <p>
        The Help Desk is available Monday to Friday, 9am to 5pm <br />(excluding Bank Holidays in England and Wales, and the 24th of December).
        </p>
        <p>
        The Help Desk can be contacted by telephone or email as follows.
        </p>
        <p>
        Telephone: 0800 028 0930<br/>
        Email: <a href="mailto:bodshelpdesk@kpmg.co.uk">bodshelpdesk@kpmg.co.uk</a> 
        </p>
        </div>
      </TwoThirdsLayout>
      <Footer />
    </>
  );
};

export default ContactUs;