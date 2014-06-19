from gettext import translation

from os.path import join
from adamo_calibrator.settings import DEFAULT_LOCALE, RESOURCES_PATH, PO_NAME

LOCALE_PATH = join(RESOURCES_PATH, 'locale')

_actual_locale = DEFAULT_LOCALE


def load_locales():
    reset_locales()


def reset_locales():
    change_locale(DEFAULT_LOCALE)


def change_locale(locale):
    global _actual_locale
    _actual_locale = locale
    language = translation(PO_NAME, LOCALE_PATH, [locale])
    language.install()


def actual_locale():
    return _actual_locale
