from etl.utils.cleaning import normalize_column_name, clean_text


def test_normalize_column_name():
    assert normalize_column_name("AÑO Lectivo") == "ano_lectivo"
    assert normalize_column_name("PIB per cápita") == "pib_per_capita"


def test_clean_text():
    assert clean_text("  Loja  ") == "LOJA"
    assert clean_text("Pichincha") == "PICHINCHA"
