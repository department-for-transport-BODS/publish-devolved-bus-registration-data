import React, { useContext, useEffect, useState, useMemo, useRef } from "react";
import { FullColumnLayout } from "../Layout/Layout";
import { Link } from "react-router-dom";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";
import PreValidationAccordionSection from "../components/PreValidationAccordionSection";
import { initAll } from "../Javascript/govuk-frontend.min";
import { v4 as uuidv4 } from "uuid";
import { useLocation, useNavigate } from "react-router-dom";
import {
  CommitRegistrations,
  DiscardRegistrations,
  GetReport,
} from "../utils/SendCsv";
import Cookies from "universal-cookie";

type buttonRef = { current: null | HTMLButtonElement };
const PreValidations: React.FC = () => {
  const discardRef: buttonRef = useRef(null);
  const commitRef: buttonRef = useRef(null);
  const { isLoggedIn } = useContext(IsLoggedInContext);
  const [ErrorMessage, setErrorMessage] = useState<string[]>([]);
  const [showError, setShowError] = useState(false);
  const [error, setError] = useState<null | string>(null);
  const [loading, setLoading] = useState(false);
  const [recordsCommitted, setRecordsCommitted] = useState(false);
  const [recordsDiscarded, setRecordsDiscarded] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state?.data;
  const memoData = useMemo(() => {
    return data;
  }, [data]);

  const handleCommitRegistrations = async (e: any) => {
    e.preventDefault();
    if (commitRef.current && !commitRef.current.disabled) {
      commitRef.current.disabled = true;
      const localCookies = new Cookies();
      const stage_id = localCookies.get("stage_id");
      if (!stage_id) {
        setErrorMessage(["No stage_id found"]);
        return;
      }
      CommitRegistrations(stage_id)
        .then(() => {
          localCookies.remove("stage_id");
          setRecordsCommitted(true);
          GetReport(stage_id, navigate);
        })
        .catch((error) => {
          setErrorMessage(["Error committing registrations"]);
        });
    }
  };

  const handleDiscardRegistrations = async (e: any) => {
    e.preventDefault();
    if (discardRef.current && !discardRef.current.disabled) {
      discardRef.current.disabled = true;
      const localCookies = new Cookies();
      const stage_id = localCookies.get("stage_id");
      DiscardRegistrations(stage_id)
        .then(() => {
          localCookies.remove("stage_id");
          setRecordsDiscarded(true);
          navigate("/upload-csv", { replace: true });
        })
        .catch((error) => {
          setErrorMessage(["Error discarding registrations"]);
        });
    }
  };

  useEffect(() => {
    if (ErrorMessage.length > 0) {
      setShowError(true);
    } else {
      setShowError(false);
    }
  }, [ErrorMessage]);
  useEffect(() => {
    initAll();
    if (!data) {
      setError("No data found");
    }
  }, [data]);
  useEffect(() => {
    if (error) {
      const errorMsg = error;
      if (!ErrorMessage.includes(errorMsg)) {
        setErrorMessage([...ErrorMessage, errorMsg]);
      }
    }
  }, [error]);

  return (
    <>
      <FullColumnLayout
        title="View active registrations"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">
          Please verify all new expected registrations are correct before
          uploading
        </h1>
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
                {ErrorMessage.map((message: string, index: number) => {
                  return (
                    <li key={index}>
                      <a href="#">{message}</a>
                    </li>
                  );
                })}
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
            {memoData.map((record: any) => {
              return (
                <PreValidationAccordionSection
                  key={uuidv4()}
                  title={record.licence_number + " - " + record.operator_name}
                  registrationNumbers={record.registration_numbers}
                />
              );
            })}
            <button
              className=" govuk-button govuk-!-margin-right-3"
              onClick={(e) => handleCommitRegistrations(e)}
              ref={commitRef}
            >
              Commit registrations
            </button>
            <button
              className="govuk-button"
              onClick={handleDiscardRegistrations}
              ref={discardRef}
            >
              Discard registrations
            </button>
          </div>
        )}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default PreValidations;
