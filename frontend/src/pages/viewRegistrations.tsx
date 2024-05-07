import React, { useContext, useEffect, useState } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import { Link } from "react-router-dom";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";
import AccordionSection from "../components/AccordionSection";
import { initAll } from "../Javascript/govuk-frontend.min";
import useRegistrationStatus from "../utils/GetRegistrationStatus";
import { v4 as uuidv4 } from "uuid";
import GetAllRecords from "../utils/GetAllRecords";
import { fetchAuthSession } from "aws-amplify/auth";
import DataProccessingWaiting from "../components/DataProccessingWaiting";
import { AxiosError } from "axios";
const ViewRegistrations: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);
  const { data, loading, error } = useRegistrationStatus();
  // const { data, loading, error } = useGetAllRecords();
  const [ErrorMessage, setErrorMessage] = useState<string[]>([]);
  const [showError, setShowError] = useState(false);

  const ClickHandler = () => {
    fetchAuthSession()
      .then(() => {
        GetAllRecords()
          .then(() => {
            if (ErrorMessage.indexOf("The CSV has failed to download. Please retry the download process.") > -1) {
            setErrorMessage(
              ErrorMessage.filter(
                (message) =>
                  message !==
                  "The CSV has failed to download. Please retry the download process."
              )
            );
          }}
        )
          .catch((error) => {
            setShowError(true);
            let errorMsg = "";

             if(error.message === "User is not part of any local authority group."){
                errorMsg = "You must be assigned to a local authority group to download this CSV. You are currently not assigned to any local authority group. Please contact support admin."
             }
              if (error.message === "No records found") {
                errorMsg = "No records found";
              }
              if (error.message === "Failed to download CSV") {
                errorMsg = "The CSV has failed to download. Please retry the download process.";
              }
              errorMsg === "" ?? "The CSV has failed to download. Please retry the download process.";
            if (!ErrorMessage.includes(errorMsg)) {
              setErrorMessage([...ErrorMessage, errorMsg]);
            }
          });
      })
      .catch((error) => {
        const errorMsg = "Network error, please try again later";
        if (!ErrorMessage.includes(errorMsg)) {
          setErrorMessage([...ErrorMessage, errorMsg]);
        }
      });
  };

  useEffect(() => {
    if (ErrorMessage.length > 0) {
      setShowError(true);
    } else {
      setShowError(false);
    }
  }, [ErrorMessage]);
  useEffect(() => {
    if (data && data?.length > 0){
      initAll();
    }
  }, [data]);
  // useEffect(() => {
  // }, [loading]);
  useEffect(() => {
    if (error) {
      const errorObject = error as AxiosError<unknown, any>;
      const errorMsg =
        (errorObject.response?.data as any)?.detail ?? "Network error, please try again later";
      if (!ErrorMessage.includes(errorMsg)) {
        setErrorMessage([...ErrorMessage, errorMsg]);
      }
    }
  }, [error]);

  return (
    <>
      <FullColumnLayout
        title="View active registrations"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">View active registrations</h1>
        <a
          className="govuk-button--secondary govuk-button"
          onClick={ClickHandler}
        >
          Download CSV of all registrations
        </a>
        {showError && (
          <div
            className="govuk-error-summary"
            aria-labelledby="error-summary-title"
            role="alert"
            tabIndex={-1}
            data-module="error-summary"
          >
            <h2 className="govuk-error-summary__title" id="error-summary-title">
              There is a problem
            </h2>
            <div className="govuk-error-message">
              <ul className="govuk-list govuk-error-summary__list">
                {ErrorMessage.map((message: string, index: number) => {
                  return (
                    <li key={index}>
                      <a href="#">{message}</a>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        )}
        {!error && !data && (
          <DataProccessingWaiting
            title="Retrieving active registrations"
            description="Once registrations are ready they will be shown here"
          />
        )}
          { data && data.length === 0 && (
          <p className="govuk-body">There are no active registrations</p>
        )}
        {!loading && !error && data && (
          <div
            className="govuk-accordion"
            data-module="govuk-accordion"
            id="accordion-default"
          >
            {Object.entries(data).map(([key, value]) => {
              return (
                <AccordionSection
                  key={uuidv4()}
                  title={value.licence_number + " - " + value.operator_name}
                  serviceCount={value.total_services}
                  serviceRequiringAttentionCount={value.requires_attention}
                />
              );
            })}
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

export default ViewRegistrations;
