import React, { useContext } from "react";
import { TwoThirdsLayout } from "../Layout/Layout";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";

const CookiePage: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);

  return (
    <>
      <TwoThirdsLayout
        title="Cookie Policy"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">
          Cookies on the Registrations portal
        </h1>
        <div className="govuk-!-font-size-19">
          <p>
            Cookies are fiels saved on your phone, tablet or computer when you
            visit a website.
          </p>
          <p>
            We only use essential cookies on this website. These cookies are to
            make this site work.
          </p>
          <p className="govuk-heading-m">Essential cookies</p>
          <p>
            Essential cookies keep your information secure while you use this
            service. We do nt need to ask permission to use them.
          </p>

          <table className="govuk-table">
            <thead className="govuk-table__head">
              <tr className="govuk-table__row">
                <th
                  scope="col"
                  className="govuk-table__header app-custom-class"
                >
                  Name
                </th>
                <th
                  scope="col"
                  className="govuk-table__header app-custom-class"
                >
                  Purpose
                </th>
                <th
                  scope="col"
                  className="govuk-table__header app-custom-class"
                >
                  Expires
                </th>
              </tr>
            </thead>
            <tbody className="govuk-table__body">
              <tr className="govuk-table__row">
                <td scope="row" className="govuk-table__cell">
                  session_cookie
                </td>
                <td className="govuk-table__cell">
                  Used to keep you signed in
                </td>
                <td className="govuk-table__cell">20 minutes</td>
              </tr>
            </tbody>
          </table>
        </div>
      </TwoThirdsLayout>
      <Footer />
    </>
  );
};

export default CookiePage;
