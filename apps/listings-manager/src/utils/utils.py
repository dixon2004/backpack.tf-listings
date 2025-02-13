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

paints_attributes = {
    1315860: "A Distinctive Lack of Hue",
    2960676: "After Eight",
    3100495: "A Color Similar to Slate",
    3329330: "The Bitter Taste of Defeat and Lime",
    3874595: "Balaclavas Are Forever",
    4345659: "Zepheniah's Greed",
    4732984: "Operator's Overalls",
    5322826: "Noble Hatter's Violet",
    6637376: "An Air of Debonair",
    6901050: "Radigan Conagher Brown",
    7511618: "Indubitably Green",
    8154199: "Ye Olde Rustic Colour",
    8289918: "Aged Moustache Grey",
    8208497: "A Deep Commitment to Purple",
    8400928: "The Value of Teamwork",
    8421376: "Drably Olive",
    10843461: "Muskelmannbraun",
    11049612: "Waterlogged Lab Coat",
    12073019: "Team Spirit",
    12377523: "A Mann's Mint",
    12807213: "Cream Spirit",
    12955537: "Peculiarly Drab Tincture",
    13595446: "Mann Co. Orange",
    14204632: "Color No. 216-190-216",
    15132390: "An Extraordinary Abundance of Tinge",
    15185211: "Australium Gold",
    15308410: "Dark Salmon Injustice",
    15787660: "The Color of a Gentlemann's Business Pants",
    16738740: "Pink as Hell",
    1: "#B8383B"
}

strange_parts_attributes = {
    10: "Scouts Killed", 
    11: "Snipers Killed", 
    12: "Soldiers Killed", 
    13: "Demomen Killed", 
    14: "Heavies Killed", 
    15: "Pyros Killed", 
    16: "Spies Killed", 
    17: "Engineers Killed", 
    18: "Medics Killed", 
    19: "Buildings Destroyed", 
    20: "Projectiles Reflected", 
    21: "Headshot Kills", 
    22: "Airborne Enemy Kills", 
    23: "Gib Kills", 
    27: "Kills Under A Full Moon", 
    28: "Dominations", 
    30: "Revenges", 
    31: "Posthumous Kills", 
    32: "Teammates Extinguished", 
    33: "Critical Kills", 
    34: "Kills While Explosive-Jumping", 
    36: "Sappers Removed", 
    37: "Cloaked Spies Killed", 
    38: "Medics Killed That Have Full ÜberCharge", 
    39: "Robots Destroyed", 
    40: "Giant Robots Destroyed", 
    44: "Kills While Low Health", 
    45: "Kills During Halloween", 
    46: "Robots Killed During Halloween", 
    47: "Defenders Killed", 
    48: "Submerged Enemy Kills", 
    49: "Kills While Invuln ÜberCharged", 
    61: "Tanks Destroyed", 
    62: "Long-Distance Kills", 
    67: "Kills During Victory Time", 
    68: "Robot Scouts Destroyed", 
    74: "Robot Spies Destroyed", 
    77: "Taunt Kills", 
    78: "Unusual-Wearing Player Kills", 
    79: "Burning Player Kills", 
    80: "Killstreaks Ended", 
    81: "Freezecam Taunt Appearances", 
    82: "Damage Dealt", 
    83: "Fires Survived", 
    84: "Allied Healing Done", 
    85: "Point Blank Kills", 
    87: "Kills", 
    88: "Full Health Kills", 
    89: "Taunting Player Kills", 
    93: "Not Crit nor MiniCrit Kills", 
    94: "Players Hit", 
    95: "Assists"
}

killstreak_sheens_attributes = {
    1: 'Team Shine',
    2: 'Deadly Daffodil',
    3: 'Manndarin',
    4: 'Mean Green',
    5: 'Agonizing Emerald',
    6: 'Villainous Violet',
    7: 'Hot Rod'
}

killstreak_effects_attributes = {
    2002: "Fire Horns",
    2003: "Cerebral Discharge",
    2004: "Tornado",
    2005: "Flames",
    2006: "Singularity",
    2007: "Incinerator",
    2008: "Hypno-Beam"
}
