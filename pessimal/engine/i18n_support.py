import i18n


def setup_i18n(override: dict = None):
    override = override or {}
    i18n_path = override.get("i18n_path", "data/i18n")

    # setup localisation
    locale = override.get("lang", "en")
    i18n.load_path.append(i18n_path)
    i18n.set("file_format", "json")
    i18n.set("filename_format", "{namespace}.{format}")
    i18n.set("locale", locale)
