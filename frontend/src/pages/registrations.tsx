import React, { useContext } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import { Link } from "react-router-dom";
import {IsLoggedInContext} from "../utils/login/LoginProvider";
import  Footer  from "../Layout/Footer";
import { v4 as uuidv4 } from "uuid";
import { TITLE } from "../utils/Constants";
import Cookies from "universal-cookie";

const Registration: React.FC = () => {
  const {isLoggedIn } = useContext(IsLoggedInContext);
  const cookies = new Cookies();
  let LINKS = []
  const accessType = cookies.get("access-type")?? undefined
  if (accessType === "read-only") {
    LINKS = [
      {
        url: "/find-registered-services",
        text: "Find registered services",
      },
    ]
  }else{
 LINKS = [
  {
    url: "/upload-csv",
    text: "Upload a CSV of registered services",
  },
  {
    url: "/view-registrations",
    text: "View active registrations",
  }
]
  }
  
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