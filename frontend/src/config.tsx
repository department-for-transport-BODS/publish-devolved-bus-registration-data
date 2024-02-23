type AppConfig = {
    apiUrl: string;
};  

type Config = {
    development: AppConfig;
    test: AppConfig;
    uat: AppConfig;
    production: AppConfig;
};  

const getConfig = () => {
    return {
        local: {
            apiUrl: 'http://localhost:8000',
        },
        development: {
            apiUrl: 'https://d2miy41rsrgmw7.cloudfront.net',
        },
        test: {
            apiUrl: 'https://dxq1b6otcjq86.cloudfront.net', 
        },
        uat: {
            // Update with UAT CloudFront URL
            apiUrl: 'https://uat.api.dft.gov.uk',
        },
        production: {
            // Update with PRODUCTION CloudFront URL
            apiUrl: 'https://api.dft.gov.uk',
        },
    };
};

const getEnvironment = (): keyof Config => {
    return (process.env.REACT_APP_ENV || "local") as keyof Config;
};

export const getApiUrl = (): string => {
    const environment = getEnvironment();
    return getConfig()[environment].apiUrl;
};