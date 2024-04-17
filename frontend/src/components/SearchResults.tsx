import React from "react";
import { v4 as uuidv4 } from "uuid";
type SearchResultsProps = {
  data: any[];
  handleRegistrationClick: any;

};
const SearchResults: React.FC<SearchResultsProps> = ({ data,handleRegistrationClick }) => {
  return (
    <>
      <div className="govuk-!-margin-top-5">
        <h2 className="govuk-heading-l">Results</h2>
        <table className="govuk-table">
          <thead className="govuk-table__head">
            <tr className="govuk-table__row">
              <th scope="col" className="govuk-table__header">
                Registration number
              </th>
              <th scope="col" className="govuk-table__header">
                Operator name
              </th>
              <th scope="col" className="govuk-table__header">
                Service number
              </th>
              <th scope="col" className="govuk-table__header">
                Licence status
              </th>
            </tr>
          </thead>
          <tbody className="govuk-table__body">
            {data.map((item,idx) => (
              <tr className="govuk-table__row" key={uuidv4()}>
                <td className="govuk-table__cell">
                  <a href="#"  data-idx={idx} onClick={handleRegistrationClick}>
                    {item.registrationNumber}
                  </a>
                </td>
                <td className="govuk-table__cell">{item.operatorName}</td>
                <td className="govuk-table__cell">
                  {item.registrationNumber.split("/")[1]}
                </td>
                <td className="govuk-table__cell">{item.licenceStatus}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default SearchResults;
