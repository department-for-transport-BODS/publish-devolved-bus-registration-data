import { SignInInput } from "aws-amplify/auth";
import React, { useState, useRef ,useEffect} from "react";

type Props = {
  email: string;
  setEmail: React.Dispatch<string>;
  errors?: string[];
  handleSignIn: (formData: SignInInput) => void;
  emailError: string | null;
  setEmailError: React.Dispatch<string | null>;
  passwordError: string | null;
  setPasswordError: React.Dispatch<string | null>;
  password: string;
  setPassword: React.Dispatch<string>;
};

const LoginForm: React.FC<Props> = ({
  errors,
  handleSignIn,
  email,
  setEmail,
  emailError,
  setEmailError,
  passwordError,
  setPasswordError,
  password,
  setPassword
}) => {

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    setPasswordError(null);
  }
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
    setEmailError(null);
  }
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = {
      username: email,
      password: password,
    };
    setPassword("");
    setEmail("");
    handleSignIn(formData);
  };
  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className={`govuk-form-group govuk-!-margin-bottom-3 ${
          emailError ? "govuk-form-group--error" : null
        }`
        }>
          <label
            className="govuk-heading-s govuk-!-margin-bottom-2"
            htmlFor="email"
          >
            Email address
          </label>
          {emailError && (
            <p id="full-name-input-error" className="govuk-error-message">
              <span className="govuk-visually-hidden">Error:</span> {emailError}
            </p>
          )}
          <input
            className="govuk-input"
            id="email"
            name="email"
            type="email"
            spellCheck="false"
            aria-describedby="email-hint"
            autoComplete="email"
            value={email}
            onChange={handleEmailChange}
          />
        </div>
        <div
          className={`govuk-form-group ${
            passwordError ? "govuk-form-group--error" : null
          }`}
        >
          <label
            className="govuk-heading-s govuk-!-margin-bottom-2"
            htmlFor="password"
            >
            Password
          </label>
            {passwordError && (
            <p id="full-name-input-error" className="govuk-error-message">
              <span className="govuk-visually-hidden">Error:</span> {passwordError}
            </p>
            )}
          <input
            className="govuk-input"
            id="password"
            name="password"
            type="password"
            spellCheck="false"
            value={password}
            onChange={handlePasswordChange}
          />
        </div>
        <div className="row">
          <div className="govuk-button-group govuk-!-margin-bottom-8">
            <button
              type="submit"
              className="govuk-button"
              data-module="govuk-button"
            >
              Sign in
            </button>
          </div>
        </div>
      </form>
    </>
  );
};

export default LoginForm;
