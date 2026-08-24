import React from "react";

type SearchErrorBoxProps = {
  searchError: string | null;
};
const SearchErrorBox: React.FC<SearchErrorBoxProps> = ({ searchError }) => {
  return (
    <>
        <div
          className="govuk-error-summary"
          aria-labelledby="error-summary-title"
          role="alert"
          tabIndex={-1}
          data-module="govuk-error-summary"
        >
          <h2 className="govuk-error-summary__title" id="error-summary-title">
            There is a problem
          </h2>
          <div className="govuk-error-summary__body">
            <ul className="govuk-list govuk-error-summary__list">
              <li>
                <a href="#search" className="govuk-link">
                  {searchError}
                </a>
              </li>
            </ul>
          </div>
        </div>
    </>
  );
};

export default SearchErrorBox;
