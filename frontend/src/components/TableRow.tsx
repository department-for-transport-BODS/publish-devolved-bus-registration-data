import React from 'react';
import { v4 as uuidv4 } from 'uuid';
import { changeDateFormat } from '../utils/ChangeDateFormat';

type TableRowPops = {
    title: string;
    value: React.ReactNode;
    isDate?: boolean;
}

const TableRow= ({ title, value, isDate  }:TableRowPops) => {
    if (isDate && typeof value === 'string') {
      value = changeDateFormat(value);
    }
    
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