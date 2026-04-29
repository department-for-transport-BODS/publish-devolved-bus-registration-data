import { ResourcesConfig } from "aws-amplify";
import { config } from "../Config";

const AmplifyConfiguration : ResourcesConfig= {
    Auth: {
      Cognito: {
        userPoolClientId: config.userPoolClientId,
        userPoolId: config.userPoolId,
        loginWith: {
          oauth: {
            domain: config.oauthDomain,
            scopes: [config.oauthScopes],
            redirectSignIn: config.oauthRedirectSignIn.split(","),
            redirectSignOut: config.oauthRedirectSignOut.split(","),
            responseType: config.oauthResponseType,
          },
          username: true,
          email: false,
          phone: false,
        },
      },
    },
  };

export default AmplifyConfiguration;
