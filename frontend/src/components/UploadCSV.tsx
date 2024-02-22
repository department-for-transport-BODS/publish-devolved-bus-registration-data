import React, { ReactElement, useState } from "react";
import { useNavigate } from "react-router-dom";
import { SendCSV } from "../utils/SendCSV";


interface UploadCSVProps {
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const UploadCSV: React.FC<UploadCSVProps> = ({
  setIsLoading,
}): ReactElement => {
  const navigate = useNavigate();
  const [recievedError, setRecievedError] = useState<
     null | ErrorTyping
  >(null);

  interface ErrorTyping {
    message: string;
    code?: string;
  }

  const handleFileError = (error: Error) => {
    const errorData = {
      message: error.message,
    };
    setRecievedError(errorData);
  };

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const fileVirosCheck = (file: File) => {
    const allowedExtensions = /(\.csv)$/i;
    if (!allowedExtensions.exec(file.name)) {
      return false;
    }
    return true;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (selectedFile) {
      if (fileVirosCheck(selectedFile)) {
        const formData = new FormData();
        formData.append("file", selectedFile);
        setIsLoading(true);
        await SendCSV(formData, navigate);
      } else {
        handleFileError(new Error("The file format must be.CSV"));
      }
    } else {
      handleFileError(new Error("No file selected"));
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {recievedError && (
          <div
            className="govuk-error-summary"
            aria-labelledby="error-summary-title"
            role="alert"
            tabIndex={-1}
            data-module="error-summary"
          >
            <h2 className="govuk-error-summary__title" id="error-summary-title">
              There is a problem <br />
              {(recievedError as ErrorTyping).code} <br />
            </h2>
            <p className="govuk-error-message">
              {(recievedError as ErrorTyping).message} <br />
            </p>
          </div>
        )}

        <div className="govuk-form-group">
          <fieldset
            className="govuk-fieldset"
            role="group"
            aria-describedby="passport-issued-hint"
          >
            <legend className="govuk-fieldset__legend govuk-fieldset__legend--l govuk-!-margin-bottom-6">
              <h1 className="govuk-fieldset__heading">
                Upload the registrations <br /> CSV below
              </h1>
            </legend>
            {recievedError ? (
              <div className="govuk-form-group govuk-!-margin-bottom-8 govuk-form-group--error">
                <label className="govuk-label" htmlFor="file-upload-1">
                  Upload in .CSV format
                </label>
                <p className="govuk-error-message">
                  File must be in .csv format
                </p>
                <input
                  className="govuk-file-upload govuk-input--error govuk-input"
                  id="target"
                  name="fileUpload1"
                  type="file"
                  onChange={handleFileChange}
                />
              </div>
            ) : (
              <div className="govuk-form-group govuk-!-margin-bottom-8">
                <label className="govuk-label" htmlFor="file-upload-1">
                  Upload in .CSV format
                </label>
                <input
                  className="govuk-file-upload"
                  id="target"
                  name="fileUpload1"
                  type="file"
                  onChange={handleFileChange}
                />
              </div>
            )}
            <div className="govuk-button-group govuk-!-margin-bottom-8">
              <button
                type="submit"
                className="govuk-button"
                data-module="govuk-button"
              >
                Continue
              </button>

              <button
                className="govuk-button govuk-button--secondary"
                data-module="govuk-button"
                onClick={() => {
                  navigate("/", { replace: true });
                }}
              >
                Cancel (return to homepage)
              </button>
            </div>
          </fieldset>
        </div>
      </form>
    </div>
  );
};
export default UploadCSV;
