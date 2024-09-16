import React, { useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { SearchRegistrationNumber } from "../utils/Search";
import { TwoThirdsColumn, GridRow } from "../Layout/Grid";
import TableRow from "../components/TableRow";
import { changeDateFormat } from "../utils/ChangeDateFormat";
type RegistrationDetailsProps = {
  registration: any;
  setShowRegistationDetails: React.Dispatch<React.SetStateAction<boolean>>;
};
const RegistrationDetails: React.FC<RegistrationDetailsProps> = ({
  registration,
  setShowRegistationDetails,
}) => {
  const handleBackToSearch = () => {
    setShowRegistationDetails(false);
  };
  const [DisplayRegistration, setDisplayRegistration] =
    React.useState<any>(registration);
  const [registrations, setRegistrations] = React.useState<any[]>([]);

  const handleVariationClick = (e: React.MouseEvent) => {
    e.preventDefault();
    // Fetch the registration data for the clicked variation number
    const idx = parseInt(e.currentTarget.getAttribute("data-idx") || "0", 10);
    setDisplayRegistration(registrations[idx]);
  };

  useEffect(() => {
    SearchRegistrationNumber(registration.registrationNumber, "No", "Yes")
      .then((response) => {
        setRegistrations(response?.data);
      })
      .catch((error) => {
        console.error("Error fetching registration data: ", error);
      });
  }, []);

  return (
    <>
      <GridRow>
        <TwoThirdsColumn>
          <div>
            <div>
              <table className="govuk-table">
                <thead className="govuk-table__head"></thead>
                <tbody className="govuk-table__body">
                  <TableRow
                    title="Registration number"
                    value={DisplayRegistration.registrationNumber}
                  />
                  <TableRow
                    title="Licence number"
                    value={DisplayRegistration.licenceNumber}
                  />
                  <TableRow
                    title="Route number"
                    value={DisplayRegistration.routeNumber}
                  />
                  <TableRow
                    title="Route description"
                    value={DisplayRegistration.description}
                  />
                  <TableRow
                    title="Variation number"
                    value={DisplayRegistration.variationNumber}
                  />
                  <TableRow
                    title="Start point"
                    value={DisplayRegistration.startPoint}
                  />
                  <TableRow
                    title="End point"
                    value={DisplayRegistration.finishPoint}
                  />
                  <TableRow title="Via" value={registration.via} />
                  <TableRow
                    title="Subsidised"
                    value={DisplayRegistration.subsidised}
                  />
                  <TableRow
                    title="Subsidy detail"
                    value={DisplayRegistration.subsidyDetail}
                  />
                  <TableRow
                    title="Is short notice"
                    value={DisplayRegistration.isShortNotice}
                  />
                  <TableRow
                    title="Received date"
                    value={DisplayRegistration.receivedDate}
                    isDate={true}
                  />
                  <TableRow
                    title="Granted date"
                    value={DisplayRegistration.grantedDate}
                    isDate={true}
                  />
                  <TableRow
                    title="Effective date"
                    value={DisplayRegistration.effectiveDate}
                    isDate={true}
                  />
                  <TableRow
                    title="End date"
                    value={registration.endDate}
                    isDate={true}
                  />
                  <TableRow
                    title="Operator name"
                    value={DisplayRegistration.operatorName}
                  />
                  <TableRow
                    title="Bus service type ID"
                    value={DisplayRegistration.busServiceTypeId}
                  />
                  <TableRow
                    title="Bus service type description"
                    value={DisplayRegistration.busServiceTypeDescription}
                  />
                  <TableRow
                    title="Traffic area ID"
                    value={DisplayRegistration.trafficAreaId}
                  />
                  <TableRow
                    title="Application type"
                    value={DisplayRegistration.applicationType}
                  />
                  <TableRow
                    title="Publication text"
                    value={DisplayRegistration.publicationText}
                  />
                  <TableRow
                    title="Other details"
                    value={DisplayRegistration.otherDetails}
                  />
                  <TableRow
                    title="Licence status"
                    value={DisplayRegistration.licenceStatus}
                  />
                </tbody>
              </table>
            </div>
          </div>
          <div>
            <table className="govuk-table">
              <caption className="govuk-table__caption govuk-table__caption--m">
                Registration history
              </caption>
              <thead className="govuk-table__head">
                <tr className="govuk-table__row">
                  <th scope="col" className="govuk-table__header">
                    Variation number
                  </th>
                  <th
                    scope="col"
                    className="govuk-table__header govuk-table__header--numeric"
                  >
                    Date received
                  </th>
                  <th
                    scope="col"
                    className="govuk-table__header govuk-table__header--numeric"
                  >
                    Date effective
                  </th>
                </tr>
              </thead>
              <tbody className="govuk-table__body">
                {registrations.map((item, idx) => (
                  <tr className="govuk-table__row" key={uuidv4()}>
                    <td className="govuk-table__cell">
                      <a href="#" data-idx={idx} onClick={handleVariationClick}>
                        {item.variationNumber}
                      </a>
                    </td>
                    <td className="govuk-table__cell govuk-table__cell--numeric">
                      {changeDateFormat(item.receivedDate)}
                    </td>
                    <td className="govuk-table__cell govuk-table__cell--numeric">
                      {changeDateFormat(item.effectiveDate)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <button
            className="govuk-button govuk-button--secondary"
            onClick={handleBackToSearch}
          >
            Back to search
          </button>
        </TwoThirdsColumn>
      </GridRow>
    </>
  );
};
export default RegistrationDetails;
