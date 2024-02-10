import React from 'react';
import { FullColumnLayout } from '../Layout/Layout';

const Home: React.FC = () => {
    return (
        <>
        <FullColumnLayout title="Home" description="Home" hideCookieBanner={true}>
            <h1 className='govuk-heading-xl'>
                Enhanced Partnerships Registration tool
            </h1>
            <p className='govuk-body'>
            This service is for uploading enhanced partnership registrations data for public transport services, excluding rail, in England.
            </p>
            <div>
                <p>The service can be used by:</p>
                <ul className="govuk-list govuk-list--bullet">
                    <li>Enhanced partnerships in England</li>
                    <li>Franchises in England</li>
                </ul>
            </div>
            <div>
                <p>The service can be used by:</p>
                <ul className="govuk-list govuk-list--bullet">
                    <li>Enhanced partnerships in England</li>
                    <li>Franchises in England</li>
                </ul>
            </div>
            <div>
            <a href="#" role="button" draggable="false" className="govuk-button govuk-button--start" data-module="govuk-button">
  Start now
  <svg className="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg" width="17.5" height="19" viewBox="0 0 33 40" aria-hidden="true" focusable="false">
    <path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" />
  </svg>
</a>
            </div>
            <div>
            Help and support

If you are having problems, please contact the Enhanced partnerships service team via this link: Contact us
            </div>
        </FullColumnLayout>
        </>
    );
};

export default Home;
