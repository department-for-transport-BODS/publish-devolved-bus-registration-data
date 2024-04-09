import React from "react";
import { InvalidRecords } from "../interfaces/invalidRecords";
import { v4 as uuidv4 } from "uuid";

export interface InvalidFeieldsDataProps {
  [key: number]: { [key: string]: string }[];
}

export interface InvalidFeieldsTableProps {
  data: InvalidRecords;
  validationTitle: string;
}

const InvalidFeieldsTable: React.FC<InvalidFeieldsTableProps> = ({ data, validationTitle}) => {
  const style = {
    minHeight: "350px",
  };
  const columnStyle = {
    width: "160px",
  };
  return (
      <div key={uuidv4()}>
      <div className="border" style={style}>
        <table className="govuk-table">
          <caption className="govuk-table__caption govuk-table__caption--m">
            {validationTitle}
          </caption>
          <thead className="govuk-table__head">
            <tr className="govuk-table__row" style={columnStyle}>
              <th scope="col" className="govuk-table__header">
                Row number
              </th>
              <th
                scope="col"
                className="govuk-table__header"
                style={columnStyle}
              >
                Field
              </th>
              <th
                scope="col"
                className="govuk-table__header"
              >
                Failure
              </th>
            </tr>
          </thead>
          <tbody className="govuk-table__body">
            {Object.entries(data).map(([RowNumber, fieldsReport]) => (
              <tr key={uuidv4()} className="govuk-table__row">
                <th scope="row" className="govuk-table__header"
                style={columnStyle}>
                  {RowNumber}
                </th>
                {fieldsReport.map((fieldReport: { [key: string]: string }) => (
                  <React.Fragment key={uuidv4()}>
                    <td className="govuk-table__cell"
                    style={columnStyle}>
                      {Object.keys(fieldReport)}
                    </td>
                    <td className="govuk-table__cell">
                      {Object.values(fieldReport)[0]}
                    </td>
                  </React.Fragment>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      </div>
  );
};

export default InvalidFeieldsTable;
