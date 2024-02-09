import React, { useState } from 'react';
import { AxiosError } from 'axios';
import axios from 'axios';
const UploadCSV: React.FC = () => {
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState<string | null| ErrorTyping>(null);

        interface ErrorTyping {
                message: string | undefined | null;
                code: string | null| undefined;
        }

    const handleFileError = (error: any) => {
        setError(error.message);
    };

    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setSelectedFile(event.target.files[0]);
        }
    };

        const handleSubmit = async (event: React.FormEvent) => {
                event.preventDefault();
                if (selectedFile) {
                        const formData = new FormData();
                        formData.append('file', selectedFile);
                        console.log({ formData });
                        try {
                                const response = await axios.post('http://localhost:8000/uploadfile',  formData, {
                                        headers: {
                                                'Content-Type': 'multipart/form-data'
                                        }
                                });
                                console.log('Upload successful:', response?.data);
                        } catch (error) {
                                console.log({ error });
                                if (error as AxiosError){
                                        setError({message: (error as AxiosError).message, code: (error as AxiosError).code});
                                }
                                else{
                                setError((error as any).response?.data);
                                console.error('Upload failed:', error);
                                console.log('Upload failed:', (error as any).response.data);
                                }}        
                }
        };

        



    return (
        <div>
                <form onSubmit={handleSubmit}>
                        {error && <div className="govuk-error-summary" aria-labelledby="error-summary-title" role="alert" tabIndex={-1} data-module="error-summary">
                                <h2 className="govuk-error-summary__title" id="error-summary-title">
                                There is a problem <br/>
                                {(error as ErrorTyping).code} <br/>
                                </h2>
                                </div>}
                                
                        <div className="govuk-form-group">
                                <fieldset className="govuk-fieldset" role="group" aria-describedby="passport-issued-hint">
                                        <legend className="govuk-fieldset__legend govuk-fieldset__legend--l govuk-!-margin-bottom-6">
                                                <h1 className="govuk-fieldset__heading">
                                                        Upload the registrations <br/> CSV below
                                                </h1>
                                        </legend>
                                        <div className="govuk-form-group govuk-!-margin-bottom-8">
                                        <label className="govuk-label" htmlFor="file-upload-1">
                                                Upload in .CSV format
                                        </label>
                                        <input className="govuk-file-upload" id="target" name="fileUpload1" type="file" onChange={handleFileChange} />
                                </div>
                                <div className="govuk-button-group govuk-!-margin-bottom-8">
                                        <button type="submit" className="govuk-button" data-module="govuk-button">
                                                Continue
                                        </button>
                                        <button type="submit" className="govuk-button govuk-button--secondary" data-module="govuk-button">
                                                Cancel
                                        </button>
                                </div>
                                </fieldset>

                        </div>
                        </form>
        </div>
    );
}

export default UploadCSV;
