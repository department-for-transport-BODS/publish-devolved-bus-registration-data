import React, { useState } from "react";

type Props = {
  errors?: string[];
  handleSetNewPassword: (password:string) => void;
  setErrorMsg: (msg: string) => void;
};

const SetNewPassword: React.FC<Props> = ({ errors , handleSetNewPassword, setErrorMsg}) => {


  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setErrorMsg("Passwords do not match");
    }else{
      setPassword(""); // Clear the password
      handleSetNewPassword(password); // Pass the correct object to handleSignIn

    }
  };
  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="govuk-form-group govuk-!-margin-bottom-3">
          <label className="govuk-heading-s govuk-!-margin-bottom-2" htmlFor="password">
            New Password
          </label>
          <input
            className="govuk-input"
            id="password"
            name="password"
            type="password"
            spellCheck="false"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="govuk-form-group govuk-!-margin-bottom-3">
          <label className="govuk-heading-s govuk-!-margin-bottom-2" htmlFor="password">
            Confirm Password
          </label>
          <input
            className="govuk-input"
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            spellCheck="false"
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <div className="row">
          <div className="govuk-button-group govuk-!-margin-bottom-8">
            <button
              type="submit"
              className="govuk-button"
              data-module="govuk-button"
            >
              Submit new password
            </button>
          </div>
        </div>
      </form>
    </>
  );
};

export default SetNewPassword;
