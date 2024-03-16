import React from "react";
import BarLoader from "react-spinners/BarLoader";

const DataProccessingWaiting: React.FC = () => {

  return (
    <>
      <div className="govuk-panel proccessing-data-pannel">
        <h3 className="govuk-panel__title">Your data is being processed</h3>
        <div className="govuk-panel__body ">
          <div className="govuk-!-font-size-19">
            Once successfully validated the data set details will be shown.
          </div>
          <div className="govuk-!-display-inline-block">
            <BarLoader color={"#ffffff"} loading={true} width={300} height={6} />
          </div>
        </div>
      </div>
    </>
  );
};

export default DataProccessingWaiting;
