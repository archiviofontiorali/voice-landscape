from django.conf import settings


def log_setting(name, *values):
    print(f"{name:>15}: " + " | ".join(map(str, values)))


def run():
    print("***** Settings *****\n")

    log_setting("BASE_DIR", settings.BASE_DIR)
    log_setting("DOMAIN", settings.DOMAIN)
    log_setting("DEBUG | HTTPS", settings.DEBUG, settings.HTTPS)
    log_setting("DATABASE_URL", settings.DATABASE_URL)
    log_setting("SPACY_MODEL", settings.SPACY_MODEL_NAME)

    log_setting("SPEECH_SERVICE", settings.SPEECH_RECOGNITION_SERVICE)
    if settings.SPEECH_RECOGNITION_SERVICE == "whisper":
        log_setting("WHISPER", settings.WHISPER_MODEL, settings.WHISPER_LANGUAGE)

    print("\n***** Settings *****")
