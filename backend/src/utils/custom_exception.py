class LicenceDetailsError(Exception):
    def __init__(self, message="Licence details not found", value=None):
        self.message = message
        super().__init__(self.message)

