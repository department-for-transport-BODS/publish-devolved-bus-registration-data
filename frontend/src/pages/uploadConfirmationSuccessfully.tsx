import React from 'react';
import '../Css/App.css';
import Footer from '../Layout/Footer';
import {FullColumnLayout} from '../Layout/Layout';
import SuccessfullyUpdated from '../components/SuccessfullyUpdated';
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
            </FullColumnLayout>
            <Footer />
        </>
    );
};

export default SuccessfullyUploaded;
