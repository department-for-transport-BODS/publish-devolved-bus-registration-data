import React, { useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import HelpAndSupport from "../components/HelpAndSupport";
import { Link } from "react-router-dom";
import { TITLE } from "../utils/contants";
import Footer from "../Layout/Footer";
import { v4 as uuidv4 } from "uuid";
import {
  TwoThirdsColumn,
  FullColumn,
  GridRow,
  OneThirdColumn,
  OneHalfColumn,
} from "../Layout/Grid";
import {SearchRegAndLicence} from "../utils/Search";

const FindRegisteredServices: React.FC = () => {
  const [searchError, setSearchError] = React.useState<string | null>(null);
  const [search, setSearch] = React.useState<string>("");
  const [data , setData] = React.useState<any[]>([]);
  const [showData, setShowData] = React.useState<boolean>(false);
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (search === "") {
      setSearchError("Please enter a search term");
      return;
    }
    SearchRegAndLicence(search).then((response:any) => {
      console.log("Changing data")
      console.log(response);
      setData(response?.data);
    }).catch((error) => {
      setSearchError(error.message);
    });
  };
  useEffect(() => {
  if (!/^[a-zA-Z0-9///]*$/.test(search)) {
      setSearchError("Invalid search input");
  }else{
    setSearchError(null);}
  },[search]);
  useEffect(() => {
    if (data){
    if (data.length > 0) {
      setShowData(true);
    }
    console.log(showData)
  }
  }, [data]);
  return (
    <>
      <FullColumnLayout
        title="Search"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={true}
      >
        <h1 className="govuk-heading-xl">Find a registered bus service</h1>
        {searchError && (
          <div
            className="govuk-error-summary"
            aria-labelledby="error-summary-title"
            role="alert"
            tabIndex={-1}
          >
            <h2 className="govuk-error-summary__title" id="error-summary-title">
              There is a problem
            </h2>
            <div className="govuk-error-summary__body">
              <ul className="govuk-list govuk-error-summary__list">
                <li>
                  <a href="#search">{searchError}</a>
                </li>
              </ul>
            </div>
          </div>
        )}


        <OneHalfColumn>
          <form onSubmit={handleSubmit}>
            <div
              className={`govuk-form-group govuk-!-margin-bottom-3 ${
                searchError ? "govuk-form-group--error" : null
              }`}
            >
              <label
                className="govuk-heading-s govuk-!-margin-bottom-2"
                htmlFor="email"
              >
                Search
              </label>
              {searchError && (
                <p id="full-name-input-error" className="govuk-error-message">
                  <span className="govuk-visually-hidden">Error:</span>{" "}
                  {searchError}
                </p>
              )}
              <p className="govuk-!-margin-1 govuk-secondary-text-colour">Enter a bus registration number or licence number.</p>
              <input
                className={`govuk-input ${ searchError && "govuk-error-summary"}`}
                id="search"
                name="search"
                type="text"
                spellCheck="false"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <button
              type="submit"
              className="govuk-button"
              data-module="govuk-button"
            >
              Search
            </button>
          </form>
        </OneHalfColumn>
        {showData && (
          <div className="govuk-!-margin-top-5">
            <h2 className="govuk-heading-l">Results</h2>
            <table className="govuk-table">
              <thead className="govuk-table__head">
                <tr className="govuk-table__row">
                  <th scope="col" className="govuk-table__header">
                    Registration number
                    </th>
                      <th scope="col" className="govuk-table__header">
                        Operator name
                        </th>
                    <th scope="col" className="govuk-table__header">
                      Service number
                      </th>
                        <th scope="col" className="govuk-table__header">
                          Licence status
                          </th>
                    </tr>
                    </thead>
                    <tbody className="govuk-table__body">
                      {data.map((item) => (
                        <tr className="govuk-table__row" key={uuidv4()}>
                          <td className="govuk-table__cell">{item.registrationNumber}</td>
                          <td className="govuk-table__cell">{item.operatorName}</td>
                          <td className="govuk-table__cell">{item.registrationNumber.split("/")[1]}</td>
                          <td className="govuk-table__cell">{item.licenceStatus}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
      </FullColumnLayout>

      <Footer />
    </>
  );
};

export default FindRegisteredServices;
