class LicenceDetailsError(Exception):
    def __init__(self, message="Licence details not found"):
        self.message = message
        super().__init__(self.message)
