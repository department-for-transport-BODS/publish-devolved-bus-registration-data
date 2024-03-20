import React from "react";

type Props = {
  errors?: string[];
  setErrorMsg: (msg: string) => void;
  email: string;
  setEmail: React.Dispatch<string>;
  handleRquestPasswordReset: (email:string) => void;
};

const RequestResetPassword : React.FC<Props> = ({ errors , handleRquestPasswordReset, setErrorMsg,email, setEmail}) => {
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    handleRquestPasswordReset(email); // Pass the correct object to handleRquestPasswordReset

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
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="row">
          <div className="govuk-button-group govuk-!-margin-bottom-8">
            <button
              type="submit"
              className="govuk-button"
              data-module="govuk-button"
            >
              Password Reset
            </button>
          <a href="/login" className='govuk-button govuk-button--secondary'>Back to Login</a>
          </div>
        </div>
      </form>
    </>
  );
};

export default RequestResetPassword;
