import React, { useContext, useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import { Link } from "react-router-dom";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";
import AccordionSection from "../components/AccordionSection";
import { initAll} from "../Javascript/govuk-frontend.min";
import useRegistrationStatus from "../utils/GetRegistrationStatus";
import { v4 as uuidv4 } from "uuid";
import  GetAllRecords  from "../utils/GetAllRecords";
import {fetchAuthSession} from "aws-amplify/auth";
const Registration: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);
  const { data, loading, error } = useRegistrationStatus();
  // const { data, loading, error } = useGetAllRecords();
 
const ClickHandler = () => {
  console.log("clicked");
  fetchAuthSession().then(() => {
    GetAllRecords();
  }).catch((error) => {
    console.log("error: ", error);
  });
}



  useEffect(() => {
    console.log(data)
      initAll();
  }, [data]);

  // useEffect(() => {
  // }, []);


  return (
    <>
      <FullColumnLayout
        title="View active registrations"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">
          View active registrations
        </h1>
        <a className="govuk-button--secondary govuk-button" onClick={ClickHandler}>
          Download CSV of all registrations
        </a>
        
        {!loading && !error && data && (
          <div
          className="govuk-accordion"
          data-module="govuk-accordion"
          id="accordion-default"
          >
            {
          Object.entries(data).map(([key, value]) => {
          return (
            <AccordionSection
              key={uuidv4()}
              title={value.licence_number + " - " + value.operator_name}
              serviceCount={value.total_services}
              serviceRequiringAttentionCount={value.requires_attention}
              status={value.licence_status}
            />

          );
        })
      }
        
          </div>
        )}
        <Link className="govuk-button--secondary govuk-button" to="/">
          Return home
        </Link>
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default Registration;
