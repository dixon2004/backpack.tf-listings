from utils.config import STEAM_API_KEY
from tf2utilities.main import TF2


tf2 = TF2(STEAM_API_KEY, auto_update=True).schema


spells_attributes = {
    1004: {
        0: 'Die Job',
        1: 'Chromatic Corruption',
        2: 'Putrescent Pigmentation',
        3: 'Spectral Spectrum',
        4: 'Sinister Staining'
    },
    1005: {
        1: 'Team Spirit Footprints',
        2: 'Headless Horseshoes',
        3100495: 'Corpse Gray Footprints',
        5322826: 'Violent Violet Footprints',
        8208497: 'Bruised Purple Footprints',
        8421376: 'Gangreen Footprints',
        13595446: 'Rotten Orange Footprints'
    },
    1006: {
        1: 'Voices From Below'
    },
    1007: {
        1: 'Pumpkin Bombs'
    },
    1008: {
        1: 'Halloween Fire'
    },
    1009: {
        1: 'Exorcism'
    }
}


def get_spell_id(spell_name: str) -> tuple:
    """
    Get spell ID from spell name.

    Args:
        spell_name (str): Name of the spell.

    Returns:
        tuple: Spell category and spell ID.
    """
    for spell_category, spells in spells_attributes.items():
        for spell_id, spell in spells.items():
            if spell.lower() == spell_name.lower():
                return spell_category, spell_id
    return None, None
