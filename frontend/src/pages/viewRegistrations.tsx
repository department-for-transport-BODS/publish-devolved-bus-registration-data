import React, { useContext, useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import { Link } from "react-router-dom";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";
import AccordionSection from "../components/AccordionSection";
import { initAll} from "../Javascript/govuk-frontend.min";

const Registration: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);
  useEffect(() => {
    initAll();
  }, []);

  return (
    <>
      <FullColumnLayout
        title="Home"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">
          View active registrations
        </h1>
        <Link className="govuk-button--secondary govuk-button" to="">
          Download CSV of all registrations
        </Link>
        <div
          className="govuk-accordion"
          data-module="govuk-accordion"
          id="accordion-default"
        >
        <AccordionSection
          title="OTC License Number - Operator Name"
          serviceCount={62}
          serviceRequiringAttentionCount={50}
          status="Registered"
        />
        </div>
        <Link className="govuk-button--secondary govuk-button" to="/">
          Return home
        </Link>
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default Registration;
