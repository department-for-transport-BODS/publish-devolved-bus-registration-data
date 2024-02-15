import React from 'react';
import '../Css/App.css';
import Footer from '../Layout/Footer';
import {TwoThirdsOneThirdLayout} from '../Layout/Layout';
import LoginForm from '../components/LoginForm';
import HelpAndSupport from '../components/HelpAndSupport';

const LoginPage: React.FC = () => (
    <>
        <TwoThirdsOneThirdLayout title="Temp Page" description="Temp Page" hideCookieBanner={true}>
            <div className="govuk-grid-row">
                <div className="govuk-grid-column-two-thirds">
                    <h1 className="govuk-heading-xl">Sign in</h1>
                </div>
            </div>
            <div className="govuk-grid-row">
                <div className="govuk-grid-column-two-thirds">
                    <div className='govuk-!-width-three-quarters'>
                        <p className="govuk-heading-m govuk-!-font-size-27">Enter you Enhanced<br /> partnershop registration account details to sign in</p>
                        <LoginForm />
                    </div>
                </div>
                <div className="govuk-grid-column-one-third">
                    <div className='govuk-!-margin-2 govuk-!-margin-bottom-7'>
                        <h3 className="govuk-heading-m">Forgot your password?</h3>
                        <a href="/reset-password" className="govuk-link">Reset your password</a>
                    </div>
                    <div className='govuk-!-margin-2 govuk-!-margin-bottom-7'>
                        <h3 className="govuk-heading-m">Don&apos;t have account?</h3>
                        <a href="/reset-password" className="govuk-link">Reset your password</a>
                    </div>
                </div>
            </div>
            <HelpAndSupport />
        </TwoThirdsOneThirdLayout>
        <Footer />
    </>
);

export default LoginPage;
