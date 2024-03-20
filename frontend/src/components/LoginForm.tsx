import { SignInInput } from "aws-amplify/auth";
import React, { useState } from "react";

type Props = {
  email: string;
  setEmail: React.Dispatch<string>;
  errors?: string[];
  handleSignIn: (formData: SignInInput) => void;
};

const LoginForm: React.FC<Props> = ({ errors , handleSignIn,email, setEmail}) => {


  const [password, setPassword] = useState("");

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
        <div className="govuk-form-group govuk-!-margin-bottom-3">
          <label className="govuk-heading-s govuk-!-margin-bottom-2" htmlFor="email">
            Email address
          </label>
          <input
            className="govuk-input"
            id="email"
            name="email"
            type="email"
            spellCheck="false"
            aria-describedby="email-hint"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="govuk-form-group">
          <label className="govuk-heading-s govuk-!-margin-bottom-2" htmlFor="password">
            Password
          </label>
          <input
            className="govuk-input"
            id="password"
            name="password"
            type="password"
            spellCheck="false"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
