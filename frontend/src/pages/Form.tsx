import React, { useState } from 'react';
import CsrfForm from '../components/CsrfForm';



const Form: React.FC = () => {
    const [name, setName] = useState('');
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
            <label>
                Name:
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
            </label>
            <br />
            <label>
                Email:
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <br />
            <button type="submit">Submit</button>
        {/* </form> */}
        </CsrfForm>
    );
};

export default Form;
