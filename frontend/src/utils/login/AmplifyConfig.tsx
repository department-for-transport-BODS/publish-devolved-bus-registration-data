import { ResourcesConfig } from "aws-amplify";


const AmplifyConfiguration : ResourcesConfig= {
    Auth: {
      Cognito: {
        userPoolClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID? process.env.REACT_APP_USER_POOL_CLIENT_ID : '',
        userPoolId: process.env.REACT_APP_USER_POOL_ID? process.env.REACT_APP_USER_POOL_ID : '',
        loginWith: {
          oauth: {
            domain: process.env.REACT_APP_DOMAIN? process.env.REACT_APP_DOMAIN : '',
            scopes: [process.env.REACT_APP_SCOPES? process.env.REACT_APP_SCOPES : ''],
            redirectSignIn: process.env.REACT_APP_REDIRECT_SIGN_IN? process.env.REACT_APP_REDIRECT_SIGN_IN.split(",") : [],
            redirectSignOut: process.env.REACT_APP_REDIRECT_SIGN_OUT? process.env.REACT_APP_REDIRECT_SIGN_OUT.split(",") : [],
            responseType: process.env.REACT_APP_RESPONSE_TYPE as 'code' | 'token' || 'code',
          },
          username: true,
          email: false,
          phone: false,
        },
      },
    },
  };

export default AmplifyConfiguration;
