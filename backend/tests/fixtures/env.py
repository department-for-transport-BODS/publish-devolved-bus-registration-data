from pytest import fixture
from os import environ

@fixture
def set_aws_env():
    print("Setup aws test env")
    # set env
    environ["AWS_REGION"] = "us-west-2"
    environ["USERPOOL_ID"] = "us-west-2_abcd1234"
    environ["APP_CLIENT_ID"] = "abcd1234"
    environ["POSTGRES_PORT"] = "5432"
    environ["POSTGRES_USER"] = "test"
    environ["POSTGRES_PASSWORD"] = "test"
    environ["POSTGRES_HOST"] = "localhost"
    environ["POSTGRES_DB"] = "test"
    print("using set_aws_env fixture")
    yield "done"
    print("Teardown aws test env")
    # unset env
    environ.pop("AWS_REGION")
    environ.pop("USERPOOL_ID")
    environ.pop("APP_CLIENT_ID")
    environ.pop("POSTGRES_PORT")
    environ.pop("POSTGRES_USER")
    environ.pop("POSTGRES_PASSWORD")
    environ.pop("POSTGRES_HOST")
    environ.pop("POSTGRES_DB")

    # PG_HOST: str = Field(default_factory=lambda: getenv("POSTGRES_HOST", "localhost"))
    # PG_PORT: str = Field(default_factory=lambda: getenv("POSTGRES_PORT", "5432"))
    # PG_DB: str = Field(default_factory=lambda: getenv("POSTGRES_DB", "postgres"))
    # PG_USER: str = Field(alias="username")