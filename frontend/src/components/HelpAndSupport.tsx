import React from 'react';
import { Link } from 'react-router-dom';
import {TITLE} from '../utils/contants';

const HelpAndSupport: React.FC = () =>{

    return (
        <div>
        <p className="govuk-heading-m">Help and support</p>
        <p>    
        If you are having problems, please contact the {TITLE} service team via this link: <Link to="/contact-us">Contact us</Link>
        </p>
        </div>


    );

}


export default HelpAndSupport