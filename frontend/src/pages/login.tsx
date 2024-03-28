import React, { useState, useEffect, useContext } from "react";
import Footer from "../Layout/Footer";
import { TwoThirdsOneThirdLayout } from "../Layout/Layout";
import LoginForm from "../components/LoginForm";
import SetNewPassword from "../components/SetNewPassword";
import HelpAndSupport from "../components/HelpAndSupport";
import RequestResetPassword from "../components/RequestResetPassword";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import {
  type SignInInput,
  confirmSignIn,
  ConfirmSignInInput,
  resetPassword,
  confirmResetPassword,
} from "aws-amplify/auth";
import { IsLoggedInContext } from "../utils/login/LoginProvider";
import ConfirmNewPasswordForm from "../components/ConfirmNewPasswordForm";
type Props = {
  error?: string;
  nextPage?: string;
};

const LoginPage: React.FC<Props> = ({ error, nextPage }) => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [confirmPassword, setConfirmPassword] = useState(false);
  const [errors, setErrors] = useState<string[]>(error ? [error] : []);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { isLoggedIn, setIsLoggedIn, signIn } = useContext(IsLoggedInContext);
  const [showError, setShowError] = useState(false);
  const location = useLocation();
  const state = location?.state ? location.state : null;
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [confirmPasswordReset, setConfirmPasswordReset] = useState<
    boolean | null
  >(null);
  async function handleSignIn({ username, password }: SignInInput) {
    if (isLoggedIn){ 
      setErrorMsg("A user is are already signed in")
    return}

    if (username ==="" || password ==="") {
      setErrorMsg("Please enter your email and password");
    if (username === "") {
      setEmailError("Enter your email address");
      setPassword(!password? "" :password)
    }
    if (password === "") {
      setPasswordError("Enter a password");
      setEmail(email)
    }
    return;
  }
    try {
      const { isSignedIn, nextStep } = await signIn({ username, password });
      setIsLoggedIn ? setIsLoggedIn(isSignedIn) : null;
      if (isSignedIn) {
        if (nextPage) {
          navigate(`/${nextPage}`);
        } else {
          navigate("/");
        }
      }
      if (nextStep) {
        const signInStep = nextStep.signInStep ? nextStep.signInStep : "";
        if (signInStep === "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED") {
          setConfirmPassword(true);
        }
      }
    } catch (error) {
      const errorMsg = (error as Error)?.message;
      setErrorMsg(errorMsg);
    }
  }

  const handleSetNewPassword = (password: string) => {
    const signInInput: ConfirmSignInInput = { challengeResponse: password };
    confirmSignIn(signInInput)
      .then(() => {
        setIsLoggedIn ? setIsLoggedIn(true) : null;
        navigate("/");
      })
      .catch((error) => {
        const errorMsg = (error as Error)?.message;
        setErrorMsg(errorMsg);
      });
  };

  const [requestPasswordReset, setRequestPasswordReset] = useState<
    boolean | null
  >(null);
  useEffect(() => {
    setConfirmPasswordReset(false);
    setConfirmPassword(false);
  }, [requestPasswordReset]);

  const handleRquestPasswordReset = (email: string) => {
    setRequestPasswordReset(false);
    resetPassword({ username: email })
      .then((data) => {
        const nextStep = data.nextStep ? data.nextStep.resetPasswordStep : "";
        if (nextStep === "CONFIRM_RESET_PASSWORD_WITH_CODE") {
          setConfirmPasswordReset(true);
        }else{
            navigate("/login");
        }
      })
      .catch((error) => {
        const errorMsg = (error as Error)?.message;
        setErrorMsg(errorMsg);
        console.error("error from reset password: ", error);
      });
  };

  useEffect(() => {
    if (errorMsg) {
      setShowError(true);
    }
  }, [errorMsg]);

  useEffect(() => {
    if (state?.error) {
      setErrorMsg(state.error);
      location.state = null;
    }
  }, [state, location]);

  return (
    <>
      <TwoThirdsOneThirdLayout
        title="Temp Page"
        description="Temp Page"
        hideCookieBanner={true}
      >
        <div className="govuk-grid-row">
          <div className="govuk-grid-column-two-thirds">
            <h1 className="govuk-heading-xl">Sign in</h1>
          </div>
        </div>
        {showError && (
          <div
            className="govuk-error-summary"
            aria-labelledby="error-summary-title"
            role="alert"
            tabIndex={-1}
            data-module="error-summary"
          >
            <h2 className="govuk-error-summary__title" id="error-summary-title">
              There is a problem
            </h2>
            <div className="govuk-error-message">
              <p>{errorMsg}</p>
            </div>
          </div>
        )}
        <div className="govuk-grid-row">
          <div className="govuk-grid-column-two-thirds">
            <div className="govuk-!-width-three-quarters">
              <p className="govuk-heading-m govuk-!-font-size-27">
                Enter you Enhanced
                <br /> partnership registration account details to sign in
              </p>
              {!confirmPassword &&
                !confirmPasswordReset &&
                !requestPasswordReset && (
                  <LoginForm
                    errors={errors}
                    handleSignIn={handleSignIn}
                    email={email}
                    setEmail={setEmail}
                    emailError={emailError}
                    setEmailError={setEmailError}
                    passwordError={passwordError}
                    setPasswordError={setPasswordError}
                    password={password}
                    setPassword={setPassword}

                  />
                )}
              {confirmPassword && (
                <SetNewPassword
                  errors={errors}
                  handleSetNewPassword={handleSetNewPassword}
                  setErrorMsg={setErrorMsg}
                />
              )}
              {confirmPasswordReset && (
                <ConfirmNewPasswordForm
                  errors={errors}
                  confirmResetPassword={confirmResetPassword}
                  setErrorMsg={setErrorMsg}
                  email={email}
                  setEmail={setEmail}
                  handleSignIn={handleSignIn}
                />
              )}
              {requestPasswordReset && (
                <RequestResetPassword
                  setErrorMsg={setErrorMsg}
                  handleRquestPasswordReset={handleRquestPasswordReset}
                  email={email}
                  setEmail={setEmail}
                />
              )}
            </div>
          </div>
          <div className="govuk-grid-column-one-third">
            <div className="govuk-!-margin-2 govuk-!-margin-bottom-7">
              <h3 className="govuk-heading-m">Forgot your password?</h3>
              <a
                href="#"
                className="govuk-link"
                onClick={() => setRequestPasswordReset(true)}
              >
                Reset your password
              </a>
            </div>
            <div className="govuk-!-margin-2 govuk-!-margin-bottom-7"></div>
          </div>
        </div>
        <HelpAndSupport />
      </TwoThirdsOneThirdLayout>
      <Footer />
    </>
  );
};


export default LoginPage;
