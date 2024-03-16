import React from "react";
import { Link } from "react-router-dom"; // Add this line
import "../Css/App.css";
import Footer from "../Layout/Footer";
import { TwoThirdsLayout } from "../Layout/Layout";
import ImportantBanner from "../components/NotificationBanner";
import ServiceCount from "../components/ServiceCount";
import InvalidFeieldsTable, {
  InvalidFeieldsDataProps,
} from "../components/InvalidFeieldsTable";
import { useLocation } from "react-router-dom";
export interface PartlyUploadingProps {
  UploadedValidRecords: number;
  InvalidRecordsCount: number;
  InvalidFieldsData: InvalidFeieldsDataProps;
}
const PartlyUploading: React.FC = () => {
  const location = useLocation();
  const SuccessfulRecords = location.state?.detail.valid_records_count;
  const InvalidFieldsData = location.state?.detail.invalid_records;
  return (
    <>
      <TwoThirdsLayout
        title="Partly Uploaded"
        description="Temp Page"
        hideCookieBanner={true}
      >
        <ImportantBanner message="Some of your data has failed to upload" />
        <ServiceCount
          title="Summary of successfully uploaded records"
          count={SuccessfulRecords}
          description="Registered services"
        />
        <ServiceCount
          title="Summary of records that failed to upload"
          count={Object.keys(InvalidFieldsData).length}
          description="Services failed to upload"
        />
      </TwoThirdsLayout>
      <div className="govuk-grid-row">
        <div className="govuk-grid-column-full">
          <div className="govuk-width-container">
            <div className="row">
              <InvalidFeieldsTable data={InvalidFieldsData} />
            </div>
            <div className="row">
              <div className="govuk-button-group govuk-!-margin-bottom-8">
                <Link
                  to="/view-registrations"
                  className="govuk-button"
                  data-module="govuk-button"
                >
                  Pulish update data set
                </Link>
                <Link
                  to="/"
                  className="govuk-button govuk-button--secondary"
                  data-module="govuk-button"
                >
                  Return to homepage
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </>
  );
};

export default PartlyUploading;
