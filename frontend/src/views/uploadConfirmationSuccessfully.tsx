import React from 'react';
import '../Css/App.css';
import Footer from '../Layout/Footer';
import {FullColumnLayout} from '../Layout/Layout';
import SuccessfullyUpdated from '../components/SuccessfullyUpdated';
import ServiceCount from '../components/ServiceCount';
import {Link, useLocation } from 'react-router-dom';

export interface SuccessfullyUploadedProps{
    initialProps: any,
    state?: any
}
const SuccessfullyUploaded: React.FC = () => {
    const location = useLocation();
    const SuccessfullyUploadedRecords: number = location.state?.valid_records_count ? location.state.valid_records_count : undefined;
    if (SuccessfullyUploadedRecords === undefined) {
        return (
            <>
                <FullColumnLayout title="Successfully Uploaded" description="Temp Page" hideCookieBanner={true}>
                   <div>No data to be displayed</div> 
                </FullColumnLayout>
                <Footer />
            </>
        );
    }
    return (

        <>
            <FullColumnLayout title="Temp Page" description="Temp Page" hideCookieBanner={true}>
            <SuccessfullyUpdated />
            <ServiceCount  
                count={SuccessfullyUploadedRecords} 
                description="Registered services"
                 />
                    <div className="row">
                        <div className="govuk-button-group govuk-!-margin-bottom-8 govuk-!-margin-top-7">
                            <Link to="/view-registrations" className="govuk-button">
                            View active registrations
                            </Link>
                        </div>
                    </div>

            </FullColumnLayout>
            <Footer />
        </>
    );
};

export default SuccessfullyUploaded;
