import React, { useEffect } from "react";
import Footer from "../Layout/Footer";
import FullColumnLayout from "../Layout/Layout";
import UploadCsv from "../components/UploadCsv";
import DataProccessingWaiting  from "../components/DataProcessingWaiting";
import {fetchAuthSession } from "aws-amplify/auth";
import { CheckStageProcesses, getStaged } from "../utils/SendCsv";
import { Link, useNavigate } from "react-router-dom";
import Cookies from "universal-cookie";
type Props = {
  isLoggedIn?: boolean;
};
const UploadCsvPage: React.FC<Props> = ({isLoggedIn=false}) => {
const [isloading, setIsLoading] = React.useState<boolean>(false);
const [previousStage, setPreviousStage] = React.useState<boolean>(false);
const [stages, setStages] = React.useState<any>([]);
const [showError, setShowError] = React.useState<boolean>(false);
const [error, setError] = React.useState<string[]>([]);
console.log("upload csv page")

  const navigate = useNavigate();

useEffect(() => {
  fetchAuthSession()
  CheckStageProcesses().then((response) => {
    const processes = response.processes?? [];
    if (processes.length > 0) {
      setStages(processes);
      setPreviousStage(true);
    }
  }).catch((error) => {
    console.error(error);
  });
}
, []);    

  const handleClick = (e:any, stage_id:string) => {
    e.preventDefault();
    console.log(stage_id)
    const cookies = new Cookies();
    cookies.set('stage_id', stage_id, { path: '/' });
    setIsLoading(true);
    setShowError(false);
    setPreviousStage(false);
    getStaged().then((stagedRecords) => {
      console.log(stagedRecords)
      navigate("/pre-validation", { state: {data: stagedRecords.records}, replace: true });
    }).catch((error) => {
      console.error(error);
      navigate("/error", { state: { error: "Getting records failed try agian later!" }, replace: true });
    });
  }

useEffect(() => {
  if(previousStage){
    stages.map((stage:any) => {
      setError((prev)=>[...prev, `Stage processes ${stage.created_at}`])
    });
    setShowError(true);
  }},[previousStage])


  if (isloading===undefined || isloading===null) {
    console.log("isloading is null")
    return null
  }

  return (
    <>
      <FullColumnLayout
        title="Upload CSV"
        description="Temp Page"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >

          {showError && (
          <div
            className="govuk-error-summary"
            aria-labelledby="error-summary-title"
            role="alert"
            tabIndex={-1}
            data-module="error-summary"
          >
            <p className="govuk-error-summary__title govuk-!-margin-bottom-0" id="error-summary-title">
              There is a problem 
              </p>
              <p>
                A previous stage has not been completed, please complete the previous stage before uploading a new file
              </p>
              {previousStage && stages.map((stage:any) => {
          return (
            <div key={stage.created_at}>
              <Link to={`/pre-validation/${stage.stage_id}`} onClick={(e) => handleClick(e,stage.stage_id)}> Stage processes {`${stage.created_at}`}</Link>
              
            </div>
          );
        })}
            </div>
          )}
         {isloading && <DataProccessingWaiting />}
        {!showError && !isloading && <UploadCsv setIsLoading={setIsLoading} />}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default UploadCsvPage;
