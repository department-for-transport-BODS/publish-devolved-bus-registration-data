import React from 'react';
import Header from '../Layout/Header';
import '../Css/App.css';
import Footer from '../Layout/Footer';
// interface HeaderProps {
//     isAuthed: boolean;
//     csrfToken: string;
//     identifier: string | undefined;
//     user: boolean;
// }
// import CsrfForm from '../components/CsrfForm';
import FullColumnLayout from '../Layout/Layout';
import UploadCSV from '../components/UploadCSV';
// const height = { height: 'auto' };

const TempPage: React.FC = () => {
    return (
        <>
            <FullColumnLayout title="Temp Page" description="Temp Page" hideCookieBanner={true}>
                <UploadCSV />
            </FullColumnLayout>
                <Footer />
        </>
    );
};

export default TempPage;
