import React from "react";
import "../Css/App.css";
import Footer from "../Layout/Footer";
import { FullColumnLayout } from "../Layout/Layout";
import HelpAndSupport from "../components/HelpAndSupport";
import { useContext } from "react";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import { useLocation } from "react-router-dom";
import { TITLE } from "../utils/Constants";

const ErrorPage: React.FC = () => {
  const location = useLocation();
  const Error = location.state;
  const { isLoggedIn } = useContext(IsLoggedInContext);

  return (
    <>
      <FullColumnLayout
        title="Home"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">
          {TITLE} tool
        </h1>
        <div>
          <div
            className="govuk-notification-banner"
            role="region"
            aria-labelledby="govuk-notification-banner-title"
            data-module="govuk-notification-banner"
          >
            <div className="govuk-notification-banner__header">
              <h2
                className="govuk-notification-banner__title"
                id="govuk-notification-banner-title"
              >
                Error!
              </h2>
            </div>
            <div className="govuk-notification-banner__content">
          <div
            className="govuk-exit-this-page"
            data-module="govuk-exit-this-page"
          >
            <a
              href="/"
              role="button"
              draggable="false"
              className="govuk-button govuk-button--warning govuk-exit-this-page__button govuk-js-exit-this-page-button"
              data-module="govuk-button"
              rel="nofollow noreferrer"
            >
              <span className="govuk-visually-hidden">Emergency</span> Exit this
              page
            </a>
          </div>
              <p className="govuk-notification-banner__heading">
                Something went wrong, please try again later.
              </p>
            </div>
          </div>
        </div>
        <HelpAndSupport />
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default ErrorPage;
