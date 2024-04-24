import React, { useEffect } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import Footer from "../Layout/Footer";
import RegistrationDetails from "./RegistrationDetails";
import { GridRow, OneHalfColumn } from "../Layout/Grid";
import SearchForm from "../components/SearchForm";
import SearchResults from "../components/SearchResults";
import SearchErrorBox from "../components/SearchErrorBox";
import NotificationBanner from "../components/NotificationBanner";

const FindRegisteredServices: React.FC = () => {
  const [searchError, setSearchError] = React.useState<string | null>(null);
  const [search, setSearch] = React.useState<string>("");
  const [data, setData] = React.useState<any[]>([]);
  const [showData, setShowData] = React.useState<boolean>(false);
  const [emptyResults, setEmptyResults] = React.useState<boolean>(false);
  const [showRegistrationDetails, setShowRegistrationDetails] =
    React.useState<boolean>(false);
  const [idx, setIdx] = React.useState<number>(0);
  useEffect(() => {
    if (!/^[a-zA-Z0-9///]*$/.test(search)) {
      setSearchError("Invalid search input");
    } else {
      setSearchError(null);
    }
  }, [search]);
  useEffect(() => {
    if (data.length > 0) {
      setShowData(true);
    }
  }, [data]);
  const handleRegistrationClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setIdx(parseInt(e.currentTarget.getAttribute("data-idx") || "0", 10));
    setShowRegistrationDetails(true);
  };
  return (
    <>
      <FullColumnLayout
        title="Search"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={true}
      >
        <h1 className="govuk-heading-xl">
          {showRegistrationDetails
            ? "Bus registration details"
            : "Find a registered bus service"}
        </h1>
        {showRegistrationDetails && (
          <RegistrationDetails
            registration={data[idx]}
            setShowRegistationDetails={setShowRegistrationDetails}
          />
        )}
        {searchError && <SearchErrorBox searchError={searchError} />}
        {!showRegistrationDetails && (
          <SearchForm
            searchError={searchError}
            setSearchError={setSearchError}
            setData={setData}
            search={search}
            setSearch={setSearch}
            setEmptyResults={setEmptyResults}
          />
        )}
        {!showRegistrationDetails && !emptyResults && showData && (
          <SearchResults
            data={data}
            handleRegistrationClick={handleRegistrationClick}
          />
        )}
        {emptyResults && (
          <GridRow>
            <OneHalfColumn>
              <NotificationBanner message="No results found" header="" />
            </OneHalfColumn>
          </GridRow>
        )}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default FindRegisteredServices;
