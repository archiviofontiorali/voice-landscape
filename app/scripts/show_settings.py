from django.conf import settings


def log_setting(name, *values):
    print(f"{name:<15}: " + " | ".join(map(str, values)))


def run():
    print("***** Settings *****\n")

    log_setting("PROJECT_PATH", settings.PROJECT_PATH)
    log_setting("DOMAIN", settings.DOMAIN)
    log_setting("DEBUG | HTTPS", settings.DEBUG, settings.HTTPS)
    log_setting("DATABASE_NAME", settings.DATABASE_NAME)
    log_setting("DATABASE_ENGINE", settings.DATABASE_ENGINE)
    log_setting("SPACY_MODEL", settings.SPACY_MODEL_NAME)

    log_setting("SPEECH SERVICE", settings.SPEECH_RECOGNITION_SERVICE)
    if settings.SPEECH_RECOGNITION_SERVICE == "whisper":
        log_setting("WHISPER", settings.WHISPER_MODEL, settings.WHISPER_LANGUAGE)

    print("\n***** Settings *****")
