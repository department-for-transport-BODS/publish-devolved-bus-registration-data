import React from 'react';


export interface InvalidFeieldsDataProps{
[key: number]: { [key: string]: string }[];
}

export interface InvalidFeieldsTableProps{
  data : InvalidFeieldsDataProps
  }

const InvalidFeieldsTable: React.FC<InvalidFeieldsTableProps> = ({data}) => {

  console.log(data);

  return (
    <table className="govuk-table">
      <caption className="govuk-table__caption govuk-table__caption--m">Dates and amounts</caption>
      <thead className="govuk-table__head">
        <tr className="govuk-table__row">
          <th scope="col" className="govuk-table__header">Row number</th>
          <th scope="col" className="govuk-table__header">Field and reason for failure</th>
        </tr>
      </thead>
      <tbody className="govuk-table__body">
        {Object.entries(data).map(([RowNumber, fieldsReport]) => (
          <tr key={RowNumber} className="govuk-table__row">
            <th scope="row" className="govuk-table__header">{RowNumber}</th>
            <td className="govuk-table__cell">
              {fieldsReport.map((fieldReport: string, index:number) => (
                <div key={`${RowNumber}-${index}`}>{Object.keys(fieldReport)} - {Object.values(fieldReport)[0]}</div>
              ))}
            </td>
          </tr>
        ))}
        </tbody>
    </table>
  )
}

export default InvalidFeieldsTable;