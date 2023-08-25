"""Firebase application configuration."""


import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials


class FirestoreInit:
    """Create client to interact with Firebase tools."""

    def __init__(self, gcp_project_id: str, gcp_bucket_name: str = ""):
        """Intake Google Cloud project info."""
        # Looks for GOOGLE_APPLICATIONS_CREDENTIALS environment variable
        firestore_cred = credentials.ApplicationDefault()
        self.app = firebase_admin.initialize_app(
            firestore_cred,
            {"projectId": gcp_project_id, "storageBucket": gcp_bucket_name},
        )

    def get_auth(self):
        """Return auth."""
        return auth
