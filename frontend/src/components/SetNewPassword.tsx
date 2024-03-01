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
      // samer@SAMER!1
      setPassword(""); // Clear the password
      handleSetNewPassword(password); // Pass the correct object to handleSignIn

    }
  };
  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="govuk-form-group">
          <label className="govuk-label" htmlFor="password">
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
        <div className="govuk-form-group">
          <label className="govuk-label" htmlFor="password">
            ConfirmPassword
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
