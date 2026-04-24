# General
# ------------------------------------------------------------------------------
PROJECT_ENV=local
PROJECT_NAME=pdbrd
HTTP_PROXY=
HTTPS_PROXY=

# # ReactJS
# # -----------------------------------------------------------------------------
NEXT_APP_API_URL=http://127.0.0.1:8000/api/v1
NEXT_APP_USER_POOL_ID=
NEXT_APP_USER_POOL_CLIENT_ID=
NEXT_APP_DOMAIN=
NEXT_APP_REDIRECT_SIGN_IN=http://localhost:3000/uploadcsv
NEXT_APP_REDIRECT_SIGN_OUT=http://localhost:3000/login
NEXT_APP_RESPONSE_TYPE=code
NEXT_APP_SCOPES=openid email phone profile aws.cognito.signin.user.admin
NEXT_APP_SUPPORT_EMAIL=example@example.com
NEXT_APP_SUPPORT_PHONE=01234 567890

# # PostgreSQL
# # ------------------------------------------------------------------------------
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=pdbrd_db

# # CSV Handler Lambda Function
# # ------------------------------------------------------------------------------
CLAMAV_S3_BUCKET_NAME=
COGNITO_USERPOOL_ID=
COGNITO_APP_CLIENT_ID=
OTC_CLIENT_API_URL=

# # OTC Client Lambda Function
# # ------------------------------------------------------------------------------
MS_TENANT_ID=
MS_CLIENT_ID=
OTC_API_URL=
MS_LOGIN_URL=
MS_SCOPE=
OTC_CLIENT_SECRET=
OTC_API_KEY=

# # WECA Client Lambda Function
# # -----------------------------------------------------------------------------
WECA_PARAM_C=
WECA_PARAM_T=
WECA_PARAM_R=
WECA_AUTH_TOKEN=
WECA_API_URL=