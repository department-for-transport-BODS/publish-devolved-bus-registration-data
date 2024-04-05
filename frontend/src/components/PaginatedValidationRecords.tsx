import React, { useState, useEffect } from "react";
import InvalidFeieldsTable from "./InvalidFeieldsTable";
import PaginationComponent from "./PaginationComponent";
import { InvalidRecords } from "../interfaces/invalidRecords";
import { v4 as uuidv4 } from "uuid";
type PaginatedValidationRecordsProps = {
  records: {
    [key: string]: InvalidRecords;
  };
  validationTitle: string;
};

const PaginatedValidationRecords: React.FC<PaginatedValidationRecordsProps> = ({
  records,
  validationTitle,
}) => {
  const [currentPage, setCurrentPage] = useState(1);

  return (
    <div key={uuidv4()}>
      {Object.entries(records).map(([index, data]) => (
        <div
          className={
            currentPage == Number(index) + 1
              ? ""
              : "govuk-tabs__panel govuk-tabs__panel--hidden"
          }
          key={uuidv4()}
        >
          <InvalidFeieldsTable data={data} validationTitle={validationTitle} key={uuidv4()} />
        </div>
      ))}
      <div className="">
        <PaginationComponent
          pagesCount={Object.keys(records).length}
          currentPage={currentPage}
          setCurrentPage={setCurrentPage}
          key={uuidv4()}
        />
      </div>
    </div>
  );
};

export default PaginatedValidationRecords;
