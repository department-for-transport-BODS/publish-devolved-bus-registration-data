import React, { useContext } from "react";
import { TwoThirdsLayout } from "../Layout/Layout";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";

const AccessibilityStatement: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);
  const APP_URL = process.env.REACT_APP_URL;

  return (
    <>
      <TwoThirdsLayout
        title="Accessibility Statement"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">Accessibility Statement</h1>
        <div className="govuk-!-font-size-19">
          <p>
            This statement applies to pages on{" "}
            <a href={`https://${APP_URL}`}>{APP_URL}</a>. <br /> <br />
            This website is run by the Department for Transport. The text should
            be clear and simple to understand. You should be able to:
          </p>
          <ul>
            <li>Zoom in up to 300% without problems</li>
            <li>
              Navigate all of the website using just a keyboard (except for maps
              which are not essential to the functionality)
            </li>
            <li>
              Navigate all of the website using speech recognition software
            </li>
            <li>
              Use all of the website using a screen reader (including the most
              recent versions of JAWS, NVDA and VoiceOver)
            </li>
            <li>
              Interpret page information through access technology due to a
              consistent heading structure
            </li>
            <li>Use all of the functionality with Javascript turned off</li>
            <li>
              Access the site and use the associated services with Google
              Chrome, Internet Explorer, Safari, Opera, Firefox, and Edge
            </li>
          </ul>
          <p className="govuk-heading-m">
            Reporting accessibility problems with this website
          </p>
          <p>
            We&apos;re always looking to improve the accessibility of this
            website. If you find any problems that are not listed on this page
            or you think we&apos;re not meeting the accessibility requirements,
            contact:{" "}
            <a href="mailto:BusOpenData@dft.gov.uk">BusOpenData@dft.gov.uk</a>
          </p>
          <p className="govuk-heading-m">Enforcement procedure</p>
          <p>
            The Equality and Human Rights Commission (EHRC) is responsible for
            enforcing the Public Sector Bodies (Websites and Mobile
            Applications) (No. 2) Accessibility Regulations 2018 (the
            &apos;accessibility regulations&apos;). If you&apos;re not happy
            with how we respond to your complaint,{" "}
            <a href="https://www.equalityadvisoryservice.com/">
              contact the Equality Advisory and Support Service (EASS).
            </a>
          </p>
          <p>
            Technical information about this website&apos;s accessibility
            Department for Transport is committed to making its websites
            accessible, in accordance with the Public Sector Bodies (Websites
            and Mobile Applications) (No. 2) Accessibility Regulations 2018.
          </p>
          <p className="govuk-heading-m">Compliance status</p>
          <p>
            This website follows the{" "}
            <a href="https://www.w3.org/TR/WCAG21/">
              Web Content Accessibility Guidelines version 2.1
            </a>{" "}
            AA standard.
          </p>
          <p className="govuk-heading-m">
            Preparation of this accessibility statement
          </p>
          <p>
            This statement was prepared on 19 March 2024. It was last reviewed
            on 19 March 2024.
          </p>
        </div>
      </TwoThirdsLayout>
      <Footer />
    </>
  );
};

export default AccessibilityStatement;
