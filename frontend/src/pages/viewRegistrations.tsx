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
const Registration: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);
  const { data, loading, error } = useRegistrationStatus();
  // const { data, loading, error } = useGetAllRecords();
  const [CSVDownloadError, setCSVDownloadError] = useState<string | null>(null);
  const [showError, setShowError] = useState(false);

  const ClickHandler = () => {
    console.log("clicked");
    fetchAuthSession()
      .then(() => {
        GetAllRecords()
          .catch((error) => {
            console.log("error: ", error);
            setShowError(true);
            setCSVDownloadError(
              "The CSV has failed to download. Please retry the download process."
            );
          });
      })
      .catch((error) => {
        console.log("error: ", error);
      });
  };

  useEffect(() => {
    if (showError) {
      console.log("error!!");
      setCSVDownloadError(
        "The CSV has failed to download. Please retry the download process."
      );
    }
  }, [showError]);

  useEffect(() => {
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
                <li>
                  <a href="#">{CSVDownloadError}</a>
                </li>
              </ul>
            </div>
          </div>
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
                  status={value.licence_status}
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

export default Registration;
