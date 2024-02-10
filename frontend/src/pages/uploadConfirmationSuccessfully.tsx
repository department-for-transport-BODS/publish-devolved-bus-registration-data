import React from 'react';
import '../Css/App.css';
import Footer from '../Layout/Footer';
import {FullColumnLayout} from '../Layout/Layout';
import SuccessfullyUpdated from '../components/SuccessfullyUpdated';
import ServiceCount from '../components/ServiceCount';
// const height = { height: 'auto' };

// interface PartlyUploadsProps {
//     title: string;
//     validRecords: number;
// }
const SuccessfullyUploaded: React.FC = () => {
    return (
        <>
            <FullColumnLayout title="Temp Page" description="Temp Page" hideCookieBanner={true}>
            <SuccessfullyUpdated />
            <ServiceCount  
                count={821} 
                description="Registered services"
                 />
                    <div className="row">
                        <div className="govuk-button-group govuk-!-margin-bottom-8 govuk-!-margin-top-7">
                            <button type="submit" className="govuk-button" data-module="govuk-button">
                                    View published data set
                            </button>
                        </div>
                    </div>

            </FullColumnLayout>
            <Footer />
        </>
    );
};

export default SuccessfullyUploaded;
