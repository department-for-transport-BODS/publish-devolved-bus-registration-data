// write coocke banner component using react
import React from 'react';

const CookieBanner: React.FC = () => {
    React.useEffect(() => {
        document.cookie = 'cookies_accepted=true;max-age=31536000';
    }, []);
    return (
        <div className="govuk-cookie-banner" data-nosnippet role="region" aria-label="Cookies on [name of service]">
            <div className="govuk-cookie-banner__message govuk-width-container">
                <div className="govuk-grid-row">
                    <div className="govuk-grid-column-two-thirds">
                        <h2 className="govuk-cookie-banner__heading govuk-heading-m">Cookies on [name of service]</h2>
                        <div className="govuk-cookie-banner__content">
                            <p className="govuk-body">We use some essential cookies to make this service work.</p>
                            <p className="govuk-body">We’d also like to use analytics cookies so we can understand how you use the service and make improvements.</p>
                        </div>
                    </div>
                </div>
                <div className="govuk-button-group">
                    <button type="button" className="govuk-button" data-module="govuk-button" id="cookieAccepted" onClick={() => {}} >
                        Accept analytics cookies
                    </button>
                    <button type="button" className="govuk-button" data-module="govuk-button">
                        Reject analytics cookies
                    </button>
                </div>
            </div>
        </div>
    );
};

export default CookieBanner;
