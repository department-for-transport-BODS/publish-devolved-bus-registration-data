import React from 'react';

interface ServiceCountProps{
    title?: string;
    count: number;
    description: string;
}

const ServiceCount: React.FC<ServiceCountProps> = ({ title, count,description }) => {
    return (
        <>
            <div className="">
                <h2>
                    {title && title}
                </h2>
            </div>
            <div className=' govuk-!-margin-0'>
                <p className='govuk-!-font-size-36 govuk-!-font-weight-bold govuk-!-margin-0'>{count}</p>
            </div>
            <div className='govuk-!-font-size-16'>
                <p>{description}</p>
            </div>
        </>
    );
}
export default ServiceCount;
