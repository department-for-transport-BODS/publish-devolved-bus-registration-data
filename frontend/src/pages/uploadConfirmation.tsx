import React from "react";
import { Link } from "react-router-dom"; // Add this line
import "../Css/App.css";
import Footer from "../Layout/Footer";
import { TwoThirdsLayout } from "../Layout/Layout";
import ImportantBanner from "../components/NotificationBanner";
import ServiceCount from "../components/ServiceCount";
import { useLocation } from "react-router-dom";
import { InvalidRecords, InvalidData } from "../interfaces/invalidRecords";
import PaginatedValidationRecords from "../components/PaginatedValidationRecords";
import { splitArray } from "../utils/DataStructure";
import { v4 as uuidv4 } from "uuid";
// export interface PartlyUploadingProps {
//   UploadedValidRecords: number;
//   InvalidRecordsCount: number;
//   InvalidFieldsData: InvalidFeieldsDataProps;
// }

const PartlyUploading: React.FC = () => {
  const location = useLocation();
  const SuccessfulRecords = location.state?.detail.valid_records_count;
  const InvalidFieldsData = location.state?.detail.invalid_records;
  const tables: {
    invalid_records: { [key: string]: InvalidRecords };
    description: string;
  }[] = [];
  InvalidFieldsData.filter(
    (element: InvalidData) => element.description !== "Record already exists"
  ).forEach((element: InvalidData) => {
    tables.push({
      invalid_records: splitArray(element.records),
      description: element.description,
    });
  });
  console.log(InvalidFieldsData);
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
          key={uuidv4()}
        />
        {InvalidFieldsData.map((element: any) => (
          <div className="govuk-grid-column-one-quarter" key={uuidv4()}>
            <ServiceCount
              key={uuidv4()}
              count={Object.keys(element.records).length}
              description={element.description}
              descriptionFontWeight="govuk-!-font-weight-bold"
            />
          </div>
        ))}
      </TwoThirdsLayout>
      <div className="govuk-grid-row">
        <div className="govuk-grid-column-full">
          <div className="govuk-width-container">
            <div className="row">
              {Object.values(tables).map((data) => (
                <PaginatedValidationRecords
                  records={data.invalid_records}
                  validationTitle={data.description}
                  key={uuidv4()}
                />
              ))}
            </div>
            <div className="row">
              <div className="govuk-button-group govuk-!-margin-bottom-8">
                <Link
                  to="/upload-csv"
                  className="govuk-button"
                  data-module="govuk-button"
                  key={uuidv4()}
                >
                  Publish updated data set
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
