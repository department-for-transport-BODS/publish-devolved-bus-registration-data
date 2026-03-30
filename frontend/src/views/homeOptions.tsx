import React, { useContext } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import { Link } from "react-router-dom";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";
import { v4 as uuidv4 } from "uuid";
import { TITLE } from "../utils/Constants";
const HomeOptions: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);
    const LINKS = [
      {
        url: "/find-registered-services",
        text: "Find registered services",
      },
      {
        url: "/login",
        text: "Login to publish registrations",
      },
    ];

  return (
    <>
      <FullColumnLayout
        title="Home page options"
        description="Options"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">{TITLE}</h1>
        {LINKS.map((value) => {
          return (
            <Link
              to={value.url}
              className="govuk-link govuk-heading-m govuk-!-margin-bottom-7"
              key={uuidv4()}
            >
              {value.text}
            </Link>
          );
        })}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default HomeOptions;
