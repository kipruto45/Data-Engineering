from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Class: function"""
    name = 'api'

    def clean(self):
        """Validate model fields."""
        if self.age and not self.age > 0 and self.age < 150:
            raise ValueError(f"Invalid age")
