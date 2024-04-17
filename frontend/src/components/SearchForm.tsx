import React from "react";
import { GridRow, OneHalfColumn } from "../Layout/Grid";
import { SearchRegAndLicence } from "../utils/Search";
type SearchFormProps = {
  searchError: string | null;
  setSearchError: React.Dispatch<React.SetStateAction<string | null>>;
  setData: React.Dispatch<React.SetStateAction<any[]>>;
  search: string;
  setSearch: React.Dispatch<React.SetStateAction<string>>;
  setEmptyResults: React.Dispatch<React.SetStateAction<boolean>>;
};
const SearchForm: React.FC<SearchFormProps> = ({
  searchError,
  setData,
  setSearchError,
  search,
    setSearch,
    setEmptyResults 
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setEmptyResults(false);
    if (search === "") {
      setSearchError("Please enter a search term");
      return;
    }
    SearchRegAndLicence(search)
      .then((response: any) => {
        if (response?.data !== undefined){
            if (response.data.length === 0) {
                setEmptyResults(true);
            }
        setData(response?.data);
        }else{
            setSearchError(response.error.message);
        }

      })
      .catch((error) => {
        setSearchError(error.message);
      });
  };
  return (
    <GridRow>
      <OneHalfColumn>
        <form onSubmit={handleSubmit}>
          <div
            className={`govuk-form-group govuk-!-margin-bottom-3 ${
              searchError ? "govuk-form-group--error" : null
            }`}
          >
            <label
              className="govuk-heading-s govuk-!-margin-bottom-2"
              htmlFor="search"
            >
              Search
            </label>
            {searchError && (
              <p id="full-name-input-error" className="govuk-error-message">
                <span className="govuk-visually-hidden">Error:</span>{" "}
                {searchError}
              </p>
            )}
            <p className="govuk-!-margin-1 govuk-secondary-text-colour">
              Enter a bus registration number or licence number.
            </p>
            <input
              className={`govuk-input ${searchError && "govuk-error-summary"}`}
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
    </GridRow>
  );
};

export default SearchForm;
