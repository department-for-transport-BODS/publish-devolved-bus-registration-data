import React from 'react';
import '../Css/App.css';
import Footer from '../Layout/Footer';
import {FullColumnLayout} from '../Layout/Layout';
import SuccessfullyUpdated from '../components/SuccessfullyUpdated';
import ServiceCount from '../components/ServiceCount';
import {useLocation } from 'react-router-dom';
// const height = { height: 'auto' };

// interface PartlyUploadsProps {
//     title: string;
//     validRecords: number;
// }
export interface SuccessfullyUploadedProps{
    initialProps: any,
    state?: any
}
const SuccessfullyUploaded: React.FC = () => {
    const location = useLocation();
    const SuccessfullyUploadedProps = location.state.valid_records;
    return (
        <>
            <FullColumnLayout title="Temp Page" description="Temp Page" hideCookieBanner={true}>
            <SuccessfullyUpdated />
            <ServiceCount  
                count={SuccessfullyUploadedProps} 
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
