import sqladmin

from .models import Voice


class VoiceAdmin(sqladmin.ModelView, model=Voice):
    column_list = [Voice.id, Voice.word]
