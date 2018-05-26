VALID_CHARACTER_CLASSES = [
    'bard',
    'cleric',
    'druid'
    'paladin',
    'ranger',
    'sorcerer',
    'warlock',
    'wizard',
]

CLASSES_VALIDATION_ERROR = "Cannot add an invalid class to a spellbook. VALID CLASSES: {}".format(VALID_CHARACTER_CLASSES)  # noqa
SPELLBOOK_SPELL_NOT_FOUND_ERROR = "One or more of the spells you tried to add could not be found."
SPELLBOOK_SPELL_CLASS_VALIDATION_ERROR = "One or more of the spells you tried to add are not of valid character classes for this spellbook"  # noqa
