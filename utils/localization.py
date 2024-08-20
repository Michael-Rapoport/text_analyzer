import gettext
import os

def setup_localization():
    localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'locales')
    gettext.install('text_file_analyzer', localedir)

def _(message):
    return gettext.gettext(message)
