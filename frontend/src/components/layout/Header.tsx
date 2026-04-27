import React, { ReactElement, useContext } from "react";
import dynamic from "next/dynamic";
import { IsLoggedInContext } from "../../utils/login/LoginProvider";
import { serviceName } from "../../utils/Constants";

const KainosGovukHeader = dynamic(
  () =>
    import("kainossoftwareltd-govuk-react-kainos").then(
      (module) => module.Header,
    ),
  { ssr: false },
);

type Props = {
  isLoggedIn?: boolean;
};

const Header = (): ReactElement<Props> => {

  const { isLoggedIn, signOutHandler } = useContext(IsLoggedInContext);
  const handleSignOut = () => {
    if (signOutHandler) {
      signOutHandler();
    }
  }

  return (
    <>
      <div className="header-shell">
        <KainosGovukHeader
          serviceName={serviceName}
          serviceUrl="/"
          showNavigation={false}
          rebrand
          signOutUrl="/"
        />
        {isLoggedIn ? (
          <div className="header-sign-out-container">
            <button
              className="govuk-button"
              type="button"
              onClick={handleSignOut}>
                Sign Out
            </button>
          </div>
        ) : null}

      </div>
    </>
  );
};

export default Header;
