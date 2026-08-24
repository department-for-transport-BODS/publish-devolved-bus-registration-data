import React from "react";
import ServiceCount from "./ServiceCount";
import { v4 as uuid4 } from "uuid";

interface AccordionSectionProps {
  title: string;
  registrationNumbers: string[];
  serviceDescription?: string;
}

const PreValidationAccordionSection: React.FC<AccordionSectionProps> = ({
  title,
  registrationNumbers,
  serviceDescription = "Registered services",
}) => {
  return (
    <>
      <div className="govuk-accordion__section">
        <div className="govuk-accordion__section-header">
          <h2 className="govuk-accordion__section-heading">
            <div
              className="govuk-accordion__section-button"
              id="accordion-default-heading-1"
            >
              <span>{title}</span>
              {/* {status === "Valid" ? (
                <span className="govuk-tag govuk-tag--green govuk-!-margin-left-4">
                  Valid in OTC
                </span>
              ) : (
                <span className="govuk-tag govuk-tag--red govuk-!-margin-left-4">
                  Invalid in OTC
                </span>
              )} */}
            </div>
          </h2>
        </div>
        <div
          id="accordion-default-content-1"
          className="govuk-accordion__section-content govuk-!-padding-0"
        >
          <div className="govuk-grid-row">
            <div className="govuk-grid-column-one-quarter govuk-!-padding-bottom-0 govuk-!-padding-top-0">
              <ServiceCount
                count={registrationNumbers.length}
                description={serviceDescription}
              />
              <details className="govuk-details">
                <summary className="govuk-details__summary">
                  <span className="govuk-details__summary-text">
                    Registration numbers
                  </span>
                </summary>
                <div className="govuk-details__text">
                  {registrationNumbers.map((registrationNumber) => {
                    return (
                      <div key={uuid4()}>
                        <p>{registrationNumber}</p>
                      </div>
                    );
                  })}
                </div>
              </details>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
export default PreValidationAccordionSection;
