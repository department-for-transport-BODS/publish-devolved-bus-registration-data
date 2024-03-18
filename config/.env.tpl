# General
# ------------------------------------------------------------------------------
PROJECT_ENV=local
PROJECT_NAME=epp
HTTP_PROXY=
HTTPS_PROXY=

# # ReactJS
# # -----------------------------------------------------------------------------
REACT_APP_URL=http://127.0.0.1:8000
REACT_APP_USER_POOL_ID=
REACT_APP_USER_POOL_CLIENT_ID=
REACT_APP_LOGIN_DOMAIN=
REACT_APP_REDIRECT_SIGN_IN=http://localhost:3000/uploadcsv
REACT_APP_REDIRECT_SIGN_OUT=http://localhost:3000/login
REACT_APP_RESPONSE_TYPE=code
REACT_APP_SCOPE=openid email phone profile aws.cognito.signin.user.admin

# # PostgreSQL
# # ------------------------------------------------------------------------------
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=epp

# # CSV Handler Lambda Function
# # ------------------------------------------------------------------------------
COGNITO_USERPOOL_ID=
COGNITO_APP_CLIENT_ID=

# # OTC Client Lambda Function
# # ------------------------------------------------------------------------------
MS_TENANT_ID=
MS_CLIENT_ID=
OTC_API_URL=
MS_LOGIN_URL=
MS_SCOPE=
OTC_CLIENT_SECRET=
OTC_API_KEY=

# # ClamAV
# # -----------------------------------------------------------------------------
# CLAMAV_HOST=clamav
# CLAMAV_PORT=3310