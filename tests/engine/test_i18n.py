from pessimal.engine import setup_i18n
from pathlib import Path

import i18n

def test_i18n():
    override = {
            "i18n_path": "tests/test_data/"
            }

    # setup default (English)
    setup_i18n(override)

    assert i18n.t("ui.one") == "One", f"{i18n.t('ui.one') =}"
    assert i18n.t("ui.two") == "Two", f"{i18n.t('ui.two') =}"

    setup_i18n(override | {"lang": "fr"})

    assert i18n.t("ui.one") == "Une", f"{i18n.t('ui.one') =}"
    assert i18n.t("ui.two") == "Deux", f"{i18n.t('ui.two') =}"

    setup_i18n(override | {"lang": "de"})

    assert i18n.t("ui.one") == "Ein", f"{i18n.t('ui.one') =}"
    assert i18n.t("ui.two") == "Zwei", f"{i18n.t('ui.two') =}"

