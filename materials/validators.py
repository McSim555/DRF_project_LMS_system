from rest_framework.serializers import ValidationError

allowed_links = "youtube.com"


def validate_links(link):
    if allowed_links not in link:
        raise ValidationError(f"Ссылка на {link} недопустима")
