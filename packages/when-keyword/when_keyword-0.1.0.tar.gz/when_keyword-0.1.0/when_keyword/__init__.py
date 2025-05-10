class when:
    def __init__(self, condition):
        self.condition = condition
        self._during = None

    def during(self, func):
        """Function to run during the main action (e.g., logging/progress)"""
        self._during = func
        return self

    def do(self, action):
        """Main function to execute when condition is True"""
        if self.condition:
            if self._during:
                self._during()
            action()