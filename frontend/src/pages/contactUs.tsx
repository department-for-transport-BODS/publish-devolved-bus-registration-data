import React, {  useContext} from "react";
import { TwoThirdsLayout } from "../Layout/Layout";
import {IsLoggedInContext} from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";
import { TITLE } from "../utils/Constants";


const ContactUs: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);
  const ContactUsEmail = process.env.REACT_APP_SUPPORT_EMAIL
  const ContactUsPhone = process.env.REACT_APP_SUPPORT_PHONE

  
  return (
    <>
      <TwoThirdsLayout title="Contact Us" description="Home" hideCookieBanner={true} isLoggedIn={isLoggedIn}>
        <h1 className="govuk-heading-xl">
        Contact the {TITLE.split(" ")
                          .slice(1)
                          .join(" ")} service team
        </h1>
        <p className="govuk-heading-m">
        Feedback and support 
        </p>
        <div className="govuk-!-font-size-19 govuk-!-margin-bottom-9">
        <p className="">
        If you are experiencing technical issues, or if you have any suggestions, comments or criticisms, please contact the {TITLE.split(" ").slice(1).join(" ")} service team through one of the channels below.
        </p>
        <p>
        The Help Desk is available Monday to Friday, 9am to 5pm <br />(excluding Bank Holidays in England and Wales, and the 24th of December).
        </p>
        <p>
        The Help Desk can be contacted by telephone or email as follows.
        </p>
        <p>
        Telephone: {ContactUsPhone}<br/>
        Email: <a href={`mailto:${ContactUsEmail}`}>{ContactUsEmail}</a> 
        </p>
        </div>
      </TwoThirdsLayout>
      <Footer />
    </>
  );
};

export default ContactUs;