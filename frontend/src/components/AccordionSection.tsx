import React from "react";
import ServiceCount from "./ServiceCount";

interface AccordionSectionProps {
  title: string;
  status: string;
  serviceCount: number;
  serviceDescription?: string ;
  percentage?: boolean;
  serviceRequiringAttentionCount: number;
  serviceRequiringAttentionDescription?: string;
}

const AccordionSection: React.FC<AccordionSectionProps> = ({
  title,
  serviceCount,
  serviceDescription = "Registered services",
  serviceRequiringAttentionCount,
  serviceRequiringAttentionDescription = "Services requiring attention",
  status
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
              {status === "Valid" ? (
                <span className="govuk-tag govuk-tag--green govuk-!-margin-left-4">
                  Valid in OTC
                </span>
              ) : (
                <span className="govuk-tag govuk-tag--red govuk-!-margin-left-4">
                  {status}
                </span>
              )}
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
                count={serviceCount}
                description={serviceDescription}
              />
            </div>
            <div className="govuk-grid-column-one-quarter">
              <ServiceCount
                count={serviceRequiringAttentionCount}
                description={serviceRequiringAttentionDescription}
                percentage={true}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
export default AccordionSection;
