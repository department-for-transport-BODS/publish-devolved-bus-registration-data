import React from 'react';
import { Link } from 'react-router-dom';
import { config } from '../../utils/Config';

const HelpAndSupport: React.FC = () =>{

    return (
        <div>
        <p className="govuk-heading-m">Help and support</p>
        <p className="govuk-body">    
        If you are having problems, please contact the {config.serviceName} service team via this link: <Link to="/contact-us">Contact us</Link>
        </p>
        </div>


    );

}


export default HelpAndSupport