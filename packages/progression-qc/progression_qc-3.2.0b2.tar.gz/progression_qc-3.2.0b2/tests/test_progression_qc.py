from progression_qc import progression_qc

def test_valider_question_sys_complète_valide_avec_tests():
    from question_sys_complète_valide_avec_tests import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements":[], "erreurs":[]}

def test_valider_question_sys_complète_valide_avec_réponse():
    from question_sys_complète_valide_avec_réponse import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements":[], "erreurs":[]}

def test_valider_question_sys_minimale_valide_avec_tests():
    from question_sys_minimale_valide_avec_tests import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements":[], "erreurs":[]}

def test_valider_question_sys_minimale_valide_avec_réponse():
    from question_sys_minimale_valide_avec_réponse import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements":[], "erreurs":[]}
    
def test_valider_question_sys_avec_tests_et_réponse():
    from question_sys_avec_tests_et_réponse import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)
    
    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].message == "{'type': 'sys', 'image': 'odralphabetix', 'tests': [{'validation': 'une validation'}], 'réponse': 'une réponse'} is valid under each of {'required': ['réponse']}, {'required': ['tests']}"

def test_valider_question_sys_sans_image_ni_tests():
    from question_sys_sans_image_ni_tests import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 2
    assert résultat["erreurs"][0].message == "'image' is a required property"
    assert résultat["erreurs"][1].message == "{'type': 'sys'} is not valid under any of the given schemas"


def test_valider_question_sys_avec_image_et_tests_vides():
    from question_sys_avec_image_et_tests_vides import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 2
    assert résultat["erreurs"][0].json_path == "$.image"
    assert résultat["erreurs"][0].message == "'' should be non-empty"
    assert résultat["erreurs"][1].json_path == "$.tests"
    assert résultat["erreurs"][1].message == "[] should be non-empty"

def test_valider_question_sys_avec_image_et_réponse_vides():
    from question_sys_avec_image_et_réponse_vides import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 2
    assert résultat["erreurs"][0].json_path == "$.image"
    assert résultat["erreurs"][0].message == "'' should be non-empty"
    assert résultat["erreurs"][1].json_path == "$.réponse"
    assert résultat["erreurs"][1].message == "'' should be non-empty"

def test_valider_question_sys_test_sortie_nulle():
    from question_sys_test_sortie_nulle import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.tests[0].sortie"
    assert résultat["erreurs"][0].message == "None is not of type 'string', 'integer'"

def test_valider_question_sys_utilisateur_nul():
    from question_sys_utilisateur_nul import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.utilisateur"
    assert résultat["erreurs"][0].message == "None is not of type 'string'"

def test_valider_question_sys_utilisateur_invalide():
    from question_sys_utilisateur_invalide import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.utilisateur"
    assert résultat["erreurs"][0].message == "'un util' does not match '^[a-z][-a-z0-9_]*$'"

def test_valider_question_sys_init_nul():
    from question_sys_init_nul import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.init"
    assert résultat["erreurs"][0].message == "None is not of type 'string'"

def test_valider_question_sys_init_vide():
    from question_sys_init_vide import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.init"
    assert résultat["erreurs"][0].message == "'' should be non-empty"

def test_valider_question_prog_complète():
    from question_prog_complète_valide import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements": [], "erreurs": []}

def test_valider_question_avec_dict_pour_énoncés():
    from question_avec_dict_pour_énoncés import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements": [], "erreurs": []}

def test_valider_question_prog_minimale():
    from question_prog_minimale_valide import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements": [], "erreurs": []}

def test_valider_question_avec_avertissement():
    from question_avec_avertissement import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert len(résultat["avertissements"]) == 1
    assert résultat["avertissements"][0].message == "Unevaluated properties are not allowed ('tata' was unexpected)"
    assert résultat["erreurs"] == []

def test_valider_question_sans_type():
    from question_sans_type import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].message == "'type' is a required property"
    
def test_valider_question_de_type_inconnu():
    from question_de_type_inconnu import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.type"
    assert résultat["erreurs"][0].message == "'erreur' does not match '(?i)^(prog|sys|seq)$'"

def test_valider_question_prog_test_avec_sortie_nulle():
    from question_prog_test_sortie_nulle import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.tests[0].sortie"
    assert résultat["erreurs"][0].message == "None is not of type 'string', 'integer'"

def test_valider_question_prog_test_avec_params_nul():
    from question_prog_test_params_nul import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)


    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.tests[0].params"
    assert résultat["erreurs"][0].message == "None is not of type 'string', 'integer'"

def test_valider_question_prog_sans_ébauches_ni_tests():
    from question_prog_sans_ébauches_ni_tests import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 2
    assert résultat["erreurs"][0].message == "'ébauches' is a required property"
    assert résultat["erreurs"][1].message == "'tests' is a required property"

def test_valider_question_prog_avec_ébauches_et_tests_vides():
    from question_prog_avec_ébauches_et_tests_vides import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 2
    assert résultat["erreurs"][0].json_path == "$.ébauches"
    assert résultat["erreurs"][0].message == "{} should be non-empty"
    assert résultat["erreurs"][1].json_path == "$.tests"
    assert résultat["erreurs"][1].message == "[] should be non-empty"

def test_valider_question_seq_minimale():
    from question_seq_minimale import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat == {"avertissements":[], "erreurs":[]}

def test_valider_question_seq_sans_séquence():
    from question_seq_sans_séquence import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)

    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].message == "'séquence' is a required property"

def test_valider_question_seq_vide():
    from question_seq_vide import question

    résultat = progression_qc.valider_schema_yaml_infos_question(question)


    assert résultat["avertissements"] == []
    assert len(résultat["erreurs"]) == 1
    assert résultat["erreurs"][0].json_path == "$.séquence"
    assert résultat["erreurs"][0].message == "[] should be non-empty"
