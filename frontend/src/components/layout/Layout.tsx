import React, { PropsWithChildren, ReactElement } from 'react';
import Head from 'next/head';
import { ErrorInfo } from '../../interfaces';
import PhaseBanner from './PhaseBanner';
import Header from './Header';
import Footer from './Footer';
interface LayoutProps {
    title: string;
    description: string;
    errors?: ErrorInfo[];
    hideCookieBanner?: boolean;
    showNavigation?: boolean;
    hideHelp?: boolean;
    referer?: string | null;
    isLoggedIn?: boolean;
}

export const BaseLayout = ({
    title,
    children,
}: PropsWithChildren<LayoutProps>): ReactElement => {
    return (
        <>
            <Head>
                <title>{title ? title : 'PDBRD Project'}</title>
                <meta name="description" content="Upload CSV" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <meta charSet="utf-8" />
            </Head>
            <Header  />
            <div className="govuk-width-container">
                <PhaseBanner />
                <main className="govuk-main-wrapper">{children}</main>
                {/* {!hideHelp && <Help />} */}
            </div>
            <Footer />
        </>
    );
};

export const FullColumnLayout = ({
    title,
    description,
    errors = [],
    children,
    hideCookieBanner = false,
    hideHelp = false,
    isLoggedIn = false
}: PropsWithChildren<LayoutProps>): ReactElement => (
    <BaseLayout
        title={title}
        description={description}
        errors={errors}
        hideCookieBanner={hideCookieBanner}
        hideHelp={hideHelp}
        isLoggedIn={isLoggedIn}
    >
        <div className="govuk-grid-row">
            <div className="govuk-grid-column-full">{children}</div>
        </div>
    </BaseLayout>
);

export const TwoThirdsOneThirdLayout = ({
    title,
    description,
    errors = [],
    children,
    hideCookieBanner = false,
    hideHelp = false,
    isLoggedIn = false
}: PropsWithChildren<LayoutProps>): ReactElement => (
    <BaseLayout
        title={title}
        description={description}
        errors={errors}
        hideCookieBanner={hideCookieBanner}
        hideHelp={hideHelp}
        isLoggedIn={isLoggedIn}
    >
        <div className="govuk-grid-row">{children}</div>
    </BaseLayout>
);
export const TwoThirdsLayout = ({
    title,
    description,
    errors = [],
    children,
    hideCookieBanner = false,
    hideHelp = false,
    isLoggedIn = false
}: PropsWithChildren<LayoutProps>): ReactElement => (
    <BaseLayout
        title={title}
        description={description}
        errors={errors}
        hideCookieBanner={hideCookieBanner}
        hideHelp={hideHelp}
        isLoggedIn={isLoggedIn}
    >
        <div className="govuk-grid-row">
            <div className="govuk-grid-column-two-thirds">{children}</div>
        </div>
    </BaseLayout>
);

export default TwoThirdsLayout;
