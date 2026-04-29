import React, {  useContext} from "react";
import { TwoThirdsLayout } from "../components/layout/Layout";
import {IsLoggedInContext} from "../utils/login/LoginProvider";
import { config } from "../utils/Config";

const ContactUs: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);
  const ContactUsEmail = config.supportEmail
  const ContactUsPhone = config.supportPhone
  
  return (
    <>
      <TwoThirdsLayout title="Contact Us" description="Home" hideCookieBanner={true} isLoggedIn={isLoggedIn}>
        <h1 className="govuk-heading-xl">
        Contact the {config.serviceName.split(" ")
                          .slice(1)
                          .join(" ")} service team
        </h1>
        <p className="govuk-heading-m">
        Feedback and support 
        </p>
        <div className="govuk-!-font-size-19 govuk-!-margin-bottom-9">
        <p className="govuk-body">
        If you are experiencing technical issues, or if you have any suggestions, comments or criticisms, please contact the {config.serviceName.split(" ").slice(1).join(" ")} service team through one of the channels below.
        </p>
        <p className="govuk-body">
        The Help Desk is available Monday to Friday, 9am to 5pm <br />(excluding Bank Holidays in England and Wales, and the 24th of December).
        </p>
        <p className="govuk-body">
        The Help Desk can be contacted by telephone or email as follows.
        </p>
        <p className="govuk-body">
        Telephone: {ContactUsPhone}<br/>
        Email: <a href={`mailto:${ContactUsEmail}`}>{ContactUsEmail}</a> 
        </p>
        </div>
      </TwoThirdsLayout>
    </>
  );
};

export default ContactUs;