import os

class Config:
    """
    The Config class retrieves credentials from the CredentialManager
    and stores them as class attributes for easy access.
    """

    _manager = None  # Holds the instance of CredentialManager

    @classmethod
    def _init_manager(cls, mongo_uri):
        """
        Initializes the CredentialManager instance if it hasn't been initialized.
        """
        if cls._manager is None:
            secret_key = os.getenv("SECRET_KEY")  # Get the secret key from the environment variable
            if not secret_key:
                raise ValueError("SECRET_KEY environment variable not set.")
            cls._manager = CredentialManager(secret_key, mongo_uri)

    @classmethod
    def load_secrets(cls):
        """
        Loads all secrets into the Config class as class attributes.
        """
        if cls._manager is None:
            raise ValueError("Config manager not initialized. Call _init_manager first.")
        
        secret_ids = cls._manager.list_credentials()
        
        for secret_id in secret_ids:
            secret = cls._manager.get_credentials(secret_id)
            setattr(cls, secret_id, secret)
