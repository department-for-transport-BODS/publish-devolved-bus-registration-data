import React, { useEffect } from "react";
import Footer from "../Layout/Footer";
import FullColumnLayout from "../Layout/Layout";
import UploadCsv from "../components/UploadCsv";
import DataProccessingWaiting from "../components/DataProccessingWaiting";
import {
  CheckStageProcesses,
  getStaged,
  handleStagedResults,
} from "../utils/SendCsv";
import { Stage } from "../interfaces/apiTypes";
import { Link, useNavigate } from "react-router-dom";
import { AxiosError } from "axios";


type Props = {
  isLoggedIn?: boolean;
};
const UploadCsvPage: React.FC<Props> = ({ isLoggedIn = false }) => {
  const [isloading, setIsLoading] = React.useState<boolean | null>(null);
  const [previousStage, setPreviousStage] = React.useState<boolean>(false);
  const [stages, setStages] = React.useState<Stage[]>([]);
  const [showError, setShowError] = React.useState<boolean | null>(null);
  const [_error, setError] = React.useState<string[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    CheckStageProcesses().then((response) => {
      if (response instanceof AxiosError) {
        setPreviousStage(false);
        setShowError(false);
        return;
      }
      const processes = response?.processes ?? [];
      if (processes.length > 0) {
        setStages(processes);
        setPreviousStage(true);
      } else {
        setPreviousStage(false);
        setShowError(false);
      }
    });
  }, []);

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setShowError(false);
    setPreviousStage(false);
    getStaged()
      .then((stagedRecords) => {
        if (stagedRecords instanceof AxiosError) {
          navigate("/error", {
            state: { error: "Getting records failed try again later!" },
            replace: true,
          });
          return;
        }
        handleStagedResults(stagedRecords, navigate);
      })
      .catch(() => {
        navigate("/error", {
          state: { error: "Getting records failed try again later!" },
          replace: true,
        });
      });
  };

  useEffect(() => {
    if (previousStage) {
      // TODO: error state is populated but never rendered — either display these messages or remove the state
      stages.map((stage: Stage) => {
        setError((prev) => [...prev, `Stage processes ${stage.created_at}`]);
      });
      setShowError(true);
    }
  }, [previousStage, stages]);

  // if (showError===undefined || showError===null) {
  //   return null
  // }
  return (
    <>
      <FullColumnLayout
        title="Upload CSV"
        description="Temp Page"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        {(showError === undefined || showError === null) && (
          <DataProccessingWaiting
            title="Check previous uploads"
            description="Checking previous uploaded processes"
          />
        )}
        {showError && (
          <div
            className="govuk-error-summary"
            aria-labelledby="error-summary-title"
            role="alert"
            tabIndex={-1}
            data-module="error-summary"
          >
            <p
              className="govuk-error-summary__title govuk-!-margin-bottom-0"
              id="error-summary-title"
            >
              There is a problem
            </p>
            <p>
              A previous stage has not been completed, please complete the
              previous stage before uploading a new file
            </p>
            {previousStage &&
              stages.map((stage: Stage) => {
                return (
                  <div key={stage.created_at}>
                    <Link
                      to={`/pre-validation/${stage.stage_id}`}
                      onClick={(e) => handleClick(e)}
                    >
                      {" "}
                      Stage processes {`${stage.created_at}`}
                    </Link>
                  </div>
                );
              })}
          </div>
        )}
        {isloading && <DataProccessingWaiting />}
        {showError !== null && !showError && !isloading && (
          <UploadCsv setIsLoading={setIsLoading} />
        )}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default UploadCsvPage;
