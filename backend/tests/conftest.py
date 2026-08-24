import utils.aws as _utils_aws
from unittest.mock import MagicMock

# csv_handler's utils.aws is resolved first from sys.path.
# otc_client/app.py also imports get_secret from utils.aws.
# Add get_secret as a stub so otc_client's module-level import succeeds.
if not hasattr(_utils_aws, "get_secret"):
    _utils_aws.get_secret = MagicMock(return_value="mock_secret")

