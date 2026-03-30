export const config = {
  // Service Name
  serviceName: "Publish devolved bus registration data",

  // Environment
  env: process.env.NODE_ENV || "development",

  // API
  publicApiUrl: process.env.NEXT_PUBLIC_API_URL || "",

  // Cognito / User Pool
  userPoolClientId: process.env.NEXT_PUBLIC_USER_POOL_CLIENT_ID || "",
  userPoolId: process.env.NEXT_PUBLIC_USER_POOL_ID || "",
  oauthDomain: process.env.NEXT_PUBLIC_DOMAIN || "",
  oauthScopes: process.env.NEXT_PUBLIC_SCOPES || "",
  oauthRedirectSignIn: process.env.NEXT_PUBLIC_REDIRECT_SIGN_IN || "",
  oauthRedirectSignOut: process.env.NEXT_PUBLIC_REDIRECT_SIGN_OUT || "",
  oauthResponseType: (process.env.NEXT_PUBLIC_RESPONSE_TYPE as 'code' | 'token') || 'code',

  // Contact Details
  supportEmail: process.env.NEXT_PUBLIC_SUPPORT_EMAIL || "",
  supportPhone: process.env.NEXT_PUBLIC_SUPPORT_PHONE || "",

  // App
  // appVersion: version,
  appUrl: process.env.NEXT_PUBLIC_APP_URL || "www.publish-bus-registrations.dft.gov.uk",
} as const;