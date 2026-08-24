import React from "react";
import BarLoader from "react-spinners/BarLoader";
 type DataProccessingWaitingProps ={
  title?: string,
  description?: string,
};

const DataProccessingWaiting: React.FC<DataProccessingWaitingProps> = ({title,description}) => {

  return (
    <>
      <div className="govuk-panel proccessing-data-pannel">
        <h3 className="govuk-panel__title">{title? title : "Your data is being processed"}</h3>
        <div className="govuk-panel__body ">
          <div className="govuk-!-font-size-19">
            {description? description: "Once successfully validated the dataset details will be shown."}
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
