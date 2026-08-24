import React from 'react';
interface SuccessfullyUpdatedProps {
    title: string;
    validRecords: number;
}


const SuccessfullyUpdated: React.FC = () => {
    return (
        <>
        <div className="govuk-panel govuk-panel--confirmation">
        <div className="govuk-panel__body">
            <strong>Your data set has been</strong><br/>
            <strong>successfully updated</strong>
        </div>
        </div>
        
        </>
    );
};

export default SuccessfullyUpdated;
