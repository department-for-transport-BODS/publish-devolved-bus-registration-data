import React from 'react';
import { v4 as uuidv4 } from 'uuid';

const TableRow = ({ title, value }: { title: string, value: React.ReactNode }) => {
    return (
        <>
         <tr key={uuidv4()} className="govuk-table__row">
         <th scope="row" className="govuk-table__header">
           {title}
         </th>
         <td className="govuk-table__cell">{value}</td>
       </tr>
       </>
    );
}

export default TableRow;