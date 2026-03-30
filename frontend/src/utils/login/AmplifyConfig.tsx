import { ResourcesConfig } from "aws-amplify";


const AmplifyConfiguration : ResourcesConfig= {
    Auth: {
      Cognito: {
        userPoolClientId: process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID? process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID : '',
        userPoolId: process.env.NEXT_PUBLIC_USER_POOL_ID? process.env.NEXT_PUBLIC_USER_POOL_ID : '',
        loginWith: {
          oauth: {
            domain: process.env.NEXT_PUBLIC_DOMAIN? process.env.NEXT_PUBLIC_DOMAIN : '',
            scopes: [process.env.NEXT_PUBLIC_SCOPES? process.env.NEXT_PUBLIC_SCOPES : ''],
            redirectSignIn: process.env.NEXT_PUBLIC_REDIRECT_SIGN_IN? process.env.NEXT_PUBLIC_REDIRECT_SIGN_IN.split(",") : [],
            redirectSignOut: process.env.NEXT_PUBLIC_REDIRECT_SIGN_OUT? process.env.NEXT_PUBLIC_REDIRECT_SIGN_OUT.split(",") : [],
            responseType: process.env.NEXT_PUBLIC_RESPONSE_TYPE as 'code' | 'token' || 'code',
          },
          username: true,
          email: false,
          phone: false,
        },
      },
    },
  };

export default AmplifyConfiguration;
