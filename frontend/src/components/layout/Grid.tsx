import React from 'react';

export const GridRow: React.FC<{children: React.ReactNode}> = ({children}) =>{
    return (
<div className="govuk-grid-row">
    {children}
</div>
     );
    }   

export const OneThirdColumn: React.FC<{children: React.ReactNode}> = ({children}) =>{
    return (
<div className="govuk-grid-column-one-third">
{children}
</div>
     );
 }

 

export const FullColumn: React.FC<{children: React.ReactNode}> = ({children}) =>{
    return (
<div className="govuk-grid-column-full">
{children}
</div>
     );
 }

 export const OneHalfColumn: React.FC<{children: React.ReactNode}> = ({children}) =>{
     return (
 <div className="govuk-grid-column-one-half">
 {children}
 </div>
      );
  }
export const TwoThirdsColumn: React.FC<{children: React.ReactNode}> = ({children}) =>{
    return (
<div className="govuk-grid-column-two-thirds">
{children}
</div>
     );
 }
 
 export const OneQuarterColumn: React.FC<{children: React.ReactNode}> = ({children}) =>{
     return (
 <div className="govuk-grid-column-one-quarter">
 {children}
 </div>
      );
  }
export const ThreeQuartersColumn: React.FC<{children: React.ReactNode}> = ({children}) =>{
    return (
<div className="govuk-grid-column-three-quarters">
{children}
</div>
     );
 }



