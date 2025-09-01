import enum


class OAuthProvider(str, enum.Enum):
    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"