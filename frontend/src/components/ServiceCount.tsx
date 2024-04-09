import React from 'react';

interface ServiceCountProps{
    title?: string;
    count: number;
    percentage?: boolean
    description: string;
    descriptionFontWeight?: string;
}

const ServiceCount: React.FC<ServiceCountProps> = ({ title, count, description, percentage, descriptionFontWeight }) => {
    description.includes("OTC") ? description = "OTC Validation": null;
    return (
        <>
            <div className="">
                <h2>
                    {title && title}
                </h2>
            </div>
            <div className=' govuk-!-margin-0'>
                <p className='govuk-!-font-size-36 govuk-!-font-weight-bold govuk-!-margin-0'>{count} {percentage ? '%' : ''} </p>
            </div>
            <div className='govuk-!-font-size-16'>
                <p className={`${descriptionFontWeight ? descriptionFontWeight : ""}`}>{description}</p>
            </div>
        </>
    );
}
export default ServiceCount;
