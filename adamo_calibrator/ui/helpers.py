from gettext import translation

from os.path import join
from adamo_calibrator.settings import DEFAULT_LOCALE, RESOURCES_PATH, PO_NAME

LOCALE_PATH = join(RESOURCES_PATH, 'locale')

_actual_locale = DEFAULT_LOCALE


def load_locales(resources_path):
    locale_path = join(resources_path, 'locale')
    reset_locales(locale_path)


def reset_locales(locale_path):
    change_locale(DEFAULT_LOCALE, locale_path)


def change_locale(locale, locale_path):
    global _actual_locale
    _actual_locale = locale
    language = translation(PO_NAME, locale_path, [locale])
    language.install()


def actual_locale():
    return _actual_locale
