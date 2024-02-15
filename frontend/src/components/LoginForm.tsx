import React, { useState } from 'react';
import CsrfForm from './CsrfForm';



const LoginForm: React.FC = () => {
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Form submitted')
        // print csrf token
        console.log('csrfToken')
        // Handle form submission logic here
    };
    return (
        <CsrfForm action="/form" method="post" csrfToken="csrfToken">
        {/* <form onSubmit={handleSubmit}> */}
        <div className="govuk-form-group">
            <label className="govuk-label" htmlFor="email">
                Email address
            </label>
            <input className="govuk-input" id="email" name="email" type="email" spellCheck="false" aria-describedby="email-hint" autoComplete="email" />
        </div>
        <div className="govuk-form-group">
            <label className="govuk-label" htmlFor="password">
                Password
            </label>
            <input className="govuk-input" id="password" name="password" type="password" spellCheck="false" />
        </div>
        <div className="row">
                            <div className="govuk-button-group govuk-!-margin-bottom-8">
                                <button type="submit" className="govuk-button" data-module="govuk-button">
                                        Sign in
                                </button>
                            </div>
                        </div>
        {/* </form> */}
        </CsrfForm>
    );
};

export default LoginForm;