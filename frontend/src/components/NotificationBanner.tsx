import React from 'react';

type NotificationBannerProps = {
    message: string;
    header?: string;
};

const Header: React.FC<NotificationBannerProps> = ({ message, header="Important" }) => {
    return (
        <>
            <div className="govuk-notification-banner" role="region" aria-labelledby="govuk-notification-banner-title" data-module="govuk-notification-banner">
                <div className="govuk-notification-banner__header">
                    <h2 className="govuk-notification-banner__title" id="govuk-notification-banner-title">
                        {header}
                    </h2>
                </div>
                <div className="govuk-notification-banner__content">
                    <p className="govuk-notification-banner__heading">
                    {message}
                    </p>
                </div>
            </div>
        </>
    );
};

export default Header;
