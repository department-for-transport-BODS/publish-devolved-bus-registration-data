import React, { useState } from "react";
import { useNavigate } from "react-router-dom";


const UploadCSV: React.FC = () => {
const navigate = useNavigate();
  const [recievedError, setRecievedError] = useState<
    string | null | ErrorTyping
  >(null);

  interface ErrorTyping {
    message: string | undefined | null;
    code: string | null | undefined;
    data: string | null | undefined;
  }

  const handleFileError = (error: any) => {
    setRecievedError(error.message);
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
          handleFileError(new Error("Invalid file type"));
          return false;
        }
        return true;
          }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (selectedFile) {
        if (fileVirosCheck(selectedFile)) {
                const formData = new FormData();
                console.log({ selectedFile })
                formData.append("file", selectedFile);
                console.log({ formData });
                // send form to uplod page
                formData.forEach((value, key) => {
                        console.log(key, value);
                        });
                navigate('/uploading', { state: {"form":selectedFile} }); 
          
        } else{
                handleFileError(new Error("Invalid file type"));
        }


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
              >
                Cancel
              </button>
            </div>
          </fieldset>
        </div>
      </form>
    </div>
  );
};

export default UploadCSV;
