import React from 'react';

const Basic = () => {
    return (
        <>
            <head>
                <meta charSet="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
                <meta name="theme-color" content="#0b0c0c" />
                <link rel="icon" sizes="48x48" href="/assets/images/favicon.ico" />
                <link rel="icon" sizes="any" href="/assets/images/favicon.svg" type="image/svg+xml" />
                <link rel="mask-icon" href="/assets/images/govuk-icon-mask.svg" color="#0b0c0c" />
                <link rel="apple-touch-icon" href="/assets/images/govuk-icon-180.png" />
            </head>
            <body className="govuk-template__body">
                <a href="#main-content" className="govuk-skip-link" data-module="govuk-skip-link">
                    Skip to main content
                </a>
                <header className="govuk-header" role="banner" data-module="govuk-header">
                    <div className="govuk-header__container govuk-width-container">
                        <div className="govuk-header__logo">
                            <a href="/" className="govuk-header__link govuk-header__link--homepage">
                                GOV.UK
                            </a>
                        </div>
                    </div>
                </header>
                <div className="govuk-width-container">
                    <main className="govuk-main-wrapper" id="main-content" role="main">
                        <h1 className="govuk-heading-xl">Default page template</h1>
                    </main>
                </div>
                <footer className="govuk-footer" role="contentinfo">
                    <div className="govuk-footer__meta">
                        <div className="govuk-footer__meta-item govuk-footer__meta-item--grow">
                            <svg
                                className="govuk-footer__licence-logo"
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 483.2 195.7"
                                height="17"
                                width="41"
                                aria-label="Open Government License logo"
                            >
                                <path d="M0 0h483.2v195.7H0z" fill="#0b0c0c" />
                                <path
                                    className="govuk-footer__licence-description"
                                    fill="#fff"
                                    d="M50.7 25.9h376.6v143.9H50.7z"
                                />
                                <path
                                    className="govuk-footer__link"
                                    fill="#fff"
                                    d="M157.6 25.9h269.7v143.9H157.6z"
                                />
                                <path
                                    className="govuk-footer__meta-item"
                                    fill="#aeaeae"
                                    d="M50.7 25.9h106.9v143.9H50.7z"
                                />
                                <path
                                    className="govuk-footer__link govuk-footer__copyright-logo"
                                    fill="#fff"
                                    d="M0 25.9h50.7v143.9H0z"
                                />
                            </svg>
                            <span className="govuk-footer__licence-description">
                                All content is available under the{' '}
                                <a
                                    className="govuk-footer__link"
                                    href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
                                    rel="license"
                                >
                                    Open Government Licence v3.0
                                </a>
                                , except where otherwise stated
                            </span>
                        </div>
                    </div>
                </footer>
            </body>
        </>
    );
};

export default Basic;