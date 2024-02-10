import React from 'react';
import '../Css/App.css';
import Footer from '../Layout/Footer';
import {TwoThirdsLayout} from '../Layout/Layout';
import ImportantBanner from '../components/NotificationBanner';
import ServiceCount from '../components/ServiceCount';
// const height = { height: 'auto' };

// interface PartlyUploadsProps {
//     title: string;
//     validRecords: number;
// }
const PartlyUploading: React.FC = () => {
    return (
        <>
            <TwoThirdsLayout title="Temp Page" description="Temp Page" hideCookieBanner={true}>
            <ImportantBanner message="Some of your data has failed to upload" />
            <ServiceCount  
                title="Summary of successfully uploaded records" 
                count={1099 } 
                description="Registered services"
                 />
            <ServiceCount
                title="Summary of records that failed to upload"
                count={5}
                description="Services failed to upload"
            />
            </TwoThirdsLayout>
            <div className="govuk-grid-row">
                <div className="govuk-grid-column-full">
                    <div className='govuk-width-container'>
                        <div className='row'>
                            <table className="govuk-table">
                                <thead className="govuk-table__head">
                                    <tr className="govuk-table__row">
                                    <th scope="col" className="govuk-table__header app-custom-class">Date</th>
                                    <th scope="col" className="govuk-table__header app-custom-class">Rate for vehicles</th>
                                    <th scope="col" className="govuk-table__header app-custom-class">Rate for bicycles</th>
                                    </tr>
                                </thead>
                                <tbody className="govuk-table__body">
                                    <tr className="govuk-table__row">
                                    <th scope="row" className="govuk-table__header">First 6 weeks</th>
                                    <td className="govuk-table__cell">£109.80 per week</td>
                                    <td className="govuk-table__cell">£59.10 per week</td>
                                    </tr>
                                    <tr className="govuk-table__row">
                                    <th scope="row" className="govuk-table__header">Next 33 weeks</th>
                                    <td className="govuk-table__cell">£159.80 per week</td>
                                    <td className="govuk-table__cell">£89.10 per week</td>
                                    </tr>
                                    <tr className="govuk-table__row">
                                    <th scope="row" className="govuk-table__header">Total estimated pay</th>
                                    <td className="govuk-table__cell">£4,282.20</td>
                                    <td className="govuk-table__cell">£2,182.20</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div className="row">
                            <div className="govuk-button-group govuk-!-margin-bottom-8">
                                <button type="submit" className="govuk-button" data-module="govuk-button">
                                        Publish updated data set
                                </button>
                                <button className="govuk-button govuk-button--secondary" data-module="govuk-button">
                                        Return to homepage
                                </button>
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
