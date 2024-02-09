

import React from 'react';

const DefaultPage: React.FC = () => {
    return (
<>
<head>
<meta charSet="utf-8" />
  <title>GOV.UK - The best place to find government services and information</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="theme-color" content="#0b0c0c" />
<link rel="icon" sizes="48x48" href="/assets/images/favicon.ico" />
<link rel="icon" sizes="any" href="/assets/images/favicon.svg" type="image/svg+xml" />
<link rel="mask-icon" href="/assets/images/govuk-icon-mask.svg" color="#0b0c0c" />
<link rel="apple-touch-icon" href="/assets/images/govuk-icon-180.png" />
<link rel="manifest" href="/assets/manifest.json" />
<link rel="stylesheet" href="/stylesheets/govuk-frontend.min.css" />
</head>

<body className="govuk-template__body">
  <script>
    document.body.className += ` js-enabled` + (`noModule`` in HTMLScriptElement.prototype ? ` govuk-frontend-supported` : ``);
  </script>
  <a href="#main-content" className="govuk-skip-link" data-module="govuk-skip-link">Skip to main content</a>
  <header className="govuk-header" role="banner" data-module="govuk-header">
    <div className="govuk-header__container govuk-width-container">
      <div className="govuk-header__logo">
        <a href="/" className="govuk-header__link govuk-header__link--homepage">
          <svg
            focusable="false"
            role="img"
            className="govuk-header__logotype"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 152 30"
            height="30"
            width="152"
            aria-label="GOV.UK">
            <title>GOV.UK</title>
            <path d="M6.7 12.2c1 .4 2.1-.1 2.5-1s-.1-2.1-1-2.5c-1-.4-2.1.1-2.5 1-.4 1 0 2.1 1 2.5m-4.3 2.5c1 .4 2.1-.1 2.5-1s-.1-2.1-1-2.5c-1-.4-2.1.1-2.5 1-.5 1 0 2.1 1 2.5m-1.3 4.8c1 .4 2.1-.1 2.5-1 .4-1-.1-2.1-1-2.5-1-.4-2.1.1-2.5 1-.4 1 0 2.1 1 2.5m10.4-5.8c1 .4 2.1-.1 2.5-1s-.1-2.1-1-2.5c-1-.4-2.1.1-2.5 1s0 2.1 1 2.5m17.4-1.5c-1 .4-2.1-.1-2.5-1s.1-2.1 1-2.5c1-.4 2.1.1 2.5 1 .5 1 0 2.1-1 2.5m4.3 2.5c-1 .4-2.1-.1-2.5-1s.1-2.1 1-2.5c1-.4 2.1.1 2.5 1 .5 1 0 2.1-1 2.5m1.3 4.8c-1 .4-2.1-.1-2.5-1-.4-1 .1-2.1 1-2.5 1-.4 2.1.1 2.5 1 .4 1 0 2.1-1 2.5m-10.4-5.8c-1 .4-2.1-.1-2.5-1s.1-2.1 1-2.5c1-.4 2.1.1 2.5 1s0 2.1-1 2.5m-5.3-4.9 2.4 1.3V6.5l-2.4.8c-.1-.1-.1-.2-.2-.2s1-3 1-3h-3.4l1 3c-.1.1-.2.1-.2.2-.1.1-2.4-.7-2.4-.7v3.5L17 8.8c-.1.1 0 .2.1.3l-1.4 4.2c-.1.2-.1.4-.1.7 0 1.1.8 2.1 1.9 2.2h.6C19.2 16 20 15.1 20 14c0-.2 0-.4-.1-.7l-1.4-4.2c.2-.1.3-.2.3-.3m-1 20.3c4.6 0 8.9.3 12.8.9 1.1-4.6 2.4-7.2 3.8-9.1l-2.6-.9c.3 1.3.3 1.9 0 2.8-.4-.4-.8-1.2-1.1-2.4l-1.2 4.2c.8-.5 1.4-.9 2-.9-1.2 2.6-2.7 3.2-3.6 3-1.2-.2-1.7-1.3-1.5-2.2.3-1.3 1.6-1.6 2.2-.1 1.2-2.4-.8-3.1-2.1-2.4 1.9-1.9 2.2-3.6.6-5.7-2.2 1.7-2.2 3.3-1.2 5.6-1.3-1.5-3.3-.7-2.5 1.7.9-1.4 2.1-.5 2 .8-.2 1.2-1.7 2.1-3.7 2-2.8-.2-3-2.2-3-3.7.7-.1 1.9.5 3 2l.4-4.4c-1.1 1.2-2.2 1.4-3.3 1.4.4-1.2 2.1-3.1 2.1-3.1h-5.5s1.8 2 2.1 3.1c-1.1 0-2.2-.3-3.3-1.4l.4 4.4c1.1-1.5 2.3-2.1 3-2-.1 1.6-.2 3.5-3 3.7-1.9.2-3.5-.8-3.7-2-.2-1.3 1-2.2 1.9-.8.7-2.4-1.3-3.1-2.6-1.7 1-2.3 1-4-1.2-5.6-1.6 2.1-1.3 3.8.6 5.7-1.3-.7-3.2 0-2.1 2.4.6-1.5 1.9-1.1 2.2.1.2.9-.4 1.9-1.5 2.2-1 .2-2.5-.5-3.7-3 .7 0 1.3.4 2 .9L5 20.4c-.3 1.2-.7 1.9-1.2 2.4-.3-.8-.2-1.5 0-2.8l-2.6.9C2.7 22.8 4 25.4 5.1 30c3.8-.5 8.2-.9 12.7-.9m30.5-11.5c0 .9.1 1.7.3 2.5.2.8.6 1.5 1 2.2.5.6 1 1.1 1.7 1.5.7.4 1.5.6 2.5.6.9 0 1.7-.1 2.3-.4s1.1-.7 1.5-1.1c.4-.4.6-.9.8-1.5.1-.5.2-1 .2-1.5v-.2h-5.3v-3.2h9.4V28H59v-2.5c-.3.4-.6.8-1 1.1-.4.3-.8.6-1.3.9-.5.2-1 .4-1.6.6s-1.2.2-1.8.2c-1.5 0-2.9-.3-4-.8-1.2-.6-2.2-1.3-3-2.3-.8-1-1.4-2.1-1.8-3.4-.3-1.4-.5-2.8-.5-4.3s.2-2.9.7-4.2c.5-1.3 1.1-2.4 2-3.4.9-1 1.9-1.7 3.1-2.3 1.2-.6 2.6-.8 4.1-.8 1 0 1.9.1 2.8.3.9.2 1.7.6 2.4 1s1.4.9 1.9 1.5c.6.6 1 1.3 1.4 2l-3.7 2.1c-.2-.4-.5-.9-.8-1.2-.3-.4-.6-.7-1-1-.4-.3-.8-.5-1.3-.7-.5-.2-1.1-.2-1.7-.2-1 0-1.8.2-2.5.6-.7.4-1.3.9-1.7 1.5-.5.6-.8 1.4-1 2.2-.3.8-.4 1.9-.4 2.7zm36.4-4.3c-.4-1.3-1.1-2.4-2-3.4-.9-1-1.9-1.7-3.1-2.3-1.2-.6-2.6-.8-4.2-.8s-2.9.3-4.2.8c-1.1.6-2.2 1.4-3 2.3-.9 1-1.5 2.1-2 3.4-.4 1.3-.7 2.7-.7 4.2s.2 2.9.7 4.2c.4 1.3 1.1 2.4 2 3.4.9 1 1.9 1.7 3.1 2.3 1.2.6 2.6.8 4.2.8 1.5 0 2.9-.3 4.2-.8 1.2-.6 2.3-1.3 3.1-2.3.9-1 1.5-2.1 2-3.4.4-1.3.7-2.7.7-4.2-.1-1.5-.3-2.9-.8-4.2zM81 17.6c0 1-.1 1.9-.4 2.7-.2.8-.6 1.6-1.1 2.2-.5.6-1.1 1.1-1.7 1.4-.7.3-1.5.5-2.4.5-.9 0-1.7-.2-2.4-.5s-1.3-.8-1.7-1.4c-.5-.6-.8-1.3-1.1-2.2-.2-.8-.4-1.7-.4-2.7v-.1c0-1 .1-1.9.4-2.7.2-.8.6-1.6 1.1-2.2.5-.6 1.1-1.1 1.7-1.4.7-.3 1.5-.5 2.4-.5.9 0 1.7.2 2.4.5s1.3.8 1.7 1.4c.5.6.8 1.3 1.1 2.2.2.8.4 1.7.4 2.7v.1zM92.9 28 87 7h4.7l4 15.7h.1l4-15.7h4.7l-5.9 21h-5.7zm28.8-3.6c.6 0 1.2-.1 1.7-.3.5-.2 1-.4 1.4-.8.4-.4.7-.8.9-1.4.2-.6.3-1.2.3-2v-13h4.1v13.6c0 1.2-.2 2.2-.6 3.1s-1 1.7-1.8 2.4c-.7.7-1.6 1.2-2.7 1.5-1 .4-2.2.5-3.4.5-1.2 0-2.4-.2-3.4-.5-1-.4-1.9-.9-2.7-1.5-.8-.7-1.3-1.5-1.8-2.4-.4-.9-.6-2-.6-3.1V6.9h4.2v13c0 .8.1 1.4.3 2 .2.6.5 1 .9 1.4.4.4.8.6 1.4.8.6.2 1.1.3 1.8.3zm13-17.4h4.2v9.1l7.4-9.1h5.2l-7.2 8.4L152 28h-4.9l-5.5-9.4-2.7 3V28h-4.2V7zm-27.6 16.1c-1.5 0-2.7 1.2-2.7 2.7s1.2 2.7 2.7 2.7 2.7-1.2 2.7-2.7-1.2-2.7-2.7-2.7z"></path>
          </svg>
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
    <div className="govuk-width-container">
      <div className="govuk-footer__meta">
        <div className="govuk-footer__meta-item govuk-footer__meta-item--grow">
          <svg
            aria-hidden="true"
            focusable="false"
            className="govuk-footer__licence-logo"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 483.2 195.7"
            height="17"
            width="41">
            <path
              fill="currentColor"
              d="M421.5 142.8V.1l-50.7 32.3v161.1h112.4v-50.7zm-122.3-9.6A47.12 47.12 0 0 1 221 97.8c0-26 21.1-47.1 47.1-47.1 16.7 0 31.4 8.7 39.7 21.8l42.7-27.2A97.63 97.63 0 0 0 268.1 0c-36.5 0-68.3 20.1-85.1 49.7A98 98 0 0 0 97.8 0C43.9 0 0 43.9 0 97.8s43.9 97.8 97.8 97.8c36.5 0 68.3-20.1 85.1-49.7a97.76 97.76 0 0 0 149.6 25.4l19.4 22.2h3v-87.8h-80l24.3 27.5zM97.8 145c-26 0-47.1-21.1-47.1-47.1s21.1-47.1 47.1-47.1 47.2 21 47.2 47S123.8 145 97.8 145" />
          </svg>
          <span className="govuk-footer__licence-description">
            All content is available under the
            <a
              className="govuk-footer__link"
              href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
              rel="license">Open Government Licence v3.0</a>, except where otherwise stated
          </span>
        </div>
        <div className="govuk-footer__meta-item">
          <a
            className="govuk-footer__link govuk-footer__copyright-logo"
            href="https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/">© Crown copyright</a>
        </div>
      </div>
    </div>
  </footer>
  <script type="module" src="/javascripts/govuk-frontend.min.js"></script>
</body>
</>
    );
};

export default DefaultPage;
