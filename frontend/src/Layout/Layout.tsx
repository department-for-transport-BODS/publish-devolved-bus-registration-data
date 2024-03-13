import React, { PropsWithChildren, ReactElement, useEffect, useState } from 'react';
import { ErrorInfo } from '../interfaces';
import PhaseBanner from '../components/PhaseBanner';
import Header from './Header';
import { HeadProvider, Title, Link, Meta } from 'react-head';
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
            <HeadProvider>
                <div className="Home">
                    <Title>{title? title: "EP Project"}</Title>
                    <Meta name="description" content={'Upload CSV'} />
                    <Meta name="viewport" content="width=device-width, initial-scale=1" />
                    <Meta charSet="utf-8" />
                    {/* Additional meta tags or links can be added here */}
                </div>
                {/* Rest of the component */}
            </HeadProvider>
            <Header  />
            <div className="govuk-width-container">
                <PhaseBanner />
                <main className="govuk-main-wrapper">{children}</main>
                {/* {!hideHelp && <Help />} */}
            </div>
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
