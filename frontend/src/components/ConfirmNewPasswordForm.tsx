import React, { useState } from "react";
import {
  type ConfirmResetPasswordInput, SignInInput
} from "aws-amplify/auth";
type Props = {
  errors?: string[];
  confirmResetPassword: (arg0: ConfirmResetPasswordInput) => Promise<void>;
  setErrorMsg: (arg: string) => void;
  email: string;
  setEmail: React.Dispatch<string>;
  handleSignIn: (input: SignInInput) => Promise<void>;
};

const ConfirmNewPasswordForm: React.FC<Props> = ({ errors , confirmResetPassword, setErrorMsg,email, setEmail, handleSignIn}) => {
  
  
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [confirmationCode, setConfirmationCode] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      console.log(newPassword, confirmPassword)
      setErrorMsg("Passwords do not match");
    }else{
      const formData = {
        username: email, 
        newPassword: newPassword,
        confirmationCode: confirmationCode,
      };
      console.log("formData: ", formData);  
      confirmResetPassword(formData).then((data) => {
        console.log("data from confirmResetPassword: ", data);
        handleSignIn({username: email, password: newPassword})          ;
      }
      ).catch((err) => {
        setErrorMsg(err.message);
      });
      setNewPassword(""); // Clear the password
      setEmail(""); // Clear the email
      setConfirmPassword(""); // Clear the email
      setConfirmationCode(""); // Clear the email
    }
  };
  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="govuk-form-group">
          <label className="govuk-label" htmlFor="email">
            Email address
          </label>
          <input
            className="govuk-input"
            id="email"
            name="email"
            type="email"
            spellCheck="false"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
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
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
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
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <div className="govuk-form-group">
          <label className="govuk-label" htmlFor="confirmationCode">
            Confirmation Code
          </label>
          <input
            className="govuk-input"
            id="confirmationCode"
            name="confirmationCode"
            type="text"
            spellCheck="false"
            value={confirmationCode}
            onChange={(e) => setConfirmationCode(e.target.value)}
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
            <a href="/login" className='govuk-button govuk-button--secondary'>Back to Login</a>
          </div>
        </div>
      </form>
    </>
  );
};

export default ConfirmNewPasswordForm;
