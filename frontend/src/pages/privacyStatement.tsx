import React, { useContext } from "react";
import { TwoThirdsLayout } from "../Layout/Layout";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import Footer from "../Layout/Footer";

const PrivacyStatement: React.FC = () => {
  const { isLoggedIn } = useContext(IsLoggedInContext);

  return (
    <>
      <TwoThirdsLayout
        title="Privacy Statement"
        description="Home"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
        <h1 className="govuk-heading-xl">Privacy Statement</h1>
        <h2>Last updated: 8th March 2024</h2>
        <div className="govuk-!-font-size-19">
          <p className="govuk-heading-m">Who we are</p>
          <p>
            The Enhanced Partner Devolved Registration Portal (EPP) is a service
            for Local Authorities acting as Enhanced Partners, to publish data
            about local bus service registrations for integration with the Bus
            Open Data Service (BODS). The service is provided by the Department
            for Transport.
          </p>
          <p className="govuk-heading-m">
            The personal data we collect from you includes:
          </p>
          <ul className="govuk-list govuk-list--bullet">
            <li>
              your questions, queries or feedback and email address if you
              contact Bus Open Data Service, supporting mailboxes or team
              members
            </li>
            <li>
              for authorised contributors, your sign- up information when
              registering with the service
            </li>
            <li>
              how you use our emails - for example whether you open them, and
              which links you click on
            </li>
            <li>
              your Internet Protocol (IP) address, and web browser version
            </li>
            <li>
              information on how you use the site, using cookies and page
              tagging
            </li>
          </ul>
          <p className="govuk-heading-m">Why we need your data</p>
          <p className="">
            We want to build an accurate database for local bus services across
            England. So, we require the ability to monitor how the data is being
            provided and used over time.
          </p>

          <p className="govuk-heading-m">We also collect data in order to:</p>
          <ul className="govuk-list govuk-list--bullet">
            <li>
              reply to any feedback you send us, if you&apos;ve asked us to
              allow you to access government services and make transactions
            </li>
            <li>
              provide you with information about local services monitor use of
              the site to identify security threats communicate service messages
              aimed at keeping users
            </li>
            <li>
              informed of the service provided, which includes service updates
              and support that is provided as part of the overall service.
            </li>
            <li>
              spot check the level of service usage for both authorised
              contributors and consumers
            </li>
          </ul>

          <p className="govuk-heading-m">What we do with your data</p>
          <p>
            We use your data to occasionally check your activity when using the
            service. We will not:
          </p>
          <ul>
            <li>Sell or rent your data to third parties.</li>
            <li>share your data with third parties for marketing purposes.</li>
          </ul>
          <p>
            We will share your data if we are required to do so by law - for
            example, by court order, or to prevent fraud or other crime.
          </p>
          <p>
            We use your data to calculate performance metrics to support
            continuous improvement of the service. When you sign up, you can
            also opt in to be contacted to participate in user research. If you
            change your mind later about this, please let us know by emailing
            BusOpenData@dft.gov.uk.
          </p>
          <p className="govuk-heading-m">How long we keep your data for</p>
          <p>
            We will retain your data for as long as you have an EPP account.
            However, if you use an institutional email account and depending on
            what you choose for your account name, this may not include any
            personally identifiable information
          </p>
          <p className="govuk-heading-m">
            Where your data is processed and stored
          </p>
          <p>
            We design, build and run our systems to make sure that your data is
            as safe as possible at any stage, both while it&apos;s s processed
            and when it&apos;s stored. Your personal data will not be
            transferred outside of the European Economic Area (EEA).
          </p>
          <p className="govuk-heading-m">
            How we protect your data and keep it secure
          </p>
          <p>
            We are committed to doing all that we can to keep your data secure.
            To prevent unauthorised access or disclosure we have put in place
            technical and organisational procedures to secure the data we
            collect about you - for example, we protect your data using varying
            levels of encryption. We also make sure that any third parties that
            we deal with have an obligation to keep all personal data they
            process on our behalf secure.
          </p>
          <p className="govuk-heading-m">Children&apos;s privacy protection</p>
          <p>
            We understand the importance of protecting children&apos;s privacy
            online. Our services are not designed for, or intentionally targeted
            at, children 13 years of age or younger. It is not our policy to
            intentionally collect or maintain data about anyone under the age of
            13.
          </p>
          <p className="govuk-heading-m">What are your rights</p>
          <p>You have the right to request:</p>
          <ul>
            <li>information about how your personal data is processed</li>
            <li>a copy of that personal data</li>
            <li>
              that anything inaccurate in your personal data is corrected
              immediately
            </li>
          </ul>
          <p>You can also:</p>
          <ul>
            <li>
              raise an objection about how your personal data is processed
            </li>
            <li>
              request that your personal data is erased if there is no longer a
              justification for it
            </li>
            <li>
              ask that the processing of your personal data is restricted in
              certain circumstances
            </li>
          </ul>
          <p>
            If you have any of these requests, get in contact with our Data
            Protection Officer - you can find their contact details below.
          </p>
          <p className="govuk-heading-m">Changes to this notice</p>
          <p>
            We may modify or amend this privacy notice at our discretion at any
            time. When we make changes to this notice, we will amend the last
            modified date at the top of this page. Any modification or amendment
            to this privacy notice will be applied to you and your data as of
            that revision date. We encourage you to periodically review this
            privacy notice to be informed about how we are protecting your data.
          </p>
          <p className="govuk-heading-m">Contact us or make a complaint</p>
          <p>Contact the DfT Data Protection Officer if you either:</p>
          <ul>
            <li>have any questions about anything in this document</li>
            <li>Think your personal data has been misused or mishandled</li>
          </ul>
          <p>
            Data Protection Officer <br />
            Department for Transport <br />
            3rd Floor <br />
            One Priory Square <br />
            Hasting <br />
            East Sussex <br />
            TN34 1EA <br />
          </p>
          <p>
            Email:{" "}
            <a href="mailto:DataProtectionOfficer@dft.gov.uk">
              DataProtectionOfficer@dft.gov.uk
            </a>
          </p>
          <p>
            Our Personal Information Charter, can be found
            <br /> here:
            <a href="https://www.gov.uk/government/organisations/department-for-transport/about/personal-information-charter">
              {" "}
              Personal information charter
            </a>
          </p>
        </div>
      </TwoThirdsLayout>
      <Footer />
    </>
  );
};

export default PrivacyStatement;
