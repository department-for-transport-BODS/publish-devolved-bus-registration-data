class RegionIsNotSet(Exception):
    pass


class UserPoolIdIsNotSet(Exception):
    pass


class AppClientIdIsNotSet(Exception):
    pass


class RecordIsAlreadyExist(Exception):
    pass


class LimitIsNotSet(Exception):
    pass


class LimitExceeded(Exception):
    pass


class GroupIsNotAuthorised(Exception):
    pass


class GroupIsNotFound(Exception):
    pass


class RecordBelongsToAnotherUser(Exception):
    pass


class NotAuthorised(Exception):
    pass


class NoStagedProcessFound(Exception):
    pass


class StagingProcessInProgress(Exception):
    pass


class NoStagedProcess(Exception):
    pass


class PreviousProcessNotCompleted(Exception):
    pass
