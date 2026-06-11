from Mantissa import Mantissa
from pathlib import Path
global_path_reference = Path(__file__).resolve().parent.parent
abs_stat_info = {
    "Pre-existence": {
        "Byte": {"Multis": None},
        "Binary": {"Multis": None},
        "Script": {"Multis": {"Byte": 10, "Binary": 6}},
        "Language": {"Multis": {"Byte": 10, "Script": 5}},
        "Compiler": {"Multis": {"Script": 7, "Language": 1.7}, "Recipe": {"Byte": 1e16, "Binary": 1e8, "Script": 1000, "Language": 5}},
        "RAM": {"Multis": {"Byte": 100, "Binary": 50, "Script": 25, "Language": 10}},
        "Reality Tether": {"Multis": None, "Recipe": {"Byte": 1e100, "Binary": 1e50, "Script": 1e33, "Language": 1e16, "Compiler": int(1e6), "RAM": 100}},
        "Data": {"Multis": None}
    },
    "Main Progression": {
     "Cash":  {"Multis": None}, 
     "Multiplier":  {"Multis": None}, 
     "Rebirths":  {"Multis": {"Multiplier": 2}}, 
     "Stone": {"Multis": {"Cash": 1.5, "Rebirths": 2}}, 
     "White Gems": {"Multis": {"Multiplier": 1.5, "Stone": 1.8}}, 
     "Crystal": {"Multis": {"Cash": 2, "White Gems": 3}}, 
     "Iron": {"Multis": {"Rebirths": 1.5, "Crystal": 2}}, 
     "Gold": {"Multis": {"Cash": 2, "Stone": 2, "Iron": 2}}, 
     "Quartz": {"Multis": {"Multiplier": 10, "Rebirths": 2, "Stone": 5, "White Gems": 3, "Crystal": 2, "Gold": 2}}, 
     "Jade": {"Multis": {"Cash": 3, "Rebirths": 10, "Stone": 4, "Crystal": 4, "Quartz": 3}}, 
     "Obsidian": {"Multis": {"Rebirths": 15, "Stone": 15,"White Gems": 15, "Crystal": 10, "Iron": 10, "Gold": 7.5, "Jade": 5}}, 
     "Ruby": {"Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2}}, 
     "Emerald": {"Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2}}, 
     "Sapphire": {"Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2}}, 
     "Diamond": {"Multis": {"Emerald": 3, "Sapphire": 2}}, 
     "Starlight": {"Multis": {"Ruby": 6, "Sapphire": 3, "Diamond": 3}}, 
     "Ion": {"Multis": {"Jade": 4, "Ruby": 2, "Emerald": 10, "Sapphire": 1.4, "Diamond": 5, "Starlight": 5}}, 
     "Uranium": {"Multis": {"Crystal": 100, "Sapphire": 60, "Starlight": 5, "Ion": 2.2}}, 
     "Bismuth": {"Multis": {"Ruby": 50, "Emerald": 25, "Sapphire": 12, "Diamond": 3, "Ion": 2.5, "Uranium": 2}} , 
     "Boracite": {"Multis": {"Starlight": 5, "Uranium": 3, "Bismuth": 1.5}}, 
     "Nissonite": {"Multis": {"Obsidian": 5, "Bismuth": 2.75, "Boracite": 2.25}}, 
     "Orpiment": {"Multis": {"Cash": 23, "Multiplier": 22, "Rebirths": 21, "Stone": 20, "White Gems": 19, "Crystal": 18, "Iron": 17, "Gold": 16, "Quartz": 15, "Jade": 14, "Obsidian": 13, "Ruby": 12, "Emerald": 11, "Sapphire": 10, "Diamond": 9, "Starlight": 8, "Ion": 7, "Uranium": 6, "Bismuth": 5, "Boracite": 4, "Nissonite": 3}}, 
     "Tetra": {"Multis": {"Diamond": 1e4, "Boracite": 30, "Nissonite": 10, "Orpiment": 2.5}}, 
     "Volt": {"Multis": {"Uranium": 100, "Nissonite": 4, "Tetra": 2}}, 
     "Aquamarine": {"Multis": {"Obsidian": 1e6, "Ion": 500, "Uranium": 400, "Nissonite": 5, "Volt": 2.1}}, 
     "Lollipop": {"Multis": {"Emerald": 8152, "Sapphire": 4096, "Diamond": 2048, "Starlight": 1024, "Ion": 512, "Uranium": 256, "Bismuth": 128, "Boracite": 64, "Nissonite": 32, "Orpiment": 16, "Tetra": 8, "Volt": 4, "Aquamarine": 2}}, 
     "C0RR8PT10N": {"Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6, "Gold": 6, "Quartz": 6, "Jade": 6, "Obsidian": 6, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 6, "Starlight": 6, "Ion": 6, "Uranium": 6, "Bismuth": 6, "Boracite": 6, "Nissonite": 6, "Orpiment": 2.3, "Tetra": 6, "Volt": 6, "Aquamarine": 4, "Lollipop": 3}}, 
     "Stargazed Metal": {"Multis": {"Cash": 1e100, "Multiplier": 1e100, "Rebirths": 1e100, "Stone": 1e100, "White Gems": 1e100, "Crystal": 1e100, "Iron": 1e100, "Gold": 1e100, "Quartz": 1e100, "Jade": 1e100, "Obsidian": 7.5, "Ruby": 7.5, "Emerald": 7.5, "Aquamarine": 2.25, "Lollipop": 2.25, "C0RR8PT10N": 3}}, 
     "Gyge": {"Multis": {"Ruby": 1e25, "Emerald": 1e25, "Sapphire": 1e25, "Diamond": 1e25, "Starlight": 1e25, "Ion": 1e25, "Uranium": 1e25, "Bismuth": 1e25, "Boracite": 1e25, "Nissonite": 1e25, "Volt": 18, "Lollipop": 7, "C0RR8PT10N": 10, "Stargazed Metal": 2}}, 
     "Auly Plate": {"Multis": {"Cash": Mantissa(1,288290), "Orpiment": 1.61, "Tetra": 3.12, "Volt": 6.25, "Aquamarine": 12.5, "Lollipop": 18, "C0RR8PT10N": 50, "Stargazed Metal": 5, "Gyge": 2}}, 
     "Shell Piece": {"Multis": {"Cash": 1e75, "Multiplier": 1e75, "Rebirths": 1e75, "Stone": 1e75, "White Gems": 1e75, "Crystal": 1e75, "Iron": 1e75, "Gold": 1e75, "Quartz": 1e75, "Jade": 1e75, "Obsidian": 1e75, "Ruby": 1e75, "Emerald": 1e75, "Sapphire": 1e75, "Diamond": 1e75, "Starlight": 1e75, "Ion": 1e75, "Uranium": 1e75, "Bismuth": 1e75, "Boracite": 1e75, "Nissonite": 1e75, "Orpiment": 1e75, "Tetra": 100, "Volt": 100, "Aquamarine": 100, "Lollipop": 100, "C0RR8PT10N": 100, "Mint": 100, "Gems": 20, "Metal": 100, "Press": 100, "Microparticles": 100, "Star": 100, "Robot": 100, "Prototype": 100}}, 
     "Singularity": {"Multis": {"Cash": Mantissa(1,987654321), "Volt": 1200, "C0RR8PT10N": 150, "Gyge": 4, "Auly Plate": 2.5, "Gems": 75}}, 
     "Capsuled Singularity": {"Multis": {"Cash": Mantissa(1,303030303), "Ruby": Mantissa(1,266664), "Emerald": Mantissa(1,266664), "Sapphire": Mantissa(1,266664), "Diamond": Mantissa(1,266664), "Starlight": Mantissa(1,133337), "Ion": Mantissa(1,666666), "Uranium": Mantissa(1,333333), "Bismuth": Mantissa(1,12555), "Boracite": Mantissa(1,5555), "Nissonite": Mantissa(1,2222), "Orpiment": Mantissa(1,1000), "Tetra": Mantissa(1,500), "Volt": 1e150, "Aquamarine": 1e75, "Lollipop": 1e25, "C0RR8PT10N": 1e6, "Stargazed Metal": 2500, "Gyge": 500, "Auly Plate": 25, "Shell Piece": 2.5, "Prototype": 1240, "Gems": 300}, "Recipe": {"Shell Piece": 5, "Prime Alpha Key": 1, "Singularity": 1, "Shroomite Bar": 2.5e23, "Gems": 1e36}}, 
     "Gems": {"Multis": None}, 
     "Event Power": {"Multis": None},
     "Mint": {"Multis": {"Multiplier": 1.5, "Rebirths": 1.3}},
     "Metal": {"Multis": {"Iron": 1.2, "Gold": 1.1}},
     "Press": {"Multis": {"Iron": 1.7, "Gold": 1.5, "Metal": 1.5}},
     "Microparticles": {"Multis": {"White Gems": 4, "Iron": 3, "Gold": 2, "Quartz": 1.1, "Metal": 1.3, "Press": 1.5}},
     "Star": {"Multis": {"Cash": 1.5, "Multiplier": 1.5, "Rebirths": 1.5, "Stone": 1.5, "White Gems": 1.5, "Iron": 1.5, "Gold": 1.5, "Quartz": 1.5, "Diamond": 1.2, "Starlight": 1.3, "Press": 1.5, "Microparticles": 2}},
     "Robot": {"Multis": {"Stone": 12, "Crystal": 7, "Iron": 5, "Gold": 3, "Quartz": 2, "Jade": 1.3, "Metal": 1.25, "Press": 1.25, "Microparticles": 1.25, "Star": 2}},
     "Prototype": {"Multis": {"Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Robot": 2}}},
    "Mastery": {
        "Master Cash": {"Multis": {"Cash": 2}},
        "Master Multiplier": {"Multis": {"Multiplier": 2}},
        "Master Rebirths": {"Multis": {"Rebirths": 2, "Master Multiplier": 2}},
        "Master Stone": {"Multis": {"Stone": 2, "Master Cash": 1, "Master Rebirths": 1.75}},
        "Master White Gems": {"Multis": {"White Gems": 2, "Master Multiplier": 1.5, "Master Stone": 2}},
        "Master Crystal": {"Multis": {"Crystal": 2, "Master Cash": 1.5, "Master Multiplier": 1.5, "Master Rebirths": 1.5, "Master Stone": 1.5, "Master White Gems": 1.5}},
        "Master Iron": {"Multis": {"Iron": 2, "Master Cash": 2, "Master White Gems": 1.75, "Master Crystal": 2.5}},
        "Master Gold": {"Multis": {"Gold": 2, "Master Cash": 2, "Master Rebirths": 3, "Master White Gems": 2, "Master Iron": 2}},
        "Master Quartz": {"Multis": {"Quartz": 2, "Master Cash": 5, "Master Multiplier": 5, "Master Rebirths": 5, "Master Stone": 4, "Master Crystal": 2.2, "Master Iron": 1.8, "Master Gold": 3}},
        "Master Jade": {"Multis": {"Jade": 2, "Master Cash": 10, "Master Multiplier": 10, "Master Crystal": 5, "Master Iron": 4, "Master Quartz": 2}},
        "Master Obsidian": {"Multis": {"Obsidian": 2, "Master Stone": 5, "Master White Gems": 5, "Master Iron": 5, "Master Quartz": 3, "Master Jade": 2}},
        "Master Ruby": {"Multis": {"Ruby": 2, "Master Cash": 2.25, "Master Multiplier": 2.25, "Master Rebirths": 2.25, "Master Stone": 2.25, "Master White Gems": 2.25, "Master Crystal": 2.25, "Master Iron": 2.25, "Master Gold": 2.25, "Master Quartz": 2.25, "Master Jade": 2.25, "Master Obsidian": 2.25}},
        "Master Emerald": {"Multis": {"Emerald": 2, "Master Cash": 2, "Master Multiplier": 2, "Master Rebirths": 2, "Master Stone": 2, "Master White Gems": 2, "Master Crystal": 2, "Master Iron": 2, "Master Gold": 2, "Master Quartz": 2, "Master Jade": 2, "Master Obsidian": 2, "Master Ruby": 2}},
        "Master Sapphire": {"Multis": {"Sapphire": 2, "Master Cash": 1.75, "Master Multiplier": 1.75, "Master Rebirths": 1.75, "Master Stone": 1.75, "Master White Gems": 1.75, "Master Crystal": 1.75, "Master Iron": 1.75, "Master Gold": 1.75, "Master Quartz": 1.75, "Master Jade": 1.75, "Master Obsidian": 1.75, "Master Ruby": 1.75, "Master Emerald": 1.75}},
        "Master Diamond": {"Multis": {"Diamond": 2, "Master Cash": 6, "Master Multiplier": 6, "Master White Gems": 6, "Master Crystal": 6, "Master Gold": 6, "Master Quartz": 6, "Master Ruby": 3.33, "Master Emerald": 3.33, "Master Sapphire": 3.33}},
        "Master Starlight": {"Multis": {"Starlight": 2, "Master Cash": 66, "Master Multiplier": 66, "Master Rebirths": 66, "Master Stone": 15, "Master White Gems": 15, "Master Crystal": 15, "Master Iron": 15, "Master Gold": 15, "Master Quartz": 15, "Master Jade": 15, "Master Ruby": 6, "Master Ruby": 6, "Master Sapphire": 2.7, "Master Diamond": 2.5}},
        "Master Ion": {"Multis": {"Ion": 2, "Master Obsidian": 2, "Master Ruby": 3, "Master Emerald": 3.5, "Master Sapphire": 3, "Master Diamond": 2, "Master Starlight": 5}},
        "Master Uranium": {"Multis": {"Uranium": 2, "Master Quartz": 10, "Master Jade": 9, "Master Obsidian": 8, "Master Ruby": 7, "Master Emerald": 6, "Master Sapphire": 5, "Master Diamond": 4, "Master Starlight": 3, "Master Ion": 2}},
        "Master Bismuth": {"Multis": {"Bismuth": 2, "Master Cash": 150, "Master Multiplier": 150, "Master Rebirths": 150, "Master Diamond": 7, "Master Ion": 5, "Master Uranium": 3}},
        "Master Boracite": {"Multis": {"Boracite": 2, "Master Sapphire": 7, "Master Diamond": 6, "Master Starlight": 5, "Master Ion": 4, "Master Uranium": 3, "Master Bismuth": 2}},
        "Master Nissonite": {"Multis": {"Nissonite": 2, "Master Cash": 4, "Master Multiplier": 4, "Master Rebirths": 4, "Master Stone": 4, "Master White Gems": 4, "Master Crystal": 4, "Master Iron": 4, "Master Gold": 4, "Master Quartz": 4, "Master Jade": 4, "Master Obsidian": 4, "Master Ruby": 4, "Master Emerald": 4, "Master Sapphire": 4, "Master Diamond": 4, "Master Starlight": 4, "Master Ion": 4, "Master Uranium": 4, "Master Bismuth": 3, "Master Boracite": 2}},
        "Master Orpiment": {"Multis": {"Opriment": 2, "Master Cash": 1e10, "Master Multiplier": 1e10, "Master Rebirths": 1e10, "Master Obsidian": 100, "Master Diamond": 10, "Master Uranium": 3, "Master Bismuth": 2, "Master Boracite": 3, "Master Nissonite": 2}},
        "Master Tetra": {"Multis": {"Tetra": 2, "Master Multiplier": 2.5, "Master Stone": 2.5, "Master Crystal": 2.5, "Master Gold": 2.5, "Master Jade": 2.5, "Master Ruby": 2.5, "Master Sapphire": 2.5, "Master Starlight": 2.5, "Master Uranium": 2.5, "Master Boracite": 2.5, "Master Orpiment": 2.5}},
        "Master Volt": {"Multis": {"Volt": 2, "Master Cash": 25, "Master Multiplier": 24, "Master Rebirths": 23, "Master Stone": 22, "Master White Gems": 21, "Master Crystal": 20, "Master Iron": 19, "Master Gold": 18, "Master Quartz": 17, "Master Jade": 16, "Master Obsidian": 15, "Master Ruby": 14, "Master Emerald": 13, "Master Sapphire": 12, "Master Diamond": 11, "Master Starlight": 10, "Master Ion": 9, "Master Uranium": 8, "Master Bismuth": 7, "Master Boracite": 6, "Master Nissonite": 5, "Master Orpiment": 4, "Master Tetra": 3}},
        "Master Aquamarine": {"Multis": {"Aquamarine": 2, "Master Obsidian": 25, "Master Emerald": 6, "Master Sapphire": 12, "Master Diamond": 16, "Master Ion": 7, "Master Bismuth": 15, "Master Nissonite": 10, "Master Volt": 2}},
        "Master Lollipop": {"Multis": {"Lollipop": 2, "Master Gold": 500, "Master Quartz": 400, "Master Jade": 300, "Master Obsidian": 200, "Master Ruby": 100, "Master Starlight": 50, "Master Ion": 40, "Master Uranium": 20, "Master Bismuth": 10, "Master Orpiment": 5, "Master Tetra": 4, "Master Volt": 3, "Master Aquamarine": 2}},
        "Prime Alpha Key": {"Multis": {"Master Cash": 2, "Master Multiplier": 2, "Master Rebirths": 2, "Master Stone": 2, "Master White Gems": 2, "Master Crystal": 2, "Master Iron": 2, "Master Gold": 2, "Master Quartz": 2, "Master Jade": 2, "Master Obsidian": 2, "Master Ruby": 2, "Master Emerald": 2, "Master Sapphire": 2, "Master Diamond": 2, "Master Starlight": 2, "Master Ion": 2, "Master Uranium": 2, "Master Bismuth": 2, "Master Boracite": 2, "Master Nissonite": 2, "Master Orpiment": 2, "Master Tetra": 2, "Master Volt": 2, "Master Aquamarine": 2, "Master Lollipop": 2, "Master Mint": 2, "Master Gems": 2, "Master Event Power": 2}},
        "Master Mint": {"Multis": {"Mint": 2, "Master Rebirths": 100}},
        "Master Gems": {"Multis": {"Gems": 2}},
        "Master Event Power": {"Multis": {"Event Power": 2}}
    },
    "Extra": {
        "Buttons Pressed": {"Multis": None}, 
        "Geodes Opened": {"Multis": None}},
    "Craftable": {
        "Rune": {"Multis": {"Cash": 16, "Multiplier": 13, "Rebirths": 10, "Stone": 6}, "Recipe": {"Rebirths": 5e29, "Stone": 150}},
        "Ultrabirth": {"Multis": {"Cash": 8}, "Recipe": {"Cash": 1e30, "Rebirths": 10}},
        "Cosmic Crystal": {"Multis": {"Rebirths": 8, "Stone": 8, "White Gems": 6}, "Recipe": {"Rebirths": 1e27, "White Gems": 250000, "Crystal": 2}},
        "Abstract Bar": {"Multis": None, "Recipe": {"Iron": Mantissa(1,5000), "Tetra": 1e32, "Rune": 10, "Cosmic Crystal": 1}},
        "Chlorophyte": {"Multis": {"Starlight": 3, "Ion": 2}, "Recipe": {"Stone": Mantissa(5, 2500), "Uranium": Mantissa(7,777), "Boracite": Mantissa(5,555)}},
        "Chlorophyte Bar": {"Multis": {"Volt": 10, "Aquamarine": 3}, "Recipe": {"Abstract Bar": 1e15, "Chlorophyte": 1e6, "Lollipop": 1000}},
        "Shroomite Bar": {"Multis": {"Cash": 8, "Multiplier": 8, "Rebirths": 8, "Stone": 8, "White Gems": 8, "Crystal": 8, "Iron": 8, "Gold": 8, "Quartz": 8, "Jade": 8, "Obsidian": 8, "Ruby": 8, "Emerald": 8, "Sapphire": 8, "Diamond": 8, "Starlight": 8, "Ion": 8, "Uranium": 8, "Bismuth": 8, "Boracite": 8, "Nissonite": 8, "Orpiment": 8, "Tetra": 8, "Volt": 8, "Aquamarine": 8, "Lollipop": 4}, "Recipe": {"Abstract Bar": 1e16, "Chlorophyte Bar": 10, "C0RR8PT10N": 1}},
        "Sigil of The Unknown": {"Multis": {"Orpiment": 1e7, "Tetra": 1e7, "Volt": 1e7, "Aquamarine": 10000, "Lollipop": 100, "C0RR8PT10N": 10}, "Recipe": {"Gems": 5e18, "C0RR8PT10N": 5, "Mint": 1e30, "Master Lollipop": 10, "Master Mint": 1.25e7, "Rune": Mantissa(1,303), "Ultrabirth": Mantissa(1,303), "Shroomite Bar": 1, "Sloth": 1, "ARG": 1, "Meridianiite": 1, "Neuron": 100, "Volcanic Molybdenum": 3, "Osmium": 10, "Sphene": 3, "Talc": 1, "Equinox": 1, "Molybendum": 1}},
        "King Crystal": {"Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 15, "Stone": 15, "White Gems": 15, "Crystal": 15, "Iron": 15, "Gold": 15, "Quartz": 15, "Jade": 15, "Obsidian": 15, "Ruby": 15, "Emerald": 15, "Sapphire": 15, "Diamond": 15, "Starlight": 15, "Ion": 15, "Uranium": 15, "Bismuth": 15, "Boracite": 15, "Nissonite": 15, "Orpiment": 15, "Tetra": 15, "Volt": 15, "Aquamarine": 15, "Lollipop": 15, "C0RR8PT10N": 5}, "Recipe": {"Gems": 1e18, "Witherite": 1, "Antimony": 1, "Biotite": 1, "Red Quartz": 1, "Iridium": 1, "Possessed Quartz": 1, "Oortodium": 1, "Amethyst": 750, "Paradoxite": 2, "Grail": 1000, "Mythril": 1, "Opal": 2, "Uzik": 2, "Tungsten": 30, "Heazlewoodite": 10, "Dragonglass": 25, "Prismarine": 5, "Garnet": 2, "Grandidierite": 2}},
        "Anomaly": {"Multis": {"Cash": 0.1, "Multiplier": 0.1, "Rebirths": 0.1, "Stone": 0.1, "White Gems": 0.1, "Crystal": 0.1, "Iron": 0.1, "Gold": 0.1, "Quartz": 0.1, "Jade": 0.1, "Obsidian": 0.1, "Ruby": 0.1, "Emerald": 0.1, "Sapphire": 0.1, "Diamond": 0.1, "Starlight": 0.1, "Ion": 0.1, "Uranium": 0.1, "Bismuth": 0.1, "Boracite": 0.1, "Nissonite": 0.1, "Orpiment": 3000, "Tetra": 500, "Volt": 5000, "Aquamarine": 50000, "Lollipop": 100000, "C0RR8PT10N": 2500, "Gems": 15, "Mint": 100}, "Recipe": {"Gems": 1e18, "Prime Alpha Key": 1, "Prototype": 50, "Unova": 1, "Cosmic Crystal": Mantissa(1,1000), "Heavenlium": 1, "Omet": 1, "Chroma": 1, "Polybasite": 1, "Mortalstone": 3, "Rune": 6, "Cloom": 3, "Wicked Branch": 1000, "Megabasite": 1}},
        "Timeless Quartz": {"Multis": {"Cash": 1e33, "Multiplier": 1e33, "Rebirths": 1e33, "Stone": 1e33, "White Gems": 1e33, "Crystal": 1e33, "Iron": 1e33, "Gold": 1e33, "Quartz": Mantissa(1,303), "Jade": 1e33, "Obsidian": 1e33, "Ruby": 1e33, "Emerald": 1e33, "Sapphire": 1e33, "Diamond": 1e33, "Starlight": 1e33, "Ion": 1e33, "Uranium": 1e33, "Bismuth": 1e33, "Boracite": 1e33, "Nissonite": 1e33, "Orpiment": 1e30, "Tetra": 1e26, "Volt": 1e21, "Aquamarine": 1e15, "Lollipop": 1e8, "C0RR8PT10N": 50, "Stargazed Metal": 1}, "Recipe": {"Master Lollipop": 100, "Prime Alpha Key": 1, "C0RR8PT10N": 250, "Gems": 1e33, "Brookite": 1, "Wicked Branch": 1750, "Mushroom": 600, "Galarium": 7, "Zanyte": 75, "Holeyum": 1, "Quetzalcoatlite": 1, "Doomdilite": 25, "Ancar": 200, "Dime": 10, "Milky Quartz": 1, "Angelicas": 1, "Ectoplasm": 1}, "max_amount": 10}
    },
    "Exclusive": {
        "Testium": {"Multis": {"Cash": 26, "Multiplier": 25, "Rebirths": 24, "Stone": 23, "White Gems": 22, "Crystal": 21, "Iron": 20, "Gold": 19, "Quartz": 18, "Jade": 17, "Obsidian": 16, "Ruby": 15, "Emerald": 14, "Sapphire": 13, "Diamond": 12, "Starlight": 11, "Ion": 10, "Uranium": 9, "Bismuth": 8, "Boracite": 7, "Nissonite": 6, "Orpiment": 5, "Tetra": 4, "Volt": 3, "Aquamarine": 2, "Lollipop": 1}},
        "Alpha Point": {"Multis": {"Cash": 1.1, "Multiplier": 1.1, "Rebirths": 1.1}},
        "Chocolate": {"Multis": {"Leaf": 2.25, "Rebirths": 3}},
        "Moonstone": {"Multis": {"Cash": 5, "Multiplier": 5, "Rebirths": 5, "Stone": 5, "White Gems": 5, "Crystal": 5, "Iron": 5, "Gold": 5, "Quartz": 5, "Jade": 5}},
        "Blue Crystal": {"Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 5, "Stone": 2, "White Gems": 2, "Crystal": 3}},
        "???": {"Multis": {"Ruby": 10, "Emerald": 8, "Sapphire": 5, "Starlight": 2, "Ion": 1.2, "Orpiment": 96, "Tetra": 48, "Volt": 24, "Aquamarine": 12, "Lollipop": 6, "C0RR8PT10N": 3}},
        "Afkime": {"Multis": {"Cash": 15, "Multiplier": 10, "Rebirths": 10, "Bismuth": 1/1.11, "Boracite": 1.5, "Nissonite": 3, "Orpiment": 1.5, "Tetra": 1.5, "Volt": 1.35, "Aquamarine": 1.6}},
        "Oortodium": {"Multis": {"White Gems": 4, "Crystal": 5, "Iron": 3}},
        "Possessed Quartz": {"Multis": {"Cash": 20, "Crystal": 10, "Quartz": 4}},
        "Brookite": {"Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Ion": 5, "Bismuth": 5}},
        "Christite": {"Multis": {"Obsidian": 12, "Ruby": 11, "Emerald": 10, "Sapphire": 9, "Diamond": 8, "Starlight": 7, "Ion": 6, "Uranium": 5, "Bismuth": 4, "Boracite": 2}},
        "Voiridis": {"Multis": {"Cash": 0.005, "Multiplier": 0.005, "Rebirths": 0.005, "Stone": 0.05, "White Gems": 0.05, "Crystal": 0.05, "Iron": 20, "Gold": 20, "Jade": 20, "Obsidian": 5, "Diamond": 5, "Starlight": 4}},
        "12.99": {"Multis": {"Cash": 12.99, "Multiplier": 12.99, "Rebirths": 12.99, "Stone": 12.99, "White Gems": 12.99, "Crystal": 12.99, "Iron": 12.99, "Gold": 12.99, "Quartz": 12.99, "Jade": 12.99, "Obsidian": 12.99, "Ruby": 12.99, "Emerald": 12.99}},
        "Eternium": {"Multis": {"Cash": Mantissa(1,307), "Volt": 5, "Aquamarine": 5, "Lollipop": 5}},
        "Fisheode": {"Multis": {"Cash": 50, "Multiplier": 50, "Rebirths": 50, "Obsidian": 20, "Emerald": 7, "Sapphire": 3, "Diamond": 5, "Uranium": 2}},
        "Zentlyo": {"Multis": {"Bismuth": 9.6e7, "Boracite": 4.8e6, "Nissonite": 240000, "Orpiment": 12000, "Tetra": 600, "Volt": 30, "Aquamarine": 8, "Lollipop": 4, "Stargazed Metal": 3}},
        "Noirment": {"Multis": {"Solargems": 4, "Moon Cash": 200, "Scoria": 15, "Pyrite": 3}},
        "Nelhim": {"Multis": {"Booster": 3, "Reincarnation": 3, "Scoria": 3, "Baryte": 3}},
        "Banana": {"Multis": {"Penny": 3.5, "Coconut": 3.5, "Wood": 3.5, "Cobblestone": 3.5, "Coal": 3.5, "Ferrotite": 3.5, "Mesolite": 3.5, "Forsterite": 3.5, "Raspite": 3.5, "Cinnabar": 3.5, "Zircon": 3.5, "Altaite": 3.5, "Galena": 3.5, "Topaz": 3.5}},
        "Fallen": {"Multis": {"Leaf": 5, "Pine": 3, "Mushroom": 2}}
    },
    "Event": {
      "Leaf": {"Multis": None },
      "Acorn": {"Multis": { "Cash": 1.5, "Leaf": 2 } },
      "Chestnut": {"Multis": { "Multiplier": 2.2, "Acorn": 2 } },
      "Pine": {
        "Multis": { "White Gems": 3.6, "Acorn": 1.5, "Chestnut": 2.5 }
      },
      "Mushroom": {"Multis": { "Gold": 5, "Pine": 4, "Leaf": 2 } },
      "Wicked Branch": {
        "Multis": { "Jade": 15, "Chestnut": 2.5, "Mushroom": 3 }
      },
      "Candy": {"Multis": None },
      "Pumpkin": {"Multis": { "Rebirths": 1.5, "Candy": 1.25 } },
      "Bat": {
        "Multis": { "White Gems": 3, "Crystal": 2, "Pumpkins": 1.5 }
      },
      "Bone": {"Multis": {"Iron": 5, "Quartz": 2, "Candy": 2, "Bat": 2 }},
      "Clover": {"Multis": {"Cash": 1.1}},
      "Heart": {"Multis": {"Flower": 2, "Love": 1.35}},
      "Orange Pumpkin": {"Multis": {"White Gems": 1.75}},
      "Ray": {"Multis": {"Stone": 2, "White Gems": 1.1, "Sand": 1.5}},
      "Patriotic Crystal": {"Multis": {"Crystal": 2, "Ray": 2}},
      "Aureal Gem": {"Multis": {"Gold": 2.5, "Quartz": 1.8, "Sand": 3, "Patriotic Crystal": 2}},
      "Fragment": {"Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Ruby": 2, "Diamond": 1.2, "Sand": 5, "Ray": 3, "Patriotic Crystal": 2.5, "Aureal Gem": 2}}
    },
    "Secret": {
        "Sloth": {"Multis": {"Multiplier": 1.5, "Rebirths": 2}},
        "Pride": {"Multis": {"Rebirths": 3, "Crystal": 4, "Iron": 2}},
        "Gluttony": {"Multis": {"Multiplier": 5, "Stone": 4, "Gold": 2.5}},
        "Desire": {"Multis": {"Multiplier": 4, "Stone": 1.5, "White Gems": 2}},
        "Envy": {"Multis": {"Gold": 3, "Quartz": 2, "Jade": 1.2}},
        "Greed": {"Multis": {"Cash": 10, "Gems": 1.2}},
        "Wrath": {"Multis": {"Obsidian": 1.8}},
        "Xenotime": {"Multis": {"Ruby": 1000, "Ion": 16, "Nissonite": 2}},
        "Kanoite": {"Multis": {"Cash": 69, "Multiplier": 69, "Rebirths": 69, "Stone": 69, "White Gems": 69, "Crystal": 69, "Iron": 69, "Gold": 69, "Quartz": 69, "Jade": 69, "Obsidian": 69, "Ruby": 69, "Emerald": 69, "Sapphire": 69, "Diamond": 30, "Bismuth": 10, "Boracite": 5, "Nissonite": 3, "Orpiment": 2}},
        "Pigmentite": {"Multis": {"Boracite": 15, "Nissonite": 5, "Orpiment": 3, "Tetra": 1.5}},
        "Celestial": {"Multis": {"Rebirths": 1.5, "Stone": 2}},
        "Petrol": {"Multis": {"Crystal": 5}},
        "Polybasite": {"Multis": {"Cash": 1.5, "Rebirths": 3, "Stone": 2.2, "White Gems": 1.6}},
        "Megabasite": {"Multis": {"Boracite": 50, "Nissonite": 5, "Orpiment": 3, "Tetra": 3}},
        "Cytoplasm": {"Multis": {"Cash": 2, "Rebirths": 3, "Stone": 2}},
        "Red Quartz": {"Multis": {"Multiplier": 3, "Rebirths": 3, "White Gems": 2.5, "Quartz": 1.3, "Ruby": 1.15}},
        "Biotite": {"Multis": {"Cash": 5, "Rebirths": 4, "Stone": 2, "White Gems": 1.25, "Obsidian": 1.11}},
        "Pyroxene": {"Multis": {"Cash": 7.5, "Multiplier": 7.5, "Rebirths": 5, "Stone": 5, "White Gems": 2.5, "Crystal": 2.5, "Iron": 1.75}},
        "Witherite": {"Multis": {"Multiplier": 2, "Stone": 3, "White Gems": 3, "Iron": 1.5}},
        "Hardystonite": {"Multis": {"Rebirths": 2, "Stone": 3, "White Gems": 2}},
        "Meridianiite": {"Multis": {"Cash": 3, "Rebirths": 2.75, "White Gems": 2.5, "Iron": 2.25, "Gold": 2, "Quartz": 2, "Obsidian": 1.75}},
        "Confusion": {"Multis": {"Cash": 10, "Rebirths": 7.5, "White Gems": 5, "Iron": 2.5}},
        "Chroma": {"Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Crystal": 3, "Gold": 3, "Jade": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3}},
        "Iridium": {"Multis": {"Ruby": 128, "Emerald": 64, "Sapphire": 32, "Diamond": 16, "Starlight": 8, "Ion": 4, "Uranium": 2}},
        "ARG": {"Multis": {"Cash": 4, "Multiplier": 4, "Rebirths": 4, "Stone": 3, "White Gems": 3, "Iron": 3, "Gold": 1.75}},
        "Binarium": {"Multis": {"Multiplier": 1e10, "Rebirhts": 100000, "Stone": 75, "White Gems": 30, "Crystal": 30, "Iron": 10, "Gold": 5, "Quartz": 2.5, "Jade": 1.5}},
        "Malware": {"Multis": {"Cash": 4, "Multiplier": 4, "Rebirths": 4, "Stone": 4, "White Gems": 4, "Crystal": 4, "Iron": 4, "Gold": 4, "Quartz": 2.5, "Jade": 1.3}},
        "Primate": {"Multis": {"Cash": 3, "Rebirths": 2}},
        "Grass": {"Multis": {"Cash": 1.5, "Multiplier": 1.5, "Rebirths": 1.5, "Stone": 1.5, "White Gems": 1.5, "Crystal": 1.5, "Iron": 1.5, "Gold": 1.5, "Quartz": 1.5, "Jade": 1.5}},
        "Frosterial": {"Multis": {"Diamond": 8, "Uranium": 3.5, "Bismuth": 2, "Boracite": 1.75}},
        "Angelicas": {"Multis": {"Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Starlight": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2, "Orpiment": 2, "Tetra": 2, "Volt": 2, "Aquamarine": 2}},
        "Heavenlium": {"Multis": {"Bismuth": 2, "Orpiment": 2, "Volt": 1.8, "Aquamarine": 2}},
        "Antimony": {"Cash": 0.0001, "Obsidian": 100, "Ruby": 40, "Emerald": 30, "Sapphire": 20, "Diamond": 13, "Starlight": 10, "Ion": 8, "Uranium": 7, "Bismuth": 10, "Boracite": 5},
        "Painite": {"Multis": {"Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 3.5}},
        "Toxant": {"Multis": {"Jade": 30, "Emerald": 3, "Sapphire": 3, "Diamond": 4, "Diamond_2": 2, "Starlight": 2.5, "Ion": 1.5}},
        "Radiant": {"Multis": {"Sapphire": 3, "Diamond": 5, "Starlight": 3, "Ion": 1.5}},
        "Obscenium": {"Multis": {"Uranium": 20, "Bismuth": 10, "Boracite": 3, "Nissonite": 1.5}},
        "Magnetite": {"Multis": {"Boracite": 15, "Nissonite": 2, "Orpiment": 5, "Tetra": 2, "Volt": 2}},
        "Ectoplasm": {"Multis": {"Rebirths": 50, "White Gems": 25, "Quartz": 8, "Obsidian": 2}},
        "Phantoplasm": {"Multis": {"Obsidian": 99, "Nissonite": 6, "Orpiment": 3, "Mint": 5, "Gems": 2.5}},
        "Esadrhium": {"Multis": {"Boracite": 5, "Nissonite": 4, "Orpiment": 3, "Tetra": 2}},
        "Graphite": {"Multis": { "Orpiment": 4, "Tetra": 2 }},
        "Tesseract": {"Multis": {"Tetra": Mantissa(1,303), "Master Tetra": 1e30}},
        "Stellarite": {"Multis": { "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2.5 }},
        "Galaxite": {"Multis": {"Obsidian": 2.75,"Ruby": 5,"Emerald": 5,"Sapphire": 5,"Diamond": 2,"Starlight": 2}},
        "Starglass": {"Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303)}},
        "Inception": {"Multis": {"Volt": 10, "Aquamarine": 9, "Lollipop": 10, "C0RR8PT10N": 9, "Stargazed Metal": 10, "Gyge": 3, "Auly Plate": 2, "Shell Piece": 1.5}},
        "Alamost": {"Multis": {"Diamond": 10000, "Starlight": 1000, "Boracite": 400, "Nissonite": 20, "Tetra": 1.2, "Aquamarine": 5, "Lollipop": 1.5, "C0RR8PT10N": 1.3}},
        "Chromatone": {"Multis": {"Obsidian": 1e6, "Ruby": 1e6, "Emerald": 1e6, "Sapphire": 1e6, "Boracite": 100, "Orpiment": 50, "Aquamarine": 2, "Lollipop": 1.2, "C0RR8PT10N": 1.1}},
        "Paputal": {"Multis": {"Ruby": 100000, "Emerald": 100000, "Boracite": 250, "Nissonite": 10, "Orpiment": 10, "Tetra": 2, "Aquamarine": 15, "Lollipop": 3.5, "C0RR8PT10N": 2}},
        "Exodal": {"Multis": {"Cash": 1e6, "Uranium": 100000, "Bismuth": 1000, "Tetra": 1.5, "Aquamarine": 10, "Lollipop": 2, "C0RR8PT10N": 1.6}},
        "Eternabasite": {"Multis": {"Cash": Mantissa(1,3003), "Multiplier": Mantissa(1,3003), "Rebirths": Mantissa(1,3003),"Tetra": 1e9, "Volt": 1e6, "Aquamarine": 1000, "Lollipop": 100, "C0RR8PT10N": 3}},
        "Darkmatter": {"Multis": {"Obsidian": Mantissa(1,303), "Tetra": 1000000, "Volt": 10000, "Aquamarine": 100,  "Lollipop": 10,  "C0RR8PT10N": 1.2}},
        "Lightmatter": {"Multis": {"Starlight": Mantissa(1,303), "Tetra": 10000, "Volt": 1e6, "Aquamarine": 300, "Lollipop": 25, "C0RR8PT10N": 1.8}},
        "==INFINITY==": {"Multis": {"Cash": Mantissa(1,2999), "Obsidian": Mantissa(1,999), "Starlight": Mantissa(1,999), "Tetra": 9e8, "Volt": 999999, "Aquamarine": 999, "Lollipop": 99, "C0RR8PT10N": 2.99}},
        "TRU3_W0RLD": {"Multis": {"Cash": 101, "Multiplier": 101, "Rebirths": 101, "Stone": 101, "White Gems": 101, "Crystal": 101, "Iron": 101, "Gold": 101, "Quartz": 101, "Jade": 101, "Obsidian": 101, "Ruby": 101, "Emerald": 101, "Sapphire": 101, "Diamond": 101, "Starlight": 101, "Ion": 101, "Uranium": 101, "Bismuth": 101, "Boracite": 101, "Nissonite": 101, "Orpiment": 101, "Tetra": 101, "Volt": 10.1, "Aquamarine": 1.5, "Lollipop": 2, "C0RR8PT10N": 3.1}},
        "DENIAL": {"Multis": {"C0RR8PT10N": 100, "Stargazed Metal": 10, "Gyge": 2}}
    },
    "Moonbase": {
        "Moon Cash": {"Multis": None},
        "Booster": {"Multis": None},
        "Reincarnation": {"Multis": {"Booster": 2}},
        "Scoria": {"Multis": {"Booster": 1.25, "Reincarnation": 2}},
        "Brighterium": {"Multis": {"Booster": 2.5, "Scoria": 2.2}},
        "Baryte": {"Multis": {"Moon Cash": 2.5, "Brighterium": 2.5}},
        "Gypsum": {"Multis": {"Reincarnation": 2, "Baryte": 3}},
        "Pyrite": {"Multis": {"Moon Cash": 4, "Reincarnation": 2.3, "Brighterium": 3, "Baryte": 2, "Gypsum": 4}},
        "Cryon": {"Multis": {"Moon Cash": 20, "Booster": 18, "Reincarnation": 12, "Scoria": 8, "Brighterium": 4, "Baryte": 5, "Pyrite": 2}},
        "Kinetic": {"Multis": {"Moon Cash": 100000, "Booster": 1000, "Reincarnation": 1000, "Scoria": 50, "Gypsum": 30, "Cryon": 2}},
        "Plasma": {"Multis": {"Moon Cash": 95.20200650580942, "Booster": 63.09573444801933, "Reincarnation": 41.89983049571471, "Scoria": 27.85761802547598, "Brighterium": 18.520259177452136, "Baryte": 12.286035066475314, "Gypsum": 8.103282983463814, "Pyrite": 5.278031643091577, "Cryon": 3.348369522101714, "Kinetic": 2, "Ruby": 5, "Emerald": 5, "Sapphire": 5, "Diamond": 5, "Starlight": 5, "Ion": 5, "Uranium": 5, "Bismuth": 5, "Boracite": 5}},
        "Solargems": {"Multis": None}
    },
    "Secret Stats (Moonbase)": {
        "Fanite": {"Multis": {"Moon Cash": 1.2, "Booster": 1.5}},
        "Showerite": {"Multis": {"Reincarnation": 1.25, "Baryte": 1.25}},
        "Hexadron": {"Multis": {"Booster": 3, "Scoria": 1.5}},
        "Glitchared": {"Multis": {"Moon Cash": 2.5, "Booster": 2.5, "Reincarnation": 2.5, "Scoria": 1.3}},
        "Yalkènzar": {"Multis": {"Scoria": 2, "Brighterium": 1.75}},
        "Imperium": {"Multis": {"Moon Cash": 2, "Booster": 2, "Reincarnation": 2, "Brighterium": 1.25}},
        "Electron": {"Multis": {"Reincarnation": 3, "Brighterium": 1.75, "Baryte": 1.5, "Gypsum": 1.25}}
    },
    "Afterlife Domain": {
        "Mana": {"Multis": None},
        "Enchantment": {"Multis": {"Mana": 1.5}},
        "Spell": {"Multis": {"Enchatment": 1.5}}
    },
    "Afterlife Domain (Geode)": {
        "Galactic Geode": {
            "Eveslogite": {"Multis": {"Mana": 1.15}},
            "Spacelite": {"Multis": {"Mana": 1.35}},
            "Astrolite": {"Multis": {"Mana": 1.2, "Enchantment": 1}},
            "Cometium": {"Multis": {"Mana": 1.6}},
            "Planetium": {"Multis": {"Mana": 1.3, "Enchantment": 1.3}},
            "Mercury": {"Multis": {"Mana": 1.3, "Enchantment": 1.6}},
            "Saturnite": {"Multis": {"Mana": 1.75, "Enchantment": 1.5}},
            "Constellar": {"Multis": {"Mana": 2, "Spell": 1.25}},
            "Neutronium": {"Multis": {"Mana": 2.25, "Enchantment": 2.15, "Uranium": 100, "Bismuth": 50, "Boracite": 30, "Nissonite": 20, "Orpiment": 10, "Tetra": 3}},
            "Magnetar": {"Multis": {"Mana": 4, "Spell": 1.75, "Boracite": 25, "Nissonite": 25, "Orpiment": 10, "Tetra": 10, "Volt": 5}},
            "Uzoburnus": {"Mutlis": {"Mana": 2, "Spell": 2, "Boracite": 0.5, "Nissonite": 0.5, "Orpiment": 25, "Tetra": 5, "Volt": 5}}
        },
        "Artificial Geode": {
            "Bit": {"Multis": {"Mana": 1.75}},
            "Pixel": {"Multis": {"Enchantment": 1.5}},
            "Aluminium": {"Multis": {"Mana": 1.35, "Enchantment": 1.35}},
            "Nickel": {"Multis": {"Mana": 2}},
            "Zinc": {"Multis": {"Mana": 1.2, "Enchantment": 1.75}},
            "Electrolite": {"Multis": {"Spell": 1.14}},
            "Livermorium": {"Multis": {"Mana": 2.5}},
            "Gygabittium": {"Multis": {"Mana": 1.5, "Enchantment": 2}},
            "Pteracorite": {"Multis": {"Spell": 1.5}},
            "Oganesson": {"Multis": {"Mana": 2.5, "Enchantment": 2.5, "Uranium": 10000, "Bismuth": 100, "Boracite": 10, "Nissonite": 10, "Orpiment": 5, "Tetra": 3}},
            "Metactinium": {"Multis": {"Mana": 1.5, "Enchantment": 3, "Spell": 2, "Diamond": 250, "Bismuth": 123456, "Orpiment": 10, "Tetra": 3}},
            "Apatite": {"Multis": {"Mana": 3, "Spell": 2.5, "Boracite": 1000, "Nissonite": 1000, "Orpiment": 50, "Tetra": 25, "Volt": 5, "Aquamarine": 2}},
            "Unbinilium": {"Multis": {"Mana": 5, "Enchantment": 4.5, "Spell": 3, "Bismuth": 100, "Boracite": 100, "Nissonite": 100, "Orpiment": 100, "Tetra": 100, "Volt": 25, "Aquamarine": 5, "Lollipop": 2.5, "Stargazed Metal": 3.24}}
        },
        "Elemental Geode": {
            "Watercrystal": {"Multis": {"Enchantment": 2}},
            "Sandstone": {"Multis": {"Mana": 3}},
            "Firecrystal": {"Multis": {"Enchantment": 1.3, "Spell": 1.3}},
            "Leafstone": {"Multis": {"Mana": 2.35, "Enchantment": 2.35}},
            "Windirius": {"Multis": {"Mana": 2, "Spell": 1.55}},
            "Rockarnium": {"Multis": {"Mana": 4, "Enchantment": 2.5}},
            "Drakan": {"Multis": {"Spell": 1.76}},
            "Chromatite": {"Multis": {"Mana": 2.5, "Enchantment": 3}},
            "Sognus": {"Multis": {"Mana": 2, "Enchantment": 2, "Spell": 2, "Orpiment": 100, "Tetra": 10, "Volt": 2}},
            "Ambrosia": {"Multis": {"Mana": 1.5, "Enchantment": 5, "Bismuth": 100, "Boracite": 100, "Nissonite": 100, "Orpiment": 100, "Tetra": 250, "Volt": 50, "Aquamarine": 5, "Lollipop": 3}},
            "Quintessence": {"Multis": {"Mana": 7, "Enchantment": 4, "Spell": 2, "Bismuth": 1e6, "Boracite": 1e6, "Nissonite": 1e6, "Orpiment": 1000, "Tetra": 500, "Volt": 50, "Aquamarine": 15, "Lollipop": 5, "C0RR8PT10N": 2.5}}
        },
        "Awakened Geode": {
            "Silicon": {"Multis": {"Spell": 1.35}},
            "Sulfur": {"Multis": {"Mana": 3, "Enchantment": 3}},
            "Chlorine": {"Multis": {"Mana": 1.5, "Spell": 2}},
            "Bromine": {"Multis": {"Enchantment": 4}},
            "Technetium": {"Multis": {"Mana": 2.5, "Enchantment": 2, "Spell": 1.8}},
            "Scandium": {"Multis": {"Spell": 2.5}},
            "Rhodimite": {"Multis": {"Mana": 3.5, "Enchantment": 3.5}},
            "Vanadium": {"Multis": {"Enchantment": 6, "Spell": 1.5}},
            "Selenium": {"Multis": {"Mana": 5, "Spell": 3}},
            "Yttrium": {"Multis": {"Mana": 8, "Enchantment": 4, "Spell": 2}},
            "Polonium": {"Multis": {"Mana": 3, "Enchantment": 3.5, "Spell": 4, "Orpiment": 1000, "Tetra": 1000, "Volt": 25, "Aquamarine": 1.5}},
            "Krypton": {"Multis": {"Mana": 10, "Enchantment": 25, "Uranium": 1e12, "Aquamarine": 3}},
            "Aeglestone": {"Multis": {"Mana": 33, "Enchantment": 10, "Spell": 7, "Boracite": 1e9, "Nissonite": 1e9, "Orpiment": 50, "Aquamarine": 50, "Lollipop": 10, "C0RR8PT10N": 2.5}}
        },
        "Magical Geode": {
            "Arctite": {"Multis": {"Mana": 2.2, "Enchantment": 2.2, "Spell": 2.2}},
            "Cuprite": {"Multis": {"Mana": 4, "Spell": 3}},
            "Musgravite": {"Multis": {"Enchantment": 7.5, "Spell": 1.5}},
            "Kainosite": {"Multis": {"Enchantment": 2, "Spell": 3.5}},
            "Neodymium": {"Multis": {"Mana": 10, "Enchantment": 4}},
            "Beryllium": {"Multis": {"Mana": 6, "Enchantment": 5, "Spell": 4}},
            "Vergamite": {"Multis": {"Enchantment": 10, "Spell": 2.5}},
            "Quamite": {"Multis": {"Mana": 25, "Spell": 5}},
            "Astralyte": {"Multis": {"Enchantment": 7, "Spell": 7, "Bismuth": 1000, "Boracite": 1000, "Nissonite": 1000, "Orpiment": 1000, "Tetra": 25, "Volt": 25, "Aquamarine": 50, "Lollipop": 5}},
            "Unobtainium": {"Multis": {"Enchantment": 30, "Spell": 15, "Bismuth": 1e6, "Boracite": 1e6, "Nissonite": 1e6, "Orpiment": 1e6, "Tetra": 250, "Volt": 250, "Aquamarine": 100, "Lollipop": 10, "C0RR8PT10N": 2}},
            "Vibranium": {"Multis": {"Mana": 50, "Enchantment": 50, "Spell": 20, "Uranium": 1e9, "Bismuth": 1e9, "Boracite": 1e9, "Nissonite": 1e9, "Orpiment": 1e9, "Tetra": 1000, "Volt": 1000, "Aquamarine": 200, "Lollipop": 15, "C0RR8PT10N": 4, "Stargazed Metal": 1.5}},
            "Stygium": {"Multis": {"Mana": 75, "Spell": 30, "Uranium": 1000, "Bismuth": 1000, "Boracite": 1000, "Nissonite": 1000, "Orpiment": 1000, "Tetra": 1000, "Volt": 1000, "Aquamarine": 1000, "Lollipop": 25, "C0RR8PT10N": 5, "Stargazed Metal": 32.5, "Gyge": 8.23, "Auly Plate": 3.32}},
            "Kyber Crystal": {"Multis": {"Mana": 100, "Enchantment": 100, "Spell": 100, "Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Quartz": Mantissa(1,303), "Jade": Mantissa(1,303), "Obsidian": Mantissa(1,303), "Ruby": Mantissa(1,303), "Emerald": Mantissa(1,303), "Sapphire": Mantissa(1,303), "Diamond": Mantissa(1,303), "Starlight": Mantissa(1,303), "Ion": Mantissa(1,303), "Uranium": Mantissa(1,303), "Bismuth": Mantissa(1,303), "Boracite": 1e111, "Nissonite": 1e111, "Orpiment": 1e111, "Tetra": 1e33, "Volt": 1e33, "Aquamarine": 1e16, "Lollipop": 1e8, "C0RR8PT10N": 1000, "Stargazed Metal": 100000, "Gyge": 23.82, "Auly Plate": 52.3, "Shell Piece": 6.42}}
        }
    },
    "Victorious Saints (Afterlife Domain)": {
        "Aether": {"Multis": {"Mana": 16, "Enchantment": 3.8, "Spell": 6, "Orpiment": 100000, "Tetra": 1000, "Volt": 10}, "Recipe": {"Gems": 1e8, "Spell": 1e33, "Mercury": 16, "Zinc": 1000, "Windirius": 200, "Sulfur": 10000, "Bromine": 650, "Rhodimite": 12, "Selenium": 3, "Arctite": 30000, "Musgravite": 2500, "Quamite": 1}, "max_amount": 1},
        "Rainbatar": {"Multis": {"Mana": 9, "Enchantment": 9, "Spell": 9, "Uranium": 1e6, "Bismuth": 1e6, "Boracite": 1e6, "Nissonite": 1e6, "Orpiment": 10000, "Tetra": 10000, "Volt": 100, "Aquamarine": 3}, "Recipe": {"Gems": 1e12, "Mana": 1e120, "Spell": 5e42, "Cometium": 1200, "Spacelite": 15000, "Aluminium": 10000, "Zinc": 1000, "Electrolite": 150, "Watercrystal": 7500, "Firecrystal": 2500, "Technetium": 100, "Rhodimite": 24, "Beryllium": 18, "Neutronium": 2, "Polonium": 1, "Magnetar": 1}, "max_amount": 1},
        "Primordial Delight": {"Multis": {"Mana": 17, "Enchantment": 17, "Spell": 17, "Uranium": 1e6, "Bismuth": 1e6, "Boracite": 1e6, "Nissonite": 1e6, "Orpiment": 1e6, "Tetra": 1e6, "Volt": 50000, "Aquamarine": 2500, "Lollipop": 50, "C0RR8PT10N": 10}, "Recipe": {"Gems": 1e20, "Spell": 5e33, "Constellar": 3, "Uzoburnus": 1, "Zinc": 1200, "Sandstone": 8000, "Leafstone": 5000, "Rockarnium": 3, "Sognus": 1, "Chlorine": 3500, "Bromine": 810, "Rhodimite": 18, "Yttrium": 2, "Krypton": 1, "Aeglestone": 1, "Cuprite": 4000, "Kainosite": 900, "Neodymium": 175}, "max_amount": 1},
        "Xylorian": {"Multis": {"Mana": 31, "Enchantment": 31, "Spell": 31, "Cash": 1e33, "Multiplier": 1e33, "Rebirths": 1e33, "Stone": 1e33, "White Gems": 1e33, "Crystal": 1e33, "Iron": 1e33, "Gold": 1e33, "Quartz": 1e33, "Jade": 1e33, "Obsidian": 1e33, "Ruby": 1e33, "Emerald": 1e33, "Sapphire": 1e33, "Diamond": 1e33, "Starlight": 1e33, "Ion": 1e33, "Uranium": 1e6, "Bismuth": 1e6, "Boracite": 1e6, "Nissonite": 1e6, "Orpiment": 1e6, "Tetra": 100000, "Volt": 100000, "Aquamarine": 10000, "Lollipop": 500, "C0RR8PT10N": 10, "Stargazed Metal": 2.5}, "Recipe": {"Gems": 1e24, "Mana": 1e135, "Enchantment": 1e109, "Spell": 7.5e42, "Spacelite": 15000, "Aluminium": 10000, "Cuprite": 16000, "Arctite": 20000, "Watercrystal": 8000, "Cometium": 1500, "Firecrystal": 6500, "Technetium": 240, "Livermorium": 150, "Planetium": 200, "Saturnite": 20, "Drakan": 28, "Vergamite": 15, "Vanadium": 13, "Selenium": 10, "Chromatite": 6, "Constellar": 8, "Neutronium": 3, "Sognus": 5, "Krypton": 2, "Astralyte": 3, "Vibranium": 2, "Unobtainium": 3, "Quintessence": 1, "Ambrosia": 1}, "max_amount": 1},
        "Prototype_Millennial": {"Multis": {"Mana": 23, "Enchantment": 23, "Spell": 23, "Boracite": 1e9, "Nissonite": 1e9, "Orpiment": 100000, "Tetra": 10000, "Volt": 1000, "Aquamarine": 100, "Lollipop": 10, "C0RR8PT10N": 5, "Stargazed Metal": 3, "Gyge": 1.2}, "Recipe": {"Gems": 1e30, "Gygabittium": 80, "Astrolite": 3500, "Chromatite": 10, "Selenium": 35, "Bit": 75000, "Enchantment": 1e115, "Pixel": 40000, "Electrolite": 600, "Metactinium": 2, "Quamite": 8, "Oganesson": 3, "Pteracorite": 8, "Silicon": 50000, "Unbinilium": 1}, "max_amount": 1},
        "Blackholium": {"Multis": {"Mana": 70, "Enchantment": 32, "Spell": 13, "Uranium": 1e33, "Bismuth": 1e33, "Boracite": 1e33, "Nissonite": 1e33, "Orpiment": 1e33, "Tetra": 1e25, "Volt": 1e15, "Aquamarine": 1e10, "Lollipop": 10000, "C0RR8PT10N": 250, "Stargazed Metal": 5, "Gyge": 2}, "Recipe": {"Gems": 1e52, "Mana": 1e175, "Eveslogite": 1200000, "Bit": 900000, "Silicon": 850000, "Sulfur": 600000, "Pixel": 500000, "Spacelite": 420000, "Cuprite": 150000, "Aluminium": 12000, "Musgravite": 9000, "Nickel": 5000, "Zinc": 4000, "Kainosite": 3000, "Planetium": 1000, "Mercury": 300, "Rockarnium": 200, "Livermorium": 185, "Drakan": 160, "Saturnite": 90, "Vanadium": 80, "Selenium": 45, "Constellar": 17, "Neutronium": 12, "Polonium": 9, "Oganesson": 7, "Astralyte": 7, "Magnetar": 6, "Sognus": 6, "Krypton": 3, "Unobtainium": 2, "Apatite": 2, "Ambrosia": 1}, "max_amount": 1}
    },
    "Geode": {"Stone Geode": {
        "Dezyp": {"Chance": 12000, "Multis": {"Cash": 15, "Rebirths": 20, "Stone": 2, "White Gems": 2}},
        "Podrillium": {"Chance": 1000000000, "Multis": {"Cash": Mantissa(1,3003), "Multiplier": Mantissa(1,3003), "Rebirths": Mantissa(1,3003), "Stone": Mantissa(1,3003), "White Gems": Mantissa(1,3003), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Jade": Mantissa(1,303), "Obsidian": 1e200, "Ruby": 1e200, "Emerald": 1e200, "Sapphire": 1e200, "Diamond": 1e100, "Starlight": 1e100, "Ion": 1e100, "Uranium": 1e100, "Bismuth": 1e50, "Boracite": 1e50, "Nissonte": 1e50, "Orpiment": 1e25, "Tetra": 1e20, "Volt": 1e15, "Aquamarine": 1e10, "Lollipop": 10000, "C0RR8PT10N": 10, "Stargazed Metal": 5, "Gyge": 4, "Auly Plate": 3, "Shell Piece": 2}} #Podrillium is real guys!!! Trust!!!
      },
      "White Gems Geode": {
          "Digenite": {"Chance": 100, "Multis": {"Cash": 4, "Stone": 6}},
          "Oneillite": {"Chance": 500, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 4, "Stone": 2, "White Gems": 1.25}},
          "Alum": {"Chance": 13000, "Multis": {"Stone": 12, "White Gems": 1.8, "Crystal": 1.14}},
          "Chaoite": {"Chance": 273000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6}},
          "Stone 2": {"Chance": 3000000, "Multis": {"Cash": 222222,"Rebirths": 22222,"Stone": 2222, "White Gems": 222, "Crystal": 22.2, "Iron": 12.22, "Gold": 2.22, "Quartz": 1.22}},
          "Loocasium": {"Chance": 9000000, "Multis": {"Gold": 10, "Quartz": 4, "Jade": 2, "Obsidian": 1}},
          "Stone 3": {"Chance": 25000000, "Multis": {"Cash": 3333333333, "Rebirths": 33333333, "Stone": 3333333, "White Gems": 333333, "Crystal": 33333, "Iron": 3333, "Gold": 333.3, "Quartz": 33.33, "Jade": 13.33, "Obsidian": 3.33, "Ruby": 1.33}},
          "Skilltriix": {"Chance": 101101101, "Multis": {"Cash": 1e101, "Stone": 101101101101101101, "White Gems": 101101101101, "Gold": 101101101, "Obsidian": 101101, "Ruby": 101101, "Emerald": 101101, "Sapphire": 101101, "Uranium": 101, "Orpiment": 10.1, "Aquamarine": 1.1, "Lollipop": 1.01, "Stargazed Metal": 10.1, "Gyge": 1.01}},
          "Hyka Gem": {"Chance": 200000000, "Multis": {"Cash": 1e200, "Stone": 1e100, "White Gems": Mantissa(1,303), "Crystal": 1e25, "Iron": 1e12, "Gold": 5e11, "Quartz": 2.5e11, "Jade": 1.25e11, "Obsidian": 6.25e10, "Ruby": 3.125e10, "Emerald": 1.55e10, "Sapphire": 7.5e9, "Diamond": 3.75e9, "Starlight": 1.75e9, "Ion": 8.5e8, "Uranium": 10000, "Bismuth": 5000, "Boracite": 1000, "Nissonite": 500, "Orpiment": 100, "Tetra": 50, "Volt": 10, "Aquamarine": 5, "Lollipop": 2, "Stargazed Metal": 10, "Gyge": 5, "Auly Plate": 2}},
      },
      "Crystal Geode": {
          "Amethyst": {"Chance": 333, "Multis": {"Stone": 6, "White Gems": 4, "Crystal": 3}},
          "Paradoxite": {"Chance": 65000, "Multis": {"Cash": 44, "Multipliers": 55, "Rebirths": 66, "Stone": 77, "White Gems": 88, "Crystal": 30, "Iron": 5}},
      },
      "Iron Geode": {
          "Silver": {"Chance": 142, "Multis": {"Multiplier": 10, "White Gems": 5, "Iron": 2}},
          "Platinum": {"Chance": 32000, "Multis": {"White Gems": 10, "Crystal": 20, "Iron": 15, "Gold": 3, "Quartz": 2}},
          "Mythril": {"Chance": 2000000, "Multis": {"Cash": 999, "Crystal": 5, "Iron": 10, "Gold": 50, "Quartz": 100}}
      },
      "Gold Geode": {
          "Yellow Beryl": {"Chance": 6666, "Multis": {"Crystal": 15, "Gold": 3}},
          "Opal": {"Chance": 51000, "Multis": {"Cash": 8, "Multiplier": 8, "Rebirths": 8, "Crystal": 8, "Gold": 8, "Jade": 8, "Ruby": 1.3, "Sapphire": 1.3, "Diamond": 1.3}},
          "Holeyum": {"Chance": 2750000, "Multis": {"Rebirths": 1000, "White Gems": 1000, "Crystal": 500, "Iron": 500, "Gold": 300}}
      },
      "Quartz Geode": {
          "Pink Quartz": {"Chance": 50, "Multis": {"Crystal": 10, "Quartz": 3}},
          "Cyan Quartz": {"Chance": 166, "Multis": {"Rebirths": 10, "Crystal": 10, "Quartz": 4}},
          "Black Quartz": {"Chance": 2500, "Multis": {"Stone": 10, "White Gems": 10, "Iron": 10, "Quartz": 5}},
          "Garnet": {"Chance": 23000, "Multis": {"Gold": 30, "Quartz": 15, "Jade": 10, "Obsidian": 5}},
          "Milky Quartz": {"Chance": 800000, "Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 100, "White Gems": 100, "Crystal": 10, "Iron": 100, "Gold": 10, "Quartz": 100, "Jade": 10, "Obsidian": 100}}
      },
      "Jade Geode": {
          "Jurite": {"Chance": 20, "Multis": {"Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3}},
          "Molybendum": {"Chance": 23000, "Multis": {"Stone": 1000, "White Gems": 1000, "Iron": 1000, "Quartz": 1000}},
          "Rbadam's Smokestackite": {"Chance": 100000, "Multis": {"Gold": 44,"Quartz": 33," Jade": 22, "Obsidian": 11, "Ruby": 1.1}}
      },
      "Emoji Geode": {
          ":3": {"Chance": 2, "Multis": {"Quartz": 2}},
          "O_O": {"Chance": 100, "Multis": {"Quartz": 5, "Jade": 2}},
          "^_^": {"Chance": 2000, "Multis": {"Multiplier": 1.1, "Rebirths": 2.2, "Stone": 3.3, "White Gems": 4.4, "Crystal": 5.5, "Iron": 6.6, "Gold": 7.7, "Quartz": 8.8}},
          "'-'": {"Chance": 12000, "Multis": {"Iron": 1.1, "Gold": 1.1, "Quartz": 1.1, "Jade": 1.1, "Obsidian": 1.1}},
          ":D": {"Chance": 35000, "Multis": {"Jade": 5, "Obsidian": 3, "Ruby": 2}},
          "OwO": {"Chance": 150000, "Multis": {"Gold": 5.5, "Emerald": 5.5}},
          "UwU": {"Chance": 1000000, "Multis": {"Gold": 6.5, "Quartz": 6.5, "Jade": 6.5, "Obsidian": 6.5, "Ruby": 5.4, "Emerald": 4.3, "Sapphire": 3.2, "Diamond": 2.1}}
      },
      "Obsidian Geode": {
          "Draconite": {"Chance": 100, "Multis": {"Crystal": 10, "Obsidian": 2}},
          "Burneite": {"Chance": 400, "Multis": {"Cash": 7, "Multiplier": 7, "Rebirths": 7, "Stone": 7, "White Gems": 7, "Crystal": 7, "Iron": 7, "Gold": 7, "Quartz": 7, "Jade": 7}},
          "Dragonglass": {"Chance": 6666, "Multis": {"Crystal": 25, "Quartz": 15, "Jade": 10, "Obsidian": 5}},
          "Hellyerite": {"Chance": 47000, "Multis": {"Obsidian": 10, "Ruby": 3}},
          "Palladium": {"Chance": 350000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6, "Gold": 6, "Jade": 6, "Obsidian": 6, "Ruby": 6, "Gems": 1.5}},
          "Osumillite": {"Chance": 4200000, "Multipliers": {"Cash": 6544, "Gold": 50, "Quartz": 40, "Jade": 30, "Obsidian": 20, "Ruby": 10}}
      },
      "Ruby Geode": {
          "Pascoite": {"Chance": 666, "Multis": {"Obsidian": 3, "Ruby": 2}},
          "Roselite": {"Chance": 3333, "Multis": {"Jade": 5, "Obsidian": 5, "Ruby": 3}},
          "Wulfenite": {"Chance": 50000, "Multis": {"Multiplier": 15, "Obsidian": 15, "Ruby": 8}}
      },
      "Emerald Geode": {
          "Olivine": {"Chance": 250, "Multis": {"Ruby": 3, "Emerald": 2}},
          "Heazlewoodite": {"Chance": 4000, "Multis": {"Obsidian": 5, "Ruby": 5, "Emerald": 3}},
          "Gaspeite": {"Chance": 35000, "Multis": {"Emerald": 15}},
          "Talc": {"Chance": 230000, "Multis": {"Cash": 15, "Jade": 15, "Emerald": 15}}
      },
      "Sapphire Geode": {
          "Lapis": {"Chance": 142, "Multis": {"Emerald": 3, "Sapphire": 2}},
          "Ringwoodite": {"Chance": 2000, "Multis": {"Ruby": 5, "Emerald": 5, "Sapphire": 3}},
          "Kyanite": {"Chance": 15000, "Multis": {"Sapphire": 15}},
          "Azurite": {"Chance": 85000, "Multis": {"Rebirths": 15, "Crystal": 15, "Quartz": 15 ,"Sapphire": 8}},
          "Cobalt": {"Chance": 3000000, "Multis": {"Cash": 20, "Multiplier": 20, "Rebirths": 20, "Crystal": 20, "Gold": 20, "Quartz": 20, "Jade": 20, "Ruby": 20, "Emerald": 20, "Sapphire": 20}}
      },
      "Diamond Geode": {
          "Spatial Dust": {"Chance": 20, "Multis": {"Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 4, "Starlight": 2}},
          "Astrophyllite": {"Chance": 71000, "Multis": {"Gold": 80, "Jade": 30, "Obsidan": 12, "Ruby": 52, "Diamond": 20, "Starlight": 25}}
      },
      "Starlight Geode": {
          "Niter": {"Chance": 4000, "Multis": {"Starlight": 5}},
          "Yrnote": {"Chance": 80000, "Multis": {"Ruby": 10, "Emerald": 10, "Sapphire": 10, "Diamond": 20, "Starlight": 15}},
          "Sercense": {"Chance": 1400000, "Multis": {"Cash": 300, "Multiplier": 300, "Rebirths": 300, "Stone": 290, "White Gems": 280, "Crystal": 270, "Iron": 260, "Gold": 130, "Quartz": 120, "Jade": 110, "Obsidian": 100, "Ruby": 50, "Emerald": 40, "Sapphire": 30, "Diamond": 20, "Starlight": 10}}
      },
      "Ion Geode": {
          "Neuron": {"Chance": 20, "Multis": {"Starlight": 5, "Ion": 2}},
          "Antimatter": {"Chance": 45000, "Multis": {"Rebirths": 10, "Gold": 10, "Quartz": 10, "Sapphire": 10, "Diamond": 10, "Starlight": 10, "Ion": 10}}
      },
      "Uranium Geode": {
          "Sphene": {"Chance": 3, "Multis": {"Diamond": 5}},
          "Acid": {"Chance": 20, "Multis": {"Uranium": 1.4, "Starlight": 2}},
          "Niflhemite": {"Chance": 100, "Multis": {"Multiplier": 3, "Rebirths": 3, "White Gems": 3, "Quartz": 3, "Obsidian": 3, "Ruby": 3, "Diamond": 3, "Uranium": 3}},
          "Reactivite": {"Chance": 27500, "Multis": {"Starlight": 12, "Ion": 8, "Uranium": 5}},
          "Plutonerite": {"Chance": 125000, "Multis": {"Diamond": 80, "Starlight": 40, "Ion": 20, "Uranium": 10}}
      },
      "Sacred Geode": {
          "Grail": {"Chance": 2, "Multis": {"Starlight": 2, "Ion": 2, "Uranium": 2}},
          "Box": {"Chance": 3500000, "Multis": {"Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Bismuth": 3, "Boracite": 3}}
      },
      "Bismuth Geode": {
          "Lead": {"Chance": 2, "Multis": {"Iron": 10000, "Obsidian": 5, "Ruby": 5, "Emerald": 5, "Sapphire": 5, "Diamond": 5}},
          "Pseudomalachite": {"Chance": 10, "Multis": {"Diamond": 6, "Uranium": 2, "Bismuth": 1.15}},
          "Osmium": {"Chance": 1428, "Multis": {"Bismuth": 5}},
          "Yhed": {"Chance": 45000, "Multis": {"Cash": 80000, "Rebirths": 80000, "White Gems": 80000, "Iron": 80000, "Quartz": 800, "Obsidian": 800, "Emerald": 8, "Diamond": 8, "Ion": 8, "Bismuth": 8}},
          "Hexaferrum": {"Chance": 300000, "Multis": {"Ruby": 3000, "Emerald": 2000, "Sapphire": 1000, "Diamond": 160, "Uranium": 40, "Bismuth": 15, "Boracite": 3}}
      },
      "Boracite Geode": {
          "Spectrolite": {"Chance": 4000, "Multis": {"Starlight": 5, "Ion": 5, "Bismuth": 5, "Boracite": 3}},
          "Hectam": {"Chance": 25000, "Multis": {"Crystal": 100, "Quartz": 100, "Jade": 100, "Ruby": 100, "Emerald": 100, "Diamond": 100, "Boracite": 10}}
      },
      "Nissonite Geode": {
          "Frostone": {"Chance": 1250, "Multis": {"Rebirths": 15, "Crystal": 15, "Quartz": 15, "Sapphire": 15, "Diamond": 15, "Boracite": 15, "Nissonite": 4, "Mint": 1.04}},
          "Neptunian": {"Chance": 6666, "Multis": {"Cash": 2, "Multiplier": 3, "Rebirths": 30, "Ion": 1.5, "Uranium": 2, "Bismuth": 3, "Boracite": 30, "Nissonite": 10}},
          "Clouminance": {"Chance": 19000, "Multis": {"Diamond": 100, "Starlight": 100, "Ion": 100, "Boracite": 100, "Nissonite": 20}},
          "Galarium": {"Chance": 600000, "Multis": {"Diamond": 300, "Starlight": 300, "Nissonite": 45}},
          "Unova": {"Chance": 5000000, "Multis": {"Cash": 1111, "Multiplier": 1111, "Rebirths": 1111, "Stone": 1111, "White Gems": 1111, "Crystal": 1111, "Iron": 1111, "Gold": 1111, "Quartz": 1111, "Jade": 1111, "Obsidian": 1111, "Ruby": 1111, "Emerald": 1111, "Sapphire": 1111, "Diamond": 1111, "Starlight": 1111, "Ion": 1111, "Uranium": 1111, "Bismuth": 1111, "Boracite": 1111, "Nissonite": 111, "Orpiment": 7, "Mint": 11.1, "Gems": 1.1}}
      },
      "Orpiment Geode": {
          "Borax": {"Chance": 3, "Multis": {"Boracite": 20}},
          "Axiom": {"Chance": 10, "Multis": {"Boracite": 15, "Nissonite": 10}},
          "Vergemite": {"Chance": 33, "Multis": {"Bismuth": 25, "Orpiment": 1.01}},
          "Zanyte": {"Chance": 13000, "Multis": {"Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 10, "Ruby": 10, "Emerald": 10, "Sapphire": 10, "Diamond": 10, "Starlight": 10, "Ion": 10, "Uranium": 10, "Bismuth": 10, "Boracite": 10, "Nissonite": 10, "Orpiment": 4}},
          "Secretum": {"Chance": 100000, "Multis": {"Orpiment": 12}},
          "Mortalstone": {"Chance": 750000, "Multis": {"Cash": 999, "Multiplier": 999, "Rebirths": 999, "Stone": 999, "White Gems": 999, "Crystal": 999, "Iron": 999, "Gold": 999, "Quartz": 999, "Jade": 999, "Obsidian": 999, "Ruby": 999, "Emerald": 999, "Sapphire": 999, "Diamond": 999, "Starlight": 999, "Ion": 999, "Uranium": 999, "Bismuth": 999, "Boracite": 100, "Nissonite": 100, "Orpiment": 15, "Gems": 10}}
      },
      "Mint Geode": {
          "Uzik": {"Chance": 69420, "Multis": {"Jade": 10, "Mint": 5}},
          "Omet": {"Chance": 133371, "Multis": {"Cash": 100000, "Mint": 20}}
      },
      "Deepness Geode": {"Hardstone": {"Chance": 2, "Multis": {"Stone": 8, "Iron": 2}},
                          "Boomite": {"Chance": 3, "Multis": {"Stone": 15, "Crystal": 4, "Gold": 1.25}},
                          "Plutonium": {"Chance": 6, "Multis": {"Rebirths": 2, "White Gems": 4, "Metal": 1.1}},
                          "Cisophrase": {"Chance": 25, "Multis": {"Multiplier": 125, "Stone": 5, "Crystal": 1.5, "Iron": 3, "Gold": 1.2}},
                          "Anatase": {"Chance": 25000, "Multis": {"Crystal": 1.5, "Iron": 2.5, "Gold": 3.5}},
                          "Oligoclase": {"Chance": 82000, "Multis": {"Rebirths": 50, "Iron": 3, "Gold": 3, "Quartz": 2, "Metal": 1.2}},
       },
      "Oceanic Geode": {"Coral": {"Chance": 3, "Multis": {"Stone": 4, "Gold": 2, "Quartz": 1.15}},
                         "Shardrite": {"Chance": 5, "Multis": {"Crystal": 4, "Gold": 2.1, "Quartz": 1.3, "Metal": 1.15}},
                         "Serpentine": {"Chance": 6, "Multis": {"Jade": 1.3, "Metal": 1.2}},
                         "Tsavorite": {"Chance": 14, "Multis": {"Rebirths": 1.25, "Stone": 1.25, "White Gems": 1.25, "Crystal": 1.25, "Iron": 1.25, "Gold": 1.25, "Jade": 1.25}},
                         "Tangeite": {"Chance": 100, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 15, "Metal": 1.8}},
                         "Labradorite": {"Chance": 32000, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Metal": 2.5, "Press": 1.1}},
                         "Tetrahedrite": {"Chance": 125000, "Multis": {"Rebirths": 50, "Stone": 3, "Metal": 3, "Press": 3}},
       },
      "Dream Geode": {"Dreamstone": {"Chance": 2, "Multis": {"Cash": 30, "Stone": 12, "Gold": 5, "Metal": 1.6}},
                       "Rhodium": {"Chance": 4, "Multis": {"Stone": 12, "White Gems": 7, "Quartz": 2, "Jade": 1.5, "Metal": 2}},
                       "Paragonite": {"Chance": 6, "Multis": {"Obsidian": 1.3}},
                       "Lautite": {"Chance": 50, "Multis": {"Gold": 2, "Jade": 2, "Press": 1.05}},
                       "Tungsten": {"Chance": 400, "Multis": {"Quartz": 3, "Metal": 2.5}},
                       "Iranite": {"Chance": 50000, "Multis": {"Quartz": 2, "Jade": 2, "Obsidian": 2, "Press": 1.25}},
                       "Grandidierite": {"Chance": 452000, "Multis": {"Ruby": 1.1, "Emerald": 1.1, "Sapphire": 1.1, "Gems": 1.25, "Mint": 1.5, "Metal": 3.25, "Press": 1.4}},
                       "Qernz": {"Chance": 3500000, "Multis": {"Cash": 30, "Multiplier": 30, "Rebirths": 30, "Stone": 30, "White Gems": 30, "Crystal": 30, "Iron": 30, "Gold": 30, "Metal": 5, "Press": 3, "Microparticles": 2}},
      },
      "Star Geode": {"Benitoite": {"Chance": 3, "Multis": {"Jade": 1.5, "Obsidian": 1.4, "Ruby": 1.2, "Press": 1.3}},
                      "Plesside": {"Chance": 5, "Multis": {"Gold": 5, "Quartz": 5, "Jade": 2}},
                      "Zykaite": {"Chance": 8, "Multis": {"Cash": 76, "Multiplier": 76, "Rebirths": 76, "Gold": 3.2, "Jade": 1.4, "Metal": 3, "Press": 1.35}},
                      "Abelsonite": {"Chance": 25, "Multis": {"Ruby": 2, "Press": 1.6}},
                      "Devilline": {"Chance": 80, "Multis": {"Gold": 3, "Quartz": 3, "Jade": 3, "Emerald": 1.15, "Metal": 3.2}},
                      "Lazulite": {"Chance": 25000, "Multis": {"Iron": 4, "Gold": 4, "Quartz": 4, "Sapphire": 1.2, "Mint": 1.45, "Metal": 2, "Press": 1.5, "Microparticles": 1.1}},
                      "Pentagonite": {"Chance": 250000, "Multis": {"Obsidian": 2.5, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Press": 2, "Microparticles": 1.3}},
      },
      "Holographic Geode": {"Pigeonite": {"Chance": 2, "Multis": {"Obsidian": 2, "Emerald": 1.25, "Mint": 1.5, "Microparticles": 1.02}},
                             "Vanuralite": {"Chance": 3, "Multis": {"Jade": 2.5, "Obsidian": 1.3, "Ruby": 1.75, "Metal": 1.75, "Press": 1.63, "Microparticles": 1.05}},
                             "Xanthoconite": {"Chance": 6, "Multis": {"Ruby": 1.25, "Emerald": 1.25, "Sapphire": 1.25, "Microparticles": 1.1}},
                             "Uytenbogaardtite": {"Chance": 50, "Multis": {"Cash": 111, "Multiplier": 111, "Rebirths": 111, "Press": 3}},
                             "Taranakite": {"Chance": 62000, "Multis": {"Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 1.15}},
                             "Quetzalcoatlite": {"Chance": 300000, "Multis": {"Ruby": 1.7, "Emerald": 1.7, "Sapphire": 1.7, "Mint": 2.5, "Metal": 2.5, "Press": 2.5, "Microparticles": 2}},
                             "Playfairite": {"Chance": 800000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Gems": 2, "Metal": 2, "Press": 2, "Microparticles": 2, "Star": 2}},
                             "Hologram": {"Chance": 12500000, "Multis": {"Diamond": 3, "Starlight": 5, "Ion": 2, "Metal": 1.5, "Press": 1.5, "Microparticles": 1.5, "Star": 1.5, "Robot": 1.5, "Prototype": 2}},
      },
      "Vector Geode": {"X": {"Chance": 1.84, "Multis": {"Cash": 3.3, "Stone": 3.3, "Iron": 3.3, "Jade": 3.3, "Emerald": 3.3}},
                        "Y": {"Chance": 2.22, "Multis": {"Multiplier": 3.3, "White Gems": 3.3, "Gold": 3.3, "Obsidian": 3.3, "Sapphire": 3.3}},
                        "Z": {"Chance": 7777, "Multis": {"Rebirths": 3.3, "Crystal": 3.3, "Quartz": 3.3, "Ruby": 3.3, "Diamond": 3.3, "Press": 3.3}},
                        "Vectorlord": {"Chance": 1750000, "Multis": {"Cash": 1.75, "Multiplier": 1.75, "Rebirths": 1.75, "Stone": 1.75, "White Gems": 1.75, "Crystal": 1.75, "Iron": 1.75, "Gold": 1.75, "Quartz": 1.75, "Jade": 1.75, "Obsidian": 1.75, "Ruby": 1.75, "Emerald": 1.75, "Sapphire": 1.75, "Diamond": 1.75, "Starlight": 1.75, "Metal": 1.75, "Press": 1.75, "Microparticles": 1.75, "Star": 1.75}},
      },
      "Insurgence Geode": {"Unholy Copper": {"Chance": 3.33, "Multis": {"Iron": 4, "Obsidian": 5, "Microparticles": 1.7}},
                            "Wrath Amethyst": {"Chance": 4, "Multis": {"Obsidian": 2.7, "Ruby": 2.7, "Sapphire": 2.7, "Press": 3.5}},
                            "Dark Gold": {"Chance": 5, "Multis": {"Obsidian": 3, "Diamond": 2, "Microparticles": 1.4, "Star": 1.1}},
                            "Tempered Quartz": {"Chance": 6, "Multis": {"Quartz": 7, "Obsidian": 4, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Press": 4.5, "Microparticles": 1.35}},
                            "Volcanic Molybdenum": {"Chance": 20, "Multis": {"Jade": 150, "Mint": 3, "Star": 1.25}},
                            "Deadly Obsidian": {"Chance": 200, "Multis": {"Obsidian": 25, "Metal": 3.5}},
                            "Doomdilite": {"Chance": 18000, "Multis": {"Ruby": 5, "Emerald": 5, "Sapphire": 5, "Diamond": 2.5, "Robot": 1.2}},
                            "Rave Ectoplasm": {"Chance": 50500, "Multis": {"Obsidian": 10, "Sapphire": 4, "Ion": 1.2, "Microparticles": 1.55}},
                            "Cloom": {"Chance": 100000, "Multis": {"Iron": 1.5, "Gold": 1.5, "Quartz": 1.5, "Jade": 1.5, "Obsidian": 1.5, "Ruby": 1.5, "Emerald": 1.5, "Sapphire": 1.5, "Diamond": 1.5, "Starlight": 1.5, "Ion": 1.5, "Metal": 1.5, "Press": 1.5, "Microparticles": 1.5}},
                            "Pentagram": {"Chance": 2500000, "Multis": {"Obsidian": 5, "Ruby": 5, "Emerald": 5, "Sapphire": 5, "Diamond": 5, "Starlight": 5, "Star": 2.5}},
                            "Nevercyan": {"Chance": 8000000, "Multis": {"Crystal": 7, "Quartz": 7, "Sapphire": 7, "Diamond": 7, "Uranium": 2, "Bismuth": 2, "Boracite": 1.5, "Mint": 5, "Robot": 2}},
                            "Core of Insurgence": {"Chance": 12000000, "Multis": {"Obsidian": 200, "Ion": 70, "Uranium": 20, "Bismuth": 3, "Orpiment": 1.5, "Metal": 4, "Press": 4, "Microparticles": 4, "Star": 4, "Robot": 4, "Prototype": 3}},
      },
      "Nostalgic Geode": {"Starfury": {"Chance": 3, "Multis": {"Star": 2}},
                           "Golden Glory": {"Chance": 5.55, "Multis": {"Gold": 78, "Ruby": 3, "Emerald": 3, "Press": 1.5}},
                           "Skylest": {"Chance": 6.25, "Multis": {"Sapphire": 3, "Diamond": 3, "Microparticles": 2}},
                           "Golest": {"Chance": 7.14, "Multis": {"Gold": 3, "Starlight": 3, "Microparticles": 3}},
                           "Prismo": {"Chance": 8.33, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2}},
                           "Aragon": {"Chance": 10, "Multis": {"Jade": 4, "Emerald": 4, "Mint": 4, "Metal": 4, "Press": 4}},
                           "Ephos": {"Chance": 12.5, "Multis": {"Gold": 4, "Obsidian": 4, "Ruby": 4, "Microparticles": 3.2}},
                           "Illudic": {"Chance": 16.67, "Multis": {"Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Mint": 3, "Metal": 3, "Press": 3, "Microparticles": 2.4}},
                           "Magmit": {"Chance": 25, "Multis": {"Ruby": 30, "Press": 5}},
                           "Phelix": {"Chance": 50, "Multis": {"Ion": 8, "Microparticles": 3.5}},
                           "Sepron": {"Chance": 200, "Multis": {"Jade": 5, "Emerald": 5, "Uranium": 5, "Metal": 5}},
                           "Ancar": {"Chance": 15000, "Multis": {"Sapphire": 3, "Diamond": 3, "Ion": 4, "Star": 3, "Robot": 2, "Prototype": 1.5}},
                           "Taryl": {"Chance": 27000, "Multis": {"Sapphire": 0.5, "Diamond": 100, "Microparticles": 2, "Star": 1.5}},
                           "Goldermine": {"Chance": 50000, "Multis": {"Gold": Mantissa(1,303), "Ruby": 10, "Emerald": 10, "Sapphire": 10, "Gems": 1.7, "Mint": 7, "Star": 3}},
                           "Prismarine": {"Chance": 75000, "Multis": {"Boracite": 3, "Mint": 9, "Metal": 5, "Press": 5}},
                           "Intergalaxias": {"Chance": 166667, "Multis": {"Emerald": 30, "Diamond": 10, "Starlight": 10, "Ion": 5, "Microparticles": 4, "Star": 4}},
                           "Eruptis": {"Chance": 181818, "Multis": {"Obsidian": 1e100, "Ruby": 8.5, "Orpiment": 1.1, "Robot": 3, "Prototype": 2}},
                           "Dime": {"Chance": 200000, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 3, "Starlight": 3, "Ion": 3, "Uranium": 3, "Bismuth": 3, "Boracite": 3}},
                           "Calamity": {"Chance": 500000, "Multis": {"Ruby": 15, "Diamond": 7, "Ion": 5, "Bismuth": 3, "Metal": 7, "Robot": 4, "Prototype": 2.5}},
                           "Elysium": {"Chance": 600000, "Multis": {"Quartz": 9696969696, "Sapphire": 96, "Boracite": 5, "Nissonite": 4, "Gems": 2.5, "Mint": 5, "Star": 5, "Robot": 4, "Prototype": 3}},
                           "Equinox": {"Chance": 750000, "Multis": {"White Gems": 7, "Iron": 7, "Quartz": 7, "Obsidian": 7, "Ruby": 7, "Emerald": 7, "Sapphire": 7, "Ion": 7, "Metal": 4.5, "Robot": 4.5}},
                           "Oculous": {"Chance": 875000, "Multis": {"Boracite": 2, "Prototype": 10}},
                           "Catalyst": {"Chance": 1500000, "Multis": {"Starlight": 8, "Ion": 8, "Uranium": 8, "Orpiment": 2, "Metal": 8, "Press": 8, "Microparticles": 8, "Robot": 5}},
                           "Loyalty": {"Chance": 3000000, "Multis": {"Orpiment": 4, "Robot": 6}},
                           "Omni": {"Chance": 5000000, "Multis": {"Emerald": 9, "Bismuth": 9, "Boracite": 9, "Nissonite": 9, "Orpiment": 3, "Metal": 9, "Prototype": 9}},
                           "Excalibur": {"Chance": 7000000, "Multis": {"Obsidian": 100, "Ruby": 25, "Diamond": 8, "Ion": 12, "Metal": 7, "Microparticles": 7}},
                           "Volùspa": {"Chance": 15000000, "Multis": {"Uranium": 6, "Bismuth": 5, "Boracite": 4, "Nissonite": 3, "Metal": 3, "Press": 3, "Microparticles": 3, "Star": 3, "Robot": 3}},
                           "Dynamo": {"Chance": 25000000, "Multis": {"Crystal": 15, "Gold": 15, "Jade": 15, "Ruby": 15, "Emerald": 15, "Sapphire": 15, "Starlight": 15, "Metal": 15}},
                           "Genesis": {"Chance": 25000000, "Multis": {"Obsidian": 15, "Emerald": 15, "Diamond": 15, "Ion": 15, "Bismuth": 15, "Press": 15}},
                           "Solomnium": {"Chance": 50000000, "Multis": {"Volt": 2, "Prototype": 3}},
                           "Immortality": {"Chance": 75000000, "Multis": {"Emerald": 50, "Ion": 12, "Bismuth": 12, "Orpiment": 3, "Metal": 12, "Robot": 7}},
                           "Temperùs": {"Chance": 150000000, "Multis": {"Crystal": 25, "Iron": 25, "Quartz": 25, "Jade": 25, "Sapphire": 25, "Diamond": 25, "Boracite": 25, "Nissonite": 25, "Aquamarine": 100, "Lollipop": 5, "Star": 15}},
                           "Relictic Loyalty": {"Chance": 300000000, "Multis": {"Emerald": 100000, "Starlight": 100000, "Nissonite": 100000, "Orpiment": 5, "Tetra": 1.5, "Volt": 1e15, "Aquamarine": 1e8, "Lollipop": 50, "C0RR8PT10N": 3, "Metal": 17, "Press": 9, "Microparticles": 8, "Star": 7}},
                           "Relictic Volùspa": {"Chance": 1500000000, "Multis": {"Cash": 100, "Multiplier": 100, "Rebirths": 100, "Stone": 100, "Crystal": 100, "Quartz": 100, "Emerald": 100, "Uranium": 100, "Orpiment": 10, "Tetra": 4, "Volt": 1e50, "Aquamarine": 1e25, "Lollipop": 1000, "C0RR8PT10N": 25, "Star": 9, "Robot": 10, "Prototype": 12}},
                           "Lifender": {"Chance": 5000000000, "Multis": {"Rebirths": 1e12, "Stone": 1e12, "Iron": 1e12, "Gold": 1e12, "Quartz": 1e12, "Diamond": 1e12, "Starlight": 1e12, "Ion": 1e12, "Uranium": 1e12, "Bismuth": 1e12, "Boracite": 1e12, "Nissonite": 1e12, "Orpiment": 1e222, "Tetra": 1e100, "Volt": 1e50, "Aquamarine": 1e30, "Lollipop": 1e15, "C0RR8PT10N": 1e6, "Mint": 50, "Metal": 1e12, "Stargazed Metal": 1e6, "Gyge": 5, "Auly Plate": 82, "Shel Piece": 9.08}},
      },
      "Cosmic Geode": {"Ascended Crystal": {"Chance": 2, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50}},
                        "Bright Quartz": {"Chance": 8, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50}},
                        "Glowing Jade": {"Chance": 23, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50}},
                        "Vivid Ruby": {"Chance": 100, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50, "Obsidian": 1e50, "Ruby": 1e50}},
                        "Glossy Diamond": {"Chance": 470, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50, "Obsidian": 1e50, "Ruby": 1e50, "Emerald": 1e50, "Sapphire": 1e50, "Diamond": 1e50}},
                        "Polarized Ion": {"Chance": 2100, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50, "Obsidian": 1e50, "Ruby": 1e50, "Emerald": 1e50, "Sapphire": 1e50, "Diamond": 1e50, "Starlight": 1e50, "Ion": 1e50}},
                        "Illuminated Bismuth": {"Chance": 8600, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50, "Obsidian": 1e50, "Ruby": 1e50, "Emerald": 1e50, "Sapphire": 1e50, "Diamond": 1e50, "Starlight": 1e50, "Ion": 1e50, "Uranium": 1e50, "Bismuth": 1e50}},
                        "Gleaming Nissonite": {"Chance": 15600, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50, "Obsidian": 1e50, "Ruby": 1e50, "Emerald": 1e50, "Sapphire": 1e50, "Diamond": 1e50, "Starlight": 1e50, "Ion": 1e50, "Uranium": 1e50, "Bismuth": 1e50, "Boracite": 1e50, "Nissonite": 1e50}},
                        "Glaring Tetra": {"Chance": 75000, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50, "Obsidian": 1e50, "Ruby": 1e50, "Emerald": 1e50, "Sapphire": 1e50, "Diamond": 1e50, "Starlight": 1e50, "Ion": 1e50, "Uranium": 1e50, "Bismuth": 1e50, "Boracite": 1e50, "Nissonite": 1e50, "Orpiment": 1e50, "Tetra": 1e50}},
                        "Shining Lollipop": {"Chance": 210000, "Multis": {"Cash": 1e50, "Multiplier": 1e50, "Rebirths": 1e50, "Stone": 1e50, "White Gems": 1e50, "Crystal": 1e50, "Iron": 1e50, "Gold": 1e50, "Quartz": 1e50, "Jade": 1e50, "Obsidian": 1e50, "Ruby": 1e50, "Emerald": 1e50, "Sapphire": 1e50, "Diamond": 1e50, "Starlight": 1e50, "Ion": 1e50, "Uranium": 1e50, "Bismuth": 1e50, "Boracite": 1e50, "Nissonite": 1e50, "Orpiment": 1e50, "Tetra": 1e50, "Volt": 1e50, "Aquamarine": 1e11, "Lollipop": 100}},
                        "Glistening Gyge": {"Chance": 613435, "Multis": {"Aquamarine": 1e8, "Lollipop": 300, "C0RR8PT10N": 2}},
                        "Scapolite": {"Chance": 1630500, "Multis": {"Volt": 1e10, "Aquamarine": 100000, "Lollipop": 5000, "C0RR8PT10N": 5}},
                        "Phenakite": {"Chance": 4230540, "Multis": {"Aquamarine": 1e20, "Lollipop": 1e6, "C0RR8PT10N": 25, "Stargazed Metal": 5}},
                        "Unarovite": {"Chance": 11230900, "Multis": {"Volt": 1e50, "Aquamarine": 1e50, "Lollipop": 1e10, "C0RR8PT10N": 150, "Stargazed Metal": 15}},
                        "Sphalerite": {"Chance": 27920300, "Multis": {"Lollipop": 1e20, "C0RR8PT10N": 1000, "Stargazed Metal": 50}},
                        "Rhodochrosite": {"Chance": 92000000, "Multis": {"Volt": 1e50, "Aquamarine": 1e50, "Lollipop": 1e50, "C0RR8PT10N": 100000, "Stargazed Metal": 150, "Gyge": 5}},
                        "Tourmaline": {"Chance": 231039274, "Multis": {"Tetra": 1e50, "Volt": 1e50, "Aquamarine": 1e50, "Lollipop": 1e50, "C0RR8PT10N": 1e8, "Stargazed Metal": 900, "Gyge": 30, "Auly Plate": 12, "Shell Piece": 2.43}},
                        "Cosmillite": {"Chance": 1000000000, "Multis": {"Boracite": 1e100, "Nissonite": 1e100, "Orpiment": 1e100, "Tetra": 1e100, "Volt": 1e100, "Aquamarine": 1e100, "Lollipop": 1e100, "C0RR8PT10N": 1e12, "Stargazed Metal": 5000, "Gyge": 132, "Auly Plate": 28, "Shell Piece": 5.42}},
      },
      "Hearted Geode": {
          "Sweet": {"Chance": 2, "Multis": {"Cash": 3, "Multiplier": 2, "Flower": 2.5, "Love": 1.5}},
          "Ichor Flower": {"Chance": 8, "Multis": {"Cash": 5, "Rebirths": 3, "Stone": 1.5, "Heart": 2}},
          "Halved Heart": {"Chance": 20, "Multis": {"White Gems": 2, "Love": 5, "Heart": 3}},
          "Rainbow": {"Chance": 100, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Crystal": 3, "Flower": 7, "Heart": 4}},
          "Unicorn": {"Chance": 333, "Multis": {"Cash": 7, "Multiplier": 7, "Rebirths": 7, "Stone": 7, "White Gems": 7, "Crystal": 7, "Flower": 7, "Heart": 7}},
          "Rose": {"Chance": 4000, "Multis": {"Gold": 5, "Quartz": 3, "Flower": 50, "Love": 20, "Heart": 10}},
          "Wickedite": {"Chance": 17500, "Multis": {"Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 10, "Heart": 1/1.4}},
          "Heartium": {"Chance": 280000, "Multis": {"Multiplier": 100, "Stone": 100, "Crystal": 100, "Jade": 10, "Ruby": 5, "Sapphire": 3, "Flower": 50, "Love": 50, "Heart": 50}},
          "Eternal Rose": {"Chance": 1250000, "Multis": {"Cash": 1000, "Multiplier": 1000, "Stone": 1000, "White Gems": 1000, "Crystal": 1000, "Iron": 1000, "Gold": 1000, "Quartz": 1000, "Jade": 1000, "Obsidian": 1000, "Ruby": 100, "Emerald": 100, "Sapphire": 100, "Nissonite": 4, "Flower": 1000, "Love": 1000, "Heart": 1000}}
      },
      "Luck Geode": {
          "Lucky Clover": {"Chance": 4, "Multis": {"Cash": 2, "Clover": 1.05}},
          "Golden Clover": {"Chance": 20, "Multis": {"Cash": 1.8, "Multiplier": 1.75, "Clover": 1.15}},
          "Diamond Clover": {"Chance": 100, "Multis": {"Multiplier": 2, "Rebirths": 3.5, "Clover": 1.25}},
          "Leprechaun's Hat": {"Chance": 200, "Multis": {"Rebirths": 3, "Stone": 1.8, "Clover": 1.32}},
          "Supreme Clover": {"Chance": 12000, "Multis": {"Crystal": 3, "Quartz": 4.5, "Clover": 1.75}},
          "Cloverite": {"Chance": 35000, "Multis": {"Stone": 10, "Gold": 5, "Jade": 3, "Emerald": 1.25, "Clover": 2.5}},
          "Ace": {"Chance": 1600000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "Crystal": 6, "Quartz": 6, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 6, "Clover": 12.5}},
          "777": {"Chance": 7777777, "Multis": {"Cash": 777, "Multiplier": 777, "Rebirths": 777, "Stone": 77, "White Gems": 77, "Crystal": 77, "Iron": 77, "Gold": 77, "Quartz": 77, "Jade": 77, "Obsidian": 77, "Ruby": 77, "Emerald": 77, "Sapphire": 77, "Clover": 77.7}}
      },
      "Clover Geode": {
          "Holy Clover": {"Chance": 3, "Multis": {"Quartz": 2, "Ruby": 1.5, "Clover": 1.45}},
          "Red Clover": {"Chance": 6, "Multis": {"Multiplier": 3, "White Gems": 1.15, "Obsidian": 3, "Ruby": 3, "Clover": 1.55}},
          "Death Clover": {"Chance": 20, "Multis": {"Stone": 5, "White Gems": 5, "Iron": 5, "Obsidian": 5, "Clover": 1.65}},
          "Oblivion Clover": {"Chance": 40, "Multis": {"Obsidian": 6, "Sapphire": 6, "Clover": 1.8}},
          "Giant Clover": {"Chance": 285, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 15, "Stone": 15, "Crystal": 15, "Clover": 2}},
          "Albino Clover": {"Chance": 1000, "Multis": {"Stone": 8, "White Gems": 8, "Iron": 8, "Ruby": 8, "Clover": 2.5}},
          "Tripetaled": {"Chance": 15000, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 3, "Clover": 3}},
          "Oddium": {"Chance": 55000, "Multis": {"Stone": 30, "Iron": 30, "Obsidian": 30, "Ruby": 30, "Emerald": 30, "Clover": 5}},
          "Dualpetaled": {"Chance": 120000, "Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Clover": 10}},
          "Core Clover": {"Chance": 1000001, "Multis": {"Cash": 100, "Rebirths": 100, "White Gems": 100, "Gold": 100, "Jade": 100, "Ruby": 100, "Mint": 10, "Clover": 25}},
          "Luckant": {"Chance": 4500000, "Multis": {"Cash": 666, "Multiplier": 666, "Rebirths": 666, "Stone": 666, "White Gems": 66, "Iron": 666, "Gold": 66, "Quartz": 66, "Jade": 66, "Obsidian": 66, "Ruby": 66, "Emerald": 66, "Sapphire": 66, "Starlight": 6, "Ion": 6, "Uranium": 6, "Bismuth": 1.6}},
          "Jackpotium": {"Chance": 8000000, "Multis": {"Cash": 1e5, "Multiplier": 1e5, "Rebirths": 1e5, "Stone": 1e5, "White Gems": 1e5, "Crystal": 1e5, "Nissonite": 1000, "Orpiment": 8, "Clover": 1000}},
          "Reality": {"Chance": 50000000, "Multis": {"Cash": 1e9, "Multiplier": 1e9, "Rebirths": 1e9, "Stone": 1e9, "White Gems": 1e9, "Crystal": 1e9, "Iron": 1e9, "Gold": 1e9, "Quartz": 1e9, "Jade": 1e9, "Obsidian": 1e9, "Ruby": 1e9, "Emerald": 1e9, "Sapphire": 1e9, "Diamond": 1e9, "Starlight": 1e9, "Ion": 1e9, "Uranium": 1e5, "Bismuth": 1e5, "Boracite": 1e5, "Nissonite": 1e5, "Orpiment": 10, "Mint": 1e9, "Clover": 1e9}}
      },
      "Celebrative Geode": {
          "Goldenium": {"Chance": 2, "Multis": {"Cash": 1.5, "Multiplier": 1.2}},
          "Lightroom": {"Chance": 5, "Multis": {"Obsidian": 1.75}},
          "Dazzlium": {"Chance": 11, "Multis": {"Cash": 2, "Multiplier": 1.7, "Rebirths": 1.7}},
          "Juled": {"Chance": 50, "Multis": {"Rebirths": 2, "Stone": 1.8}},
          "Tempested": {"Chance": 400, "Multis": {"Rebirths": 3, "Crystal": 1.5}},
          "Cyclone": {"Chance": 13000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2}},
          "Koanite": {"Chance": 21000, "Multis": {"Crystal": 5, "Quartz": 3}},
          "Torbdenum": {"Chance": 45000, "Multis": {"Gold": 12, "Jade": 10, "Obsidian": 5}},
          "Darnite": {"Chance": 100000, "Multis": {"Cash": 1000, "Ruby": 2, "Emerald": 2, "Sapphire": 2}},
          "Wubium": {"Chance": 500000, "Multis": {"Rebirths": 653, "Crystal": 25, "Obsidian": 8, "Diamond": 3}},
          "Woofern": {"Chance": 1150000, "Multis": {"Cash": 27, "Multiplier": 27, "Rebirths": 27, "Stone": 27, "White Gems": 27, "Crystal": 27, "Iron": 27, "Gold": 27, "Quartz": 27, "Jade": 27, "Obsidian": 27, "Ion": 10, "Bismuth": 2}},
          "Acastar": {"Chance": 4750000, "Multis": {"Rebirths": 100, "Quartz": 100, "Sapphire": 100, "Diamond": 100, "Starlight": 100, "Ion": 100}},
          "Zinction": {"Chance": 9000000, "Multis": {"Cash": 5, "Multiplier": 5, "Rebirths": 5, "Stone": 5, "White Gems": 5, "Crystal": 5, "Iron": 5, "Gold": 5, "Quartz": 5, "Jade": 5, "Orpiment": 3.5}},
          "Prismatum": {"Chance": 17500000, "Multis": {"Iron": 20, "Gold": 20, "Quartz": 20, "Jade": 20, "Obsidian": 20, "Ruby": 20, "Emerald": 20, "Sapphire": 20, "Diamond": 20, "Starlight": 20, "Ion": 20, "Uranium": 20, "Bismuth": 20, "Boracite": 20, "Nissonite": 20, "Orpiment": 8.5}}
    },
      "Spring Geode": {"Vine": {"Chance": 4, "Multis": {"Cash": 10, "Rebirths": 5}},
          "Dew": {"Chance": 6, "Multis": {"Cash": 25, "Multiplier": 30, "Stone": 20}},
          "Daisy": {"Chance": 12, "Multis": {"Cash": 100, "Stone": 25, "White Gems": 10}},
          "Tulip": {"Chance": 33, "Multis": {"Multiplier": 20, "Crystal": 10}},
          "Aster": {"Chance": 10000, "Multis": {"Stone": 1000, "Gold": 250, "Quartz": 100}},
          "Honeysuckle": {"Chance": 27500, "Multis": {"Rebirths": 2500, "Iron": 50, "Jade": 25}},
          "Trollius": {"Chance": 75000, "Multis": {"Stone": 1000, "Crystal": 250, "Gold": 200, "Jade": 100}},
          "Nymphea": {"Chance": 255000, "Multis": {"White Gems": 2500, "Quartz": 150, "Obsidian": 5}},
          "Sunflower": {"Chance": 800000, "Multis": {"Stone": 200, "Gold": 1000, "Ruby": 5}},
          "Yarrow": {"Chance": 3000000, "Multis": {"Cash": 1e6, "Ruby": 200, "Emerald": 200, "Sapphire": 200}},
          "Windflower": {"Chance": 5000000, "Multis": {"Multiplier": 10000, "Iron": 250, "Obsidian": 50, "Diamond": 15}},
          "Bachelor's Button": {"Chance": 12500000, "Multis": {"Rebirths": 1e5, "Gold": 500, "Emerald": 35, "Starlight": 5}}
     },
      "Easter Geode": {"Egg": {"Chance": 4, "Multis": {"Cash": 2}},
           "Tainted Egg": {"Chance": 5, "Multis": {"Cash": 10, "Multiplier": 10}},
           "Spotted Egg": {"Chance": 8, "Multis": {"Rebirths": 10}},
           "Equinox Egg": {"Chance": 20, "Multis": {"Stone": 10}},
           "Sugar Egg": {"Chance": 15000, "Multis": {"Multiplier": 100, "White Gems": 15, "Crystal": 10}},
           "Time Egg": {"Chance": 50500, "Multis": {"Quartz": 25, "Obsidian": 1.1}},
           "Malicious Egg": {"Chance": 125000, "Multis": {"Rebirths": 10000, "Iron": 1000, "Jade": 20}},
           "Stained Glass Egg": {"Chance": 6000000, "Multis": {"Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3}},
           "Space Egg": {"Chance": 6000000, "Multis": {"White Gems": 42, "Crystal": 42, "Obsidian": 10, "Ruby": 2}},
           "Gravitational Egg": {"Chance": 6000000, "Multis": {"Cash": 4, "Multiplier": 4, "Rebirths": 4, "Stone": 4, "White Gems": 4, "Crystal": 4, "Iron": 4, "Gold": 4, "Quartz": 4, "Jade": 4, "Obsidian": 4}},
           "EGG9000": {"Chance": 6000000, "Multis": {"Stone": 9000, "White Gems": 9000, "Crystal": 9000, "Iron": 9000, "Gold": 9000, "Quartz": 900, "Jade": 90, "Obsidian": 9}},
           "Dust Devil Egg": {"Chance": 6000000, "Multis": {"Multiplier": 3e6, "White Gems": 300, "Quartz": 35, "Obsidian": 3, "Ruby": 2.5}},
           "Black Iron Fabergé": {"Chance": 25000000, "Multis": {"Iron": 1e12, "Obsidian": 1e6, "Uranium": 1.25}},
           "Gilded Fabergé": {"Chance": 25000000, "Multis": {"Cash": 1e12, "Stone": 1000, "Crystal": 500, "Emerald": 100, "Sapphire": 5}},
           "Royal Fabergé": {"Chance": 25000000, "Multis": {"Cash": 1e9, "Gold": 1e6, "Diamond": 5, "Uranium": 1.5}},
           "Easter Basket": {"Chance": 100000000, "Multis": {"Cash": 100, "Multiplier": 100, "Rebirths": 100, "Stone": 100, "White Gems": 100, "Crystal": 100, "Iron": 100, "Gold": 100, "Quartz": 100, "Jade": 100, "Obsidian": 100, "Ruby": 100, "Emerald": 100, "Sapphire": 100, "Diamond": 100, "Starlight": 100, "Ion": 100, "Uranium": 100, "Bismuth": 100, "Boracite": 25, "Nissonite": 10, "Orpiment": 5, "Orpiment_2": 5, "Tetra": 10000, "Volt": 100, "Aquamarine": 15, "Lollipop": 5, "Stargazed Metal": 15, "Gyge": 5, "Auly Plate": 2}},
           "Egg of Destiny": {"Chance": 1000000000000, "Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Quartz": Mantissa(1,303), "Jade": Mantissa(1,303), "Obsidian": Mantissa(1,303), "Ruby": Mantissa(1,303), "Emerald": Mantissa(1,303), "Sapphire": Mantissa(1,303), "Diamond": Mantissa(1,303), "Starlight": Mantissa(1,303), "Ion": Mantissa(1,303), "Uranium": Mantissa(1,303), "Bismuth": Mantissa(1,303), "Boracite": Mantissa(1,303), "Nissonite": Mantissa(1,303), "Orpiment": Mantissa(1,303), "Tetra": Mantissa(1,303), "Volt": Mantissa(1,303), "Aquamarine": Mantissa(1,303), "Lollipop": Mantissa(1,303), "C0RR8PT10N": Mantissa(1,303), "Stargazed Metal": 1e100, "Gyge": 1e50, "Auly Plate": 1e25, "Shell Piece": 100000, "Prime Alpha Key": 1000}}
    },
      "Fabled Geode": {"Shinestone": {"Chance": 5, "Multis": {"Cash": 1e12, "Rebirths": 1e9}},
           "Yen": {"Chance": 5, "Multis": {"Cash": 2, "Multiplier": 2}},
           "Ascension": {"Chance": 5, "Multis": {"Rebirths": 800, "Stone": 400, "White Gems": 200, "Crystal": 100, "Iron": 50, "Gold": 25}},
           "Translucid Gem": {"Chance": 10, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2}},
           "Luminant Crystal": {"Chance": 10, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2}},
           "Exotic Metal": {"Chance": 20, "Multis": {"Cash": 2, 'Multiplier': 2, "Rebirths": 2, "Stone": 2, "Crystal": 2}},
           "Polyhedral Gold": {"Chance": 20, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2}},
           "Luxurious Quartz": {"Chance": 33, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2}},
           "Scarlet Jade": {"Chance": 33, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2}},
           "Reflected Obsidian": {"Chance": 100, "Multis": {"Cash": 2, "Multiplier": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2}},
           "Chromio": {"Chance": 100, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2}},
           "Clusterized Diamond": {"Chance": 200, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2}},
           "Cosmodryal": {"Chance": 200, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2}},
           "Augmented Ion": {"Chance": 1000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Starlight": 2}},
           "Symmetrite": {"Chance": 1000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2}},
           "Levigated Bismuth": {"Chance": 2000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2}},
           "Niflhemic Boracite": {"Chance": 4000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2}},
           "Encored Nissonite": {"Chance": 4000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2}},
           "Ethereal Orpiment": {"Chance": 12500, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2}},
           "Charged Tetra": {"Chance": 30000, "Multis": {"Cash": 1.5, "Multiplier": 1.5, "Rebirths": 1.5, "Stone": 1.5, "White Gems": 1.5, "Crystal": 1.5, "Iron": 1.5, "Gold": 1.5, "Quartz": 1.5, "Jade": 1.5, "Obsidian": 1.5, "Ruby": 1.5, "Emerald": 1.5, "Sapphire": 1.5, "Diamond": 1.5, "Ion": 1.5, "Uranium": 1.5, "Bismuth": 1.5, "Boracite": 1.5, "Nissonite": 1.5, "Orpiment": 1.5}},
           "Overclocked Volt": {"Chance": 75000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2, "Orpiment": 2}},
           "Agate": {"Chance": 125000, "Multis": {"Jade": 1e9, "Diamond": 1e9, "Ion": 1e5}},
           "Bustamite": {"Chance": 175000, "Multis": {"Iron": 1e9, "Sapphire": 1000, "Starlight": 20000}},
           "Polycrase": {"Chance": 262000, "Multis": {"Cash": 1e15, "Stone": 1e12, "Quartz": 1e9, "Ruby": 1e6}},
           "Stolzite": {"Chance": 363000, "Multis": {"Gold": 1e12, "Emerald": 1e9, "Uranium": 100}},
           "Zeunerite": {"Chance": 532000, "Multis": {"Jade": 1e12, "Emerald": 1e9, "Starlight": 1000, "Boracite": 100}},
           "Phosphophyllite": {"Chance": 750000, "Multis": {"Sapphire": 1e9, "Diamond": 2e6, "Ion": 1000, "Uranium": 400}},
           "Haxonite": {"Chance": 958000, "Multis": {"Ruby": 1e6, "Emerald": 1e15, "Starlight": 1e12, "Boracite": 600}},
           "Glaucodot": {"Chance": 987000, "Multis": {"Diamond": 1000, "Starlight": 1000, "Ion": 1000, "Uranium": 1000, "Bismuth": 1e6}},
           "Dyscrasite": {"Chance": 1525000, "Multis": {"Sapphire": 1e7, "Ion": 10000, "Boracite": 1000, "Nissonite": 10}},
           "Bazzite": {"Chance": 3321000, "Multis": {"Jade": 1e15, "Diamond": 1e9, "Bismuth": 100000, "Nissonite": 100}},
           "Cornubite": {"Chance": 5216000, "Multis": {"Emerald": 1e12, "Ion": 1e6, "Boracite": 100000, "Nissonite": 1000}},
           "Kostovite": {"Chance": 7521000, "Multis": {"Sapphire": 1e15, "Starlight": 1.9e10, "Nissonite": 10000, "Orpiment": 15}},
           "Minium": {"Chance": 10526000, "Multis": {"Diamond": 1e15, "Bismuth": 100000, "Orpiment": 100}},
           "Nyerereite": {"Chance": 22878000, "Multis": {"Ruby": 1e21, "Uranium": 1e12, "Orpiment": 650}},
           "Peridot": {"Chance": 60648000, "Multis": {"Obsidian": 1e99, "Starlight": 1e21, "Nissonite": 1e6, "Opriment": 5000}},
           "Realgar": {"Chance": 80632000, "Multis": {"Diamond": 1e22, "Ion": 1e12, "Opriment": 500, "Tetra": 1.25}},
           "Ereus": {"Chance": 100742000, "Multis": {"Cash": Mantissa(1,300), "Ruby": 1e33, "Bismuth": 1e15, "Nissonite": 1e9, "Tetra": 1e10, "Volt": 50000, "Aquamarine": 1000, "Lollipop": 25, "Stargazed Metal": 20, "Gyge": 5, "Auly Plate": 3, "Shell Piece": 1.1}},
           "Existence": {"Chance": 500000000, "Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": 1e273, "Gold": 1e243, "Quartz": 1e213, "Jade": 1e183, "Obsidian": 1e153, "Ruby": 1e123, "Emerald": 1e93, "Sapphire": 1e63, "Diamond": 1e45, "Starlight": 1e30, "Ion": 1e15, "Uranium": 1e12, "Bismuth": 1e9, "Boracite": 1e6, "Nissonite": 10000, "Orpiment": 100, "Tetra": 4, "Aquamarine": 1e9, "Lollipop": 150, "C0RR8PT10N": 5, "Gyge": 97.2, "Auly Plate": 10, "Shell Piece": 3}}
    },
      "Firey Duced Geode": {"Charcoal": {"Chance": 2, "Multis": {"White Gems": 4.5, "Obsidian": 2}},
                             "Flamecrystal": {"Chance": 4, "Multis": {"Ruby": 1.3}},
                             "Torbernite": {"Chance": 8, "Multis": {"Jade": 3, "Emerald": 1.1}},
                             "Manganite": {"Chance": 12, "Multis": {"Obsidian": 7.5}},
                             "Pyrrhoite": {"Chance": 40, "Multis": {"Ruby": 2, "Emerald": 1.2}},
                             "Norbergite": {"Chance": 100, "Multis": {"Quartz": 1.75, "Sapphire": 2.75}},
                             "Moolooite": {"Chance": 17500, "Multis": {"Ruby": 2.1, "Emerald": 2.1, "Sapphire": 2.1}},
                             "Lizardite": {"Chance": 47000, "Multis": {"Ruby": 5, "Sapphire": 2.8}},
                             "Kassite": {"Chance": 186000, "Multis": {"Ruby": 3.5, "Emerald": 2, "Sapphire": 1.7, "Diamond": 1.3}},
                             "Geocronite": {"Chance": 421000, "Multis": {"Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 2}},
                             "Dioptase": {"Chance": 757000, "Multis": {"Diamond": 2, "Starlight": 2, "Ion": 2}},
                             "Corkite": {"Chance": 2500000, "Multis": {"Ruby": 60, "Ion": 4, "Uranium": 2}},
                             "Thorium": {"Chance": 6275000, "Multis": {"Multiplier": 5, "Quartz": 5, "Obsidian": 5, "Ruby": 5, "Sapphire": 5, "Diamond": 5, "Bismuth": 5, "Boracite": 5}},
                             "Qusongite": {"Chance": 10000000, "Multis": {"Ruby": 11, "Emerald": 9, "Sapphire": 10, "Diamond": 6, "Starlight": 8, "Ion": 5, "Uranium": 7, "Bismuth": 4, "Boracite": 2, "Nissonite": 3.5}},
                             "Vulcanite": {"Chance": 22222222, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 3, "Starlight": 3, "Ion": 3, "Uranium": 3, "Bismuth": 3, "Boracite": 3, "Nissonite": 3, "Orpiment": 3, "Tetra": 3}},
                             "Carnelite": {"Chance": 66666666, "Multis": {"Sapphire": 2, "Diamond": 2, "Starlight": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2, "Orpiment": 2, "Tetra": 2, "Volt": 2}},
                             "Matter": {"Chance": 800800800, "Multis": {"Cash": 8e30, "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Quartz": Mantissa(1,300), "Jade": 1e288, "Obsidian": 1e280, "Ruby": 1e260, "Emerald": 1e260, "Sapphire": 1e260, "Diamond": 1e200, "Starlight": 1e190, "Ion": 1e150, "Uranium": 8.005e17, "Bismuth": 8.005e14, "Boracite": 8.005e11, "Nissonite": 800780, "Orpiment": 388, "Tetra": 8, "Volt": 6, "Aquamarine": 50000, "Lollipop": 200, "Lollipop_2": 1.5, "C0RR8PT10N": 10, "Stargazed Metal": 135, "Gyge": 45, "Auly Plate": 15, "Shell Piece": 5}},
     },
      "Symbiotic Geode": {"PROT5409-Irosfagum": {"Chance": 2, "Multis": {"Emerald": 54, "Starlight": 540, "Bismuth": 1.2, "Boracite": 1.14, "Nissonite": 1.1}},
                           "Radiobarite": {"Chance": 4, "Multis": {"Cash": 120120120, "Multiplier": 120120, "Rebirths": 120, "Uranium": 404, "Boracite": 1.2}},
                           "Uramarsite": {"Chance": 8, "Multis": {"Obsidian": 3, "Ruby": 15, "Emerald": 25, "Sapphire": 50, "Diamond": 100, "Ion": 555, "Uranium": 854, "Bismuth": 4, "Boracite": 3}},
                           "Uranopolycrase": {"Chance": 12, "Multis": {"Stone": 5000, "White Gems": 50000, "Crystal": 500000, "Iron": 5e6, "Gold": 5e7, "Ion": 155, "Bismuth": 1.8}},
                           "Yttrobetafite": {"Chance": 28, "Multis": {"Starlight": 68, "Ion": 34, "Uranium": 12, "Bismuth": 6, "Boracite": 3, "Nissonite": 1.5}},
                           "IMA2008-047": {"Chance": 100, "Multis": {"Uranium": 47, "Bismuth": 5, "Boracite": 3}},
                           "Ludlockite": {"Chance": 12000, "Multis": {"Sapphire": 1575, "Diamond": 157, "Starlight": 57, "Uranium": 20, "Boracite": 10, "Nissonite": 7}},
                           "Cattite": {"Chance": 80000, "Multis": {"Multiplier": 9, "Rebirths": 9, "Stone": 9, "White Gems": 9, "Crystal": 9, "Iron": 9, "Gold": 9, "Jade": 9, "Ruby": 9, "Emerald": 9, "Diamond": 9, "Starlight": 9, "Ion": 20, "Uranium": 9, "Uranium_2": 11, "Bismuth": 9, "Bismuth_2": 7, "Boracite": 9, "Boracite": 2, "Nissonite": 9, "Nissonite": 3.5, "Orpiment": 7, "Orpiment_2": 1.6}},
                           "Schorl": {"Chance": 300000, "Multis": {"Cash": 2.5e10, "Multiplier": 2.5e7, "Rebirths": 2.5e7, "Stone": 250000, "White Gems": 25000, "Crystal": 2500, "Uranium": 455, "Bismuth": 255, "Boracite": 15, "Nissonite": 10, "Orpiment": 8}},
                           "Mixite": {"Chance": 4500000, "Multis": {"Cash": 69, "Multiplier": 69, "Rebirths": 69, "Stone": 69, "White Gems": 69, "Crystal": 69, "Iron": 69, "Jade": 4.5e46, "Obsidian": 4.5e46, "Starlight": 4.5e6, "Ion": 450000, "Uranium": 45000, "Bismuth": 4500, "Boracite": 450, "Nissonite": 45, "Orpiment": 7, "Tetra": 3}},
                           "Tellurium": {"Chance": 47500000, "Multis": {"Stone": 9.4e9, "White Gems": 9e90, "Crystal": 9.4e7, "Gold": 940000, "Obsidian": 6e70, "Ruby": 24040, "Diamond": 80800, "Starlight": 8e6, "Ion": 24040, "Uranium": 1.02e7, "Bismuth": 14000, "Boracite": 4700, "Nissonite": 47.5, "Orpiment": 12, "Tetra": 3, "Volt": 2.3}},
                           "Eyselite": {"Chance": 650000000, "Multis": {"Cash": 6e70, "Multiplier": 6e70, "Rebirths": 6e70, "Stone": 6e70, "White Gems": 6e70, "Crystal": 6e70, "Iron": 6e70, "Gold": 6e70, "Quartz": 6e70, "Jade": 6e70, "Obsidian": 4e70, "Ruby": 6e70, "Emerald": 6e70, "Sapphire": 6e70, "Diamond": 6e70, "Starlight": 6e70, "Ion": 6e70, "Uranium": 6.7066e11, "Bismuth": 6.7066e8, "Boracite": 670670, "Nissonite": 670, "Orpiment": 67, "Tetra": 6, "Volt": 5, "Aquamarine": 1e17, "Lollipop": 700, "C0RR8PT10N": 7.5, "Stargazed Metal": 101.01, "Auly Plate": 25.321, "Shell Piece": 4.32}},
       },
      "Summer Geode": {"Water": {"Chance": 5, "Multis": {"Stone": 1.5, "Sand": 1.6}},
                        "Beach Ball": {"Chance": 7, "Multis": {"Stone": 2, "Sand": 1.75}},
                        "Ice Cream": {"Chance": 13, "Multis": {"White Gems": 1.4, "Sand": 2}},
                        "Umbrella": {"Chance": 1314, "Multis": {"Cash": 1.5, "Multiplier": 1.5, "Stone": 1.5, "White Gems": 1.5, "Sand": 1.5, "Ray": 1.5}},
                        "Salt": {"Chance": 5294, "Multis": {"Crystal": 1.6, "Sand": 3.5, "Ray": 2.2}},
                        "Rockbottom": {"Chance": 12379, "Multis": {"Obsidian": 2, "Patriotic Crystal": 1.25}},
                        "Fossil": {"Chance": 58617, "Multis": {"Stone": 50, "Iron": 10, "Jade": 3, "Sand": 3, "Ray": 3}},
                        "Bedrock": {"Chance": 532649, "Multis": {"Obsidian": 5, "Ruby": 3, "Sand": 5, "Patriotic Crystal": 1.7}},
                        "Tryglogem": {"Chance": 7880324, "Multis": {"Crystal": 63, "Quartz": 15, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 5, "Ion": 2, "Aureal Gem": 2}},
       },
      "Patriotic Geode": {"American Flag": {"Chance": 2, "Multis": {"White Gems": 1.5, "Ray": 1.5}},
                           "Fluorescent Iron": {"Chance": 6, "Multis": {"Iron": 2, "Gold": 1.5, "Sand": 2, "Ray": 1.8}},
                           "Fluorite": {"Chance": 8195, "Multis": {"Gold": 2, "Quartz": 2, "Sand": 2.6, "Patriotic Crystal": 1.5}},
                           "Patriotic Opal": {"Chance": 42807, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Sand": 2, "Ray": 2, "Patriotic Crystal": 2}},
                           "Silver of Justice": {"Chance": 181504, "Multis": {"Iron": 10, "Gold": 10, "Quartz": 3, "Obsidian": 4, "Ruby": 1.5, "Sand": 1.5, "Ray": 2, "Patriotic Crystal": 2.5}},
                           "Epidote of Liberty": {"Chance": 602968, "Multis": {"White Gems": 100, "Jade": 10, "Emerald": 4, "Sand": 5, "Ray": 5, "Patriotic Crystal": 3}},
                           "Fireworks": {"Chance": 3283269, "Multis": {"Stone": 5, "Iron": 5, "Quartz": 5, "Obsidian": 5, "Emerald": 5, "Diamond": 5, "Starlight": 5, "Sand": 15, "Ray": 10, "Patriotic Crystal": 5}},
                           "Firecracker": {"Chance": 24932184, "Multis": {"Ruby": 21, "Emerald": 21, "Sapphire": 21, "Diamond": 16, "Ion": 15, "Uranium": 2, "Boracite": 5, "Sand": 12, "Ray": 12, "Patriotic Crystal": 12}},
      },
      "Aureal Geode": {"Shinepowder": {"Chance": 3, "Multis": {"Cash": 1.5, "Multiplier": 1.5, "Rebirths": 1.5, "Stone": 1.5, "White Gems": 1.5, "Iron": 1.5, "Gold": 1.5, "Quartz": 1.5, "Jade": 1.5, "Ruby": 1.5, "Emerald": 1.5, "Sapphire": 1.5, "Patriotic Crystal": 1.5}},
                        "Lightray": {"Chance": 3, "Multis": {"Jade": 2, "Obsidian": 3, "Ruby": 2, "Ray": 2, "Patriotic Crystal": 1.5}},
                        "Chalice": {"Chance": 3, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Patriotic Crystal": 2}},
                        "Halo": {"Chance": 6, "Multis": {"Obsidian": 2.5, "Ruby": 2.5, "Emerald": 2.5, "Patriotic Crystal": 2.5}},
                        "Dimwidth Diamond": {"Chance": 12, "Multis": {"Aureal Gem": 2}},
                        "Eldritch Moonstone": {"Chance": 25, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 15, "Stone": 15, "White Gems": 15, "Crystal": 15, "Iron": 15, "Gold": 15, "Quartz": 15, "Jade": 15, "Star": 2, "Patriotic Crystal": 3}},
                        "Polarstone": {"Chance": 300, "Multis": {"Gems": 2, "Mint": 2, "Metal": 2, "Press": 2, "Microparticles": 2, "Star": 2, "Robot": 2, "Prototype": 2, "Sand": 2, "Ray": 2, "Patriotic Crystal": 2}},
                        "Ophanim": {"Chance": 5000, "Multis": {"Starlight": 2, "Aureal Gem": 2}},
                        "Sunstone": {"Chance": 25321, "Multis": {"Jade": 2.5, "Obsidian": 2.5, "Ruby": 2.5, "Emerald": 2.5, "Sapphire": 2.5, "Diamond": 2.5, "Starlight": 1.5, "Sand": 2.5, "Ray": 2.5, "Patriotic Crystal": 2.5, "Aureal Gem": 2.5}},
                        "Judgemental Jade": {"Chance": 72488, "Multis": {"Jade": 2.92993e43, "Aureal Gem": 5}},
                        "Glassomophore": {"Chance": 305154, "Multis": {"Obsidian": 3, "Ion": 3, "Uranium": 3, "Gems": 3, "Sand": 3.5, "Ray": 3.5, "Patriotic Crystal": 3.5, "Aureal Gem": 3.5}},
                        "Aurora Borealis": {"Chance": 2061827, "Multis": {"Emerald": 10, "Sapphire": 10, "Diamond": 10, "Starlight": 10, "Ion": 10, "Uranium": 10, "Aureal Gem": 10}},
                        "Archangel Meridianiite": {"Chance": 7623836, "Multis": {"Gold": 2, "Emerald": 2, "Nissonite": 2, "Sand": 48, "Ray": 24, "Patriotic Crystal": 12, "Aureal Gem": 6}},
                        "Overpurified Sculptanium": {"Chance": 48261628, "Multis": {"Nissonite": 10, "Gems": 10, "Mint": 10, "Metal": 10, "Press": 10, "Microparticles": 10, "Star": 10, "Robot": 10, "Prototype": 10, "Sand": 18, "Ray": 18, "Patriotic Crystal": 18, "Aureal Gem": 18}},
                        "Bloodstone": {"Chance": 202090891, "Multis": {"Ion": 160, "Uranium": 80, "Bismuth": 40, "Boracite": 20, "Nissonite": 10, "Orpiment": 5, "Volt": 1e8, "Aquamarine": 100000, "Lollipop": 50, "C0RR8PT10N": 2.5, "Stargazed Metal": 60.43, "Auly Plate": 10, "Shell Piece": 2, "Fragment": 2}},
      },
      "Eden Geode": {"Soul": {"Chance": 2, "Multis": {"Ion": 2, "Uranium": 3, "Patriotic Crystal": 2, "Aureal Gem": 3}},
                      "Menace": {"Chance": 3, "Multis": {"Orpiment": 2, "Sand": 3, "Ray": 3, "Patriotic Crystal": 3, "Aureal Gem": 5, "Fragment": 2.5}},
                      "Anger": {"Chance": 4, "Multis": {"Bismuth": 2, "Boracite": 4, "Nissonite": 2, "Press": 3, "Star": 3, "Sand": 3, "Ray": 3, "Patriotic Crystal": 10, "Aureal Gem": 3, "Fragment": 3}},
                      "Emptiness": {"Chance": 8, "Multis": {"Ion": 3.5, "Uranium": 3.5, "Bismuth": 3.5, "Boracite": 3.5, "Nissonite": 3.5, "Fragment": 4}},
                      "Vastness": {"Chance": 15, "Multis": {"Gems": 3, "Mint": 25, "Aureal Gem": 25}},
                      "Fracture": {"Chance": 50, "Multis": {"Multiplier": 2, "Stone": 2, "Crystal": 2, "Gold": 2, "Jade": 2, "Ruby": 2, "Sapphire": 2, "Starlight": 2, "Uranium": 2, "Boracite": 2, "Orpiment": 2, "Press": 2, "Star": 2, "Prototype": 2, "Sand": 2, "Patriotic Crystal": 2, "Fragment": 2}},
                      "Wickstone": {"Chance": 450, "Multis": {"Stone": 600, "Iron": 600, "Obsidian": 600, "Boracite": 5, "Gems": 6, "Mint": 14, "Sand": 4, "Ray": 4, "Patriotic Crystal": 4, "Aureal Gem": 4, "Fragment": 4}},
                      "Chromatory": {"Chance": 2700, "Multis": {"Orpiment": 3, "Aureal Gem": 2, "Fragment": 5}},
                      "Shatterment": {"Chance": 9400, "Multis": {"Boracite": 7, "Sand": 10, "Ray": 10, "Patriotic Crystal": 10, "Aureal Gem": 10, "Fragment": 3}},
                      "Deepenlor": {"Chance": 41825, "Multis": {"Fragment": 10}},
                      "Graphium": {"Chance": 105368, "Multis": {"Orpiment": 1.5, "Gems": 4, "Mint": 6, "Sand": 6, "Ray": 6, "Patriotic Crystal": 6, "Aureal Gem": 6, "Fragment": 6}},
                      "Vayonium": {"Chance": 341723, "Multis": {"Stone": 1e6, "White Gems": 1e6, "Crystal": 1e6, "Iron": 1e6, "Gold": 1e6, "Quartz": 1e6, "Jade": 1e6, "Obsidian": 1e6, "Ruby": 1e6, "Emerald": 1e6, "Sapphire": 1e6, "Diamond": 1e6, "Starlight": 1e6, "Ion": 1e6, "Uranium": 1e6, "Bismuth": 1e6}},
                      "Trimonia": {"Chance": 737319, "Multis": {"Ion": 96, "Uranium": 48, "Bismuth": 24, "Boracite": 12, "Nissonite": 6, "Orpiment": 3, "Metal": 5, "Sand": 15, "Ray": 12, "Patriotic Crystal": 9, "Aureal Gem": 699, "Fragment": 3}},
                      "Defragstone": {"Chance": 924361, "Multis": {"Orpiment": 4, "Tetra": 2, "Gems": 9, "Mint": 45, "Star": 30, "Robot": 15, "Prototype": 8, "Aureal Gem": 20, "Fragment": 12}},
                      "Monochromia": {"Chance": 1625526, "Multis": {"Emerald": 20, "Uranium": 20, "Boracite": 20, "Nissonite": 20, "Orpiment": 20, "Fragment": 20}},
                      "Antaloptide": {"Chance": 5261367, "Multis": {"Tetra": 5, "Mint": 60, "Prototype": 13, "Fragment": 26}},
                      "Astatine": {"Chance": 11362572, "Multis": {"Tetra": 8, "Volt": 3, "Sand": 35, "Ray": 35, "Patriotic Crystal": 35, "Aureal Gem": 35, "Fragment": 35}},
                      "Vantablack": {"Chance": 32516272, "Multis": {"Volt": 4, "Aureal Gem": 0.1, "Fragment": 1000}},
                      "Titanium": {"Chance": 75727188, "Multis": {"Cash": 75, "Multiplier": 75, "Rebirths": 75, "Stone": 75, "White Gems": 75, "Crystal": 75, "Iron": 75, "Gold": 75, "Quartz": 75, "Jade": 75, "Obsidian": 75, "Ruby": 75, "Emerald": 75, "Sapphire": 75, "Diamond": 75, "Starlight": 75, "Ion": 75, "Uranium": 75, "Bismuth": 75, "Boracite": 75, "Nissonite": 75, "Orpiment": 75, "Metal": 75, "Press": 75, "Microparticles": 75, "Star": 75, "Robot": 75, "Sand": 75, "Ray": 75, "Patriotic Crystal": 75, "Aureal Gem": 75, "Fragment": 75}},
                      "Actuality": {"Chance": 950216271, "Multis": {"Cash": 1e6, "Multiplier": 1e6, "Rebirths": 1e6, "Stone": 1e6, "White Gems": 1e6, "Crystal": 1e6, "Iron": 1e6, "Gold": 1e6, "Quartz": 1e6, "Jade": 1e6, "Obsidian": 1e6, "Ruby": 1e6, "Emerald": 1e6, "Sapphire": 1e6, "Diamond": 1e6, "Starlight": 1e6, "Ion": 1e6, "Uranium": 1e6, "Bismuth": 1e6, "Boracite": 1e6, "Nissonite": 1e6, "Orpiment": 1e6, "Tetra": 1e6, "Volt": 1e6, "Aquamarine": 1e8, "Lollipop": 700, "C0RR8PT10N": 15, "Stargazed Metal": 1000, "Gyge": 100, "Auly Plate": 15.5, "Shell Piece": 3.532, "Gems": 15, "Mint": 80, "Metal": 80, "Press": 80, "Microparticles": 80, "Star": 80, "Robot": 80, "Prototype": 80, "Sand": 1e6, "Ray": 1e6, "Patriotic Crystal": 1e6, "Aureal Gem": 1e6, "Fragment": 1e6}},
         },
      "Lost Geode": {"Mist": {"Chance": 2, "Multis": {"Multiplier": 4, "Crystal": 2}},
                      "Vision": {"Chance": 9, "Multis": {"Iron": 3}},
                      "Obscurity": {"Chance": 60, "Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Crystal": 6, "Quartz": 2}},
                      "The Mark": {"Chance": 275, "Multis": {"Cash": 8, "Multiplier": 8, "Rebirths": 8, "Stone": 8, "White Gems": 8, "Crystal": 8, "Iron": 8, "Gold": 8}},
                      "Forgotten": {"Chance": 1500, "Multis": {"Gold": 15, "Jade": 4}},
                      "Pestilence": {"Chance": 8000, "Multis": {"Jade": 15, "Obsidian": 2}},
                      "Forbidden": {"Chance": 50000, "Multis": {"Obsidian": 2.25, "Ruby": 1.25, "Emerald": 1.25, "Sapphire": 1.25}},
                      "GL1TCH": {"Chance": 300000, "Multis": {"Cash": 999, "Multiplier": 999, "Rebirths": 999, "Jade": 99, "Ruby": 2, "Sapphire": 3}},
                      "Oblivion": {"Chance": 2500000, "Multis": {"Gold": 7, "Quartz": 20, "Jade": 50, "Ruby": 77, "Diamond": 5, "Ion": 2.5}},
                      "Brimstone": {"Chance": 8000000, "Multis": {"Cash": 2400, "Multiplier": 2300, "Rebirths": 2200, "Stone": 2100, "White Gems": 200, "Crystal": 190, "Iron": 180, "Gold": 170, "Quartz": 160, "Jade": 150, "Obsidian": 140, "Ruby": 13, "Emerald": 12, "Sapphire": 11, "Diamond": 10, "Starlight": 9, "Ion": 8, "Uranium": 7, "Bismuth": 6, "Boracite": 5, "Nissonite": 4, "Orpiment": 3}},
                      "ù": {"Chance": 255255255, "Multis": {"Cash": 1.01, "Lollipop": 10, "C0RR8PT10N": 1.5, "Stargazed Metal": 50, "Auly Plate": 2, "Shell Piece": 1.1, "Gems": 50}},
       },
      "Sinister Geode": {"Perishstone": {"Chance": 2, "Multis": {"Stone": 3, "Crystal": 1.8}},
                          "Ghostly Gem": {"Chance": 7, "Multis": {"Cash": 12, "Stone": 4.75, "White Gems": 2.8, "Iron": 2.15}},
                          "Waxy Iron": {"Chance": 16, "Multis": {"White Gems": 1.95, "Iron": 3.1, "Gold": 1.72}},
                          "Moonlit Quartz": {"Chance": 76, "Multis": {"Cash": 5, "Multiplier": 5, "Rebirths": 5, "Stone": 5, "White Gems": 5, "Crystal": 5, "Iron": 5, "Gold": 5, "Quartz": 5}},
                          "Looming Crystal": {"Chance": 222, "Multis": {"Stone": 0.5, "Crystal": 1.5, "Iron": 1.5, "Gold": 2.5, "Quartz": 3, "Jade": 3.5}},
                          "Perilous Gold": {"Chance": 666, "Multis": {"Gold": 15, "Gems": 1.08}},
                          "Shadowy Jade": {"Chance": 2500, "Multis": {"Cash": 15, "Multiplier": 13, "Crystal": 5, "Iron": 5, "Jade": 7, "Mint": 3}},
                          "Warped Obsidian": {"Chance": 8000, "Multis": {"Multiplier": 6.54, "Rebirths": 6.54, "Stone": 6.54, "White Gems": 6.54, "Crystal": 6.54, "Iron": 6.54, "Gold": 6.54, "Quartz": 6.54, "Jade": 6.54, "Obsidian": 2}},
                          "Mischievous Agate": {"Chance": 15000, "Multis": {"Stone": 7, "White Gems": 10, "Crystal": 5, "Obsidian": 1.5, "Ruby": 2, "Emerald": 2, "Sapphire": 2}},
                          "Dastard Emerald": {"Chance": 69000, "Multis": {"Gold": 52, "Emerald": 7, "Gems": 1.15, "Metal": 2}},
                          "Rabid Diamond": {"Chance": 200000, "Multis": {"Multiplier": 70, "Rebirths": 70, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 10, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 5}},
                          "Preternatural Polybasite": {"Chance": 450000, "Multis": {"Cash": 300000, "Multiplier": 300000, "Rebirths": 300000, "Gold": 25, "Quartz": 30, "Jade": 80, "Starlight": 1.75, "Ion": 1.75}},
                          "Wretched Orpiment": {"Chance": 900000, "Multis": {"Rebirths": 5.87e9, "White Gems": 1e7, "Gold": 900, "Ruby": 32, "Emerald": 16, "Diamond": 7, "Starlight": 2, "Uranium": 1.3, "Bismuth": 1.25, "Gems": 1.72}},
                          "Cerussite": {"Chance": 1750000, "Multis": {"Rebirths": 6.66e8, "Iron": 500, "Gold": 500, "Ruby": 11, "Ion": 7, "Uranium": 2.5, "Boracite": 2}},
                          "Yunium": {"Chance": 4000000, "Multis": {"Cash": 1e15, "Stone": 1e9, "Crystal": 1e9, "Quartz": 1e9, "Ruby": 1000, "Emerald": 1000, "Sapphire": 1000, "Starlight": 100, "Ion": 30, "Uranium": 20, "Nissonite": 3, "Orpiment": 1.5, "Tetra": 2}},
                          "Cristobalite": {"Chance": 20000000, "Multis": {"Cash": 9.4e9, "Multiplier": 2.1345e8, "Rebirths": 6.5784e8, "Stone": 9.8765e8, "White Gems": 888888, "Crystal": 69, "Iron": 1333, "Gold": 666, "Quartz": 404, "Jade": 77, "Obsidian": 11, "Ruby": 22, "Emerald": 44, "Sapphire": 111, "Diamond": 777, "Starlight": 66, "Ion": 17, "Uranium": 4, "Bismuth": 88, "Boracite": 25, "Nissonite": 25, "Orpiment": 8, "Tetra": 3.75}},
        },
      "Aztec Geode": {"Grimmetal": {"Chance": 2, "Multis": {"Ruby": 2, "Emerald": 2, "Sapphire": 2}},
                       "Sestrum": {"Chance": 6, "Multis": {"Diamond": 2.5, "Starlight": 2.5}},
                       "Klovonium": {"Chance": 33, "Multis": {"Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Ion": 2, "Clover": 3}},
                       "Goose's Gold": {"Chance": 222, "Multis": {"Gold": 1.23e6, "Diamond": 3, "Starlight": 3, "Ion": 3, "Uranium": 3}},
                       "Concillite": {"Chance": 1666, "Multis": {"Obsidian": 5, "Ruby": 5, "Emerald": 5, "Sapphire": 5, "Diamond": 5, "Starlight": 5, "Ion": 5, "Uranium": 5, "Bismuth": 2}},
                       "Ztarrium": {"Chance": 33333, "Multis": {"Bismuth": 5, "Boracite": 2.5, "Nissonite": 2.5}},
                       "Jongium": {"Chance": 85000, "Multis": {"Boracite": 3, "Nissonite": 3, "Orpiment": 2}},
                       "Revoolut": {"Chance": 175000, "Multis": {"Bismuth": 8, "Boracite": 8, "Nissonite": 8, "Orpiment": 4, "Tetra": 2}},
                       "Halandrite": {"Chance": 380000, "Multis": {"Nissonite": 100, "Orpiment": 25, "Tetra": 5, "Volt": 2}},
                       "Zestrium": {"Chance": 710000, "Multis": {"Orpiment": 123.45, "Tetra": 12.33, "Volt": 5.55, "Aquamarine": 2}},
                       "Limitrite": {"Chance": 989989, "Multis": {"Orpiment": 500, "Tetra": 25, "Volt": 10, "Aquamarine": 4}},
                       "Aztekium": {"Chance": 3000000, "Multis": {"Volt": 25, "Aquamarine": 5, "Lollipop": 2, "Gems": 250, "Clover": 777}},
                       "Swordium": {"Chance": 10000000, "Multis": {"Ruby": 1e33, "Ion": 1e6, "Orpiment": 2000, "Volt": 75, "Lollipop": 5, "C0RR8PT10N": 2}},
                       "Shieldium": {"Chance": 10000000, "Multis": {"Sapphire": 1e33, "Boracite": 3000, "Nissonite": 3000, "Tetra": 800, "Aquamarine": 15, "Lollipop": 5, "C0RR8PT10N": 2}},
                       "Spanchium": {"Chance": 15000000, "Multis": {"Orpiment": 123456, "Tetra": 12345, "Volt": 1234, "C0RR8PT10N": 3}},
                       "Spearite": {"Chance": 25000000, "Multis": {"Tetra": 50000, "Volt": 3000, "Aquamarine": 250, "Lollipop": 15, "C0RR8PT10N": 5}},
                       "Vasolonio": {"Chance": 69666999, "Multis": {"Aquamarine": 1333, "Lollipop": 42.01, "C0RR8PT10N": 6.9, "Stargazed Metal": 2}},
                       "Megabursite": {"Chance": 277000000, "Multis": {"Tetra": 3.33e24, "Volt": 1.11e8, "Aquamarine": 65530, "Lollipop": 256, "C0RR8PT10N": 16, "Stargazed Metal": 4, "Gyge": 2}},
                       "Tematonium": {"Chance": 750000000, "Multis": {"Orpiment": Mantissa(1,303), "Tetra": 1e100, "Volt": 1e36, "Aquamarine": 1e6, "Lollipop": 2400, "C0RR8PT10N": 120, "Stargazed Metal": 120, "Gyge": 3, "Auly Plate": 11.2, "Shell Piece": 2.22}},
                       "Divinorum": {"Chance": 9000000000, "Multis": {"Cash": Mantissa(1,1e10), "Multiplier": Mantissa(3.33,3333), "Rebirths": Mantissa(3.33,3333), "Stone": Mantissa(3.33,3333), "White Gems": Mantissa(3.33,3333), "Crystal": Mantissa(3.33,3333), "Iron": Mantissa(3.33,3333), "Gold": Mantissa(3.33,3333), "Quartz": Mantissa(3.33,3333), "Jade": Mantissa(3.33,3333), "Obsidian": Mantissa(3.33,3333), "Ruby": Mantissa(3.33,3333), "Emerald": Mantissa(3.33,3333), "Sapphire": Mantissa(3.33,3333), "Diamond": Mantissa(3.33,3333), "Starlight": Mantissa(3.33,3333), "Ion": Mantissa(3.33,3333), "Uranium": Mantissa(3.33,3333), "Bismuth": Mantissa(3.33,3333), "Boracite": Mantissa(3.33,3333), "Nissonite": Mantissa(3.33,3333), "Orpiment": Mantissa(3.33,3333), "Tetra": Mantissa(3.33, 1000), "Volt": Mantissa(3.33, 333), "Aquamarine": 3.33e100, "Lollipop": 3.33e33, "C0RR8PT10N": 3.33e6, "Stargazed Metal": 3333, "Gyge": 333, "Auly Plate": 33, "Shell Piece": 3.3}},
       },
      "Revival Geode": {"Limestone": {"Chance": 3, "Multis": {"Cash": 100, "Rebirths": 50, "White Gems": 10}},
                         "Amber": {"Chance": 10, "Multis": {"Crystal": 35, "Iron": 20, "Gold": 15}},
                         "Lustrous Amethyst": {"Chance": 40, "Multis": {"Crystal": 100, "Iron": 25, "Quartz": 15}},
                         "Molten Iron": {"Chance": 90, "Multis": {"Iron": 100, "Gold": 50, "Jade": 25}},
                         "Fools Gold": {"Chance": 200, "Multis": {"Gold": 100, "Quartz": 50, "Obsidian": 10}},
                         "Exotic Quartz": {"Chance": 450, "Multis": {"Quartz": 200, "Jade": 50, "Obsidian": 25}},
                         "Grossular Jade": {"Chance": 900, "Multis": {"Jade": 250, "Ruby": 50, "Emerald": 50, "Sapphire": 50}},
                         "Purple Obsidian": {"Chance": 1700, "Multis": {"Obsidian": 500, "Diamond": 25, "Starlight": 10}},
                         "Black Diamond": {"Chance": 2900, "Multis": {"Diamond": 250, "Starlight": 100, "Ion": 25}},
                         "Enlightened Starlight": {"Chance": 5100, "Multis": {"Starlight": 750, "Ion": 50, "Uranium": 25}},
                         "Supercharged Ion": {"Chance": 11000, "Multis": {"Ion": 250, "Uranium": 50, "Bismuth": 15}},
                         "Chromatic Bismuth": {"Chance": 22500, "Multis": {"Bismuth": 100, "Boracite": 25, "Nissonite": 5}},
                         "Sparkling Nissonite": {"Chance": 52000, "Multis": {"Nissonite": 50, "Orpiment": 10, "Tetra": 3}},
                         "Pure Orpiment": {"Chance": 90100, "Multis": {"Orpiment": 25, "Tetra": 10, "Volt": 5}},
                         "Indestructible Tetra": {"Chance": 160000, "Multis": {"Tetra": 45, "Volt": 25, "Aquamarine": 5}},
                         "Hypercharged Volt": {"Chance": 520000, "Multis": {"Volt": 30, "Aquamarine": 20, "Lollipop": 10}},
                         "Galaxium": {"Chance": 1200000, "Multis": {"Aquamarine": 250, "Lollipop": 10, "C0RR8PT10N": 3}},
                         "Mythralite": {"Chance": 3100000, "Multis": {"Tetra": 100, "Volt": 100, "Aquamarine": 100, "C0RR8PT10N": 9}},
                         "Phantasmite": {"Chance": 5900000, "Multis": {"Lollipop": 5, "C0RR8PT10N": 15, "Stargazed Metal": 3}},
                         "Eclipsium": {"Chance": 12500000, "Multis": {"Aquamarine": 10000, "Lollipop": 200, "Stargazed Metal": 5, "Gyge": 1.5}},
                         "Aetherite": {"Chance": 21000000, "Multis": {"Lollipop": 50, "C0RR8PT10N": 40, "Stargazed Metal": 10, "Gyge": 2.5, "Auly Plate": 1.2}},
                         "Aurorite": {"Chance": 32000000, "Multis": {"Lollipop": 60, "C0RR8PT10N": 50, "Stargazed Metal": 12, "Gyge": 4, "Auly Plate": 2}},
                         "Crysalith": {"Chance": 52000000, "Multis": {"Stargazed Metal": 5, "Gyge": 4, "Auly Plate": 3, "Shell Piece": 1.1}},
                         "Vortexium": {"Chance": 74600000, "Multis": {"C0RR8PT10N": 1000, "Gyge": 20, "Auly Plate": 4.5, "Shell Piece": 1.5}},
                         "Ignisium": {"Chance": 96100000, "Multis": {"C0RR8PT10N": 1e6, "Auly Plate": 10, "Shell Piece": 2}},
                         "Luminaris": {"Chance": 210000000, "Multis": {"C0RR8PT10N": 1e8, "Stargazed Metal": 3000, "Gyge": 50, "Auly Plate": 20, "Shell Piece": 3}},
                         "Chronicality": {"Chance": 750163471, "Multis": {"Stargazed Metal": 100000, "Gyge": 20, "Auly Plate": 100, "Shell Piece": 5, "Prime Alpha Key": 1.5}},
                         "Amalgamation": {"Chance": 1842817456, "Multis": {"Volt": 1e20, "Aquamarine": 1e15, "Lollipop": 1e12, "C0RR8PT10N": 1e10, "Stargazed Metal": 1e6, "Gyge": 100, "Auly Plate": 250, "Shell Piece": 10, "Prime Alpha Key": 2}},
                         "Purity": {"Chance": 17891091451, "Multis": {"Uranium": Mantissa(1,300), "Bismuth": Mantissa(1,300), "Boracite": Mantissa(1,300), "Nissonite": Mantissa(1,300), "Orpiment": Mantissa(1,300), "Tetra": Mantissa(1,300), "Volt": Mantissa(1,300), "Aquamarine": 1e45, "Lollipop": 1e40, "C0RR8PT10N": 1e20, "Prime Alpha Key": 7.5}},
                         "Totality": {"Chance": 47145471001, "Multis": {"Ion": Mantissa(1,300), "Uranium": Mantissa(1,300), "Bismuth": Mantissa(1,300), "Boracite": Mantissa(1,300), "Nissonite": Mantissa(1,300), "Orpiment": Mantissa(1,300), "Tetra": 1e200, "Volt": 1e100, "Aquamarine": 1e55, "Lollipop": 1e50, "C0RR8PT10N": 1e30, "Prime Alpha Key": 15}},
                         },
      "Unlucky Geode": {
          "ant": {"Multis": None},
          "unlucky stone": {"Multis": None},
          "silly stat": {"Multis": None},
          "mendozite": {"Multis": None},
          "kinda lucky stone": {"Multis": None},
          "womendozite": {"Multis": None},
          "lucky stone": {"Multis": None},
          "silly stat 2": {"Multis": None},
          "silly stat 4": {"Multis": None},
          "toiletum": {"Multis": None},
          "upvotium": {"Multis": None},
          "colourscriptsample": {"Multis": None},
          "spectrafractum": {"Multis": None},
          "very lucky stone": {"Multis": None},
          "silly stat 5": {"Multis": None},
          "hitbox": {"Multis": None},
          "sotne": {"Multis": None},
          "almost 💔": {"Multis": None},
          "silly stat 3": {"Multis": None},
          "eulogy to the dead god": {"Multis": None},
          "legacy eyselite": {"Multis": None},
          "polyprism": {"Multis": None},
          "mayb3_w0rld": {"Multis": None},
          "synthase": {"Multis": None},
          "flawless grandidierite": {"Multis": None},
          "silly stat 6": {"Multis": None},
          "phosphoribosylaminoimidazolesuccinocarboxamide": {"Multis": None},
          "gullibilius": {"Multis": None},
      }
  }
}
stat_gradients = {
    "Gems": {"Colours": ["#f9fb7c", "#fefe01"], "Angle": 180},
    "Event Power": {"Colours": ["#00ff7c", "#00ff02"], "Angle": 180},
    "Cash": {"Colours": ["#55c82f", "#4bb82c"], "Angle": 90},
    "Multiplier": {"Colours": ["#f79292", "#f66161"], "Angle": 90},
    "Rebirths": {"Colours": ["#a39afa", "#7b75e5"], "Angle": 90},
    "Stone": {"Colours": ["#a6a6a6", "#8e8e8e"], "Angle": 90},
    "White Gems": {"Colours": ["#e3e3e3", "#d8d8d8"], "Angle": 90},
    "Crystal": {"Colours": ["#5432ae", "#5123bb"], "Angle": 90},
    "Iron": {"Colours": ["#3f3f15", "#3c3c16"], "Angle": 90},
    "Gold": {"Colours": ["#ffff7f", "#fffff8", "#ffff22", "#fffff3", "#fbfb01"], "Angle": 135},
    "Quartz": {"Colours": ["#88f7f9", "#50f9fc", "#caffff"], "Angle": 135},
    "Jade": {"Colours": ["#005500", "#0b9267", "#15807e"], "Angle": 135},
    "Obsidian": {"Colours": ["#000000", "#221313", "#000000"], "Angle": 135},
    "Ruby": {"Colours": ["#ff3c3c", "#f52c2c"], "Angle": 90},
    "Emerald": {"Colours": ["#a1ff73", "#b8f79b", "#abff82"], "Angle": 90},
    "Sapphire": {"Colours": ["#2829ff", "#4647f9"], "Angle": 90},
    "Diamond": {"Colours": ["#00aaff", "#ffffff", "#15b1ff", "#ffffff", "#87d7ff"], "Angle": 90},
    "Starlight": {"Colours": ["#ffff20", "#83ffed", "#ffffff", "#87d7ff"], "Angle": 90},
    "Ion": {"Colours": ["#a2a200", "#000609", "#00476b"], "Angle": 90},
    "Uranium": {"Colours": ["#4fff77", "#03ff05"], "Angle": 90},
    "Bismuth": {"Colours": ["#ffb9b7", "#90ff9a", "#aeccf8"], "Angle": 90},
    "Boracite": {"Colours": ["#00c0ff", "#ffffff", "#00c0ff"], "Angle": 90},
    "Nissonite": {"Colours": ["#aaffff", "#5556ff"], "Angle": 135},
    "Orpiment": {"Colours": ["#cf0000", "#f64100"], "Angle": 90},
    "Tetra": {"Colours": ["#2b747d", "#346ca6"], "Angle": 90},
    "Volt": {"Colours": ["#7d7900", "#fdf500", "#000000"], "Angle": 90},
    "Aquamarine": {"Colours": ["#283d8c", "#0cb668"], "Angle": 90},
    "Lollipop": {"Colours": ["#ffffff", "#ff6868"], "Angle": 90},
    "C0RR8PT10N": {"Colours": ["#7811c7", "#de4530"], "Angle": 180},
    "Stargazed Metal": {"Colours": ["#9c4fbe", "#6b0bf9"], "Angle": 180},
    "Gyge": {"Colours": ["#9c4fbe", "#33220f"], "Angle": 180},
    "Auly Plate": {"Colours": ["#80f2c1", "#ebfbab"], "Angle": 180},
    "Shell Piece": {"Colours": ["#2b2e2f", "#b5b8b8"], "Angle": 180},
    "Singularity": {"Colours": ["#ffffff","#ffffff","#6a6a6a","#000000","#6a6a6a","#ffffff","#6a6a6a","#000000","#6a6a6a","#ffffff","#6a6a6a","#000000","#6a6a6a","#ffffff","#ffffff"], "Angle": 100},
    "Capsuled Singularity": {"Colours": ["#323232", "#323232", "#323232", "#000000", "#9e9e9e", "#ffffff", "#9e9e9e", "#000000", "#323232", "#323232", "#323232"], "Angle": 135},
    "Mint": {"Colours": ["#c6ffd0", "#58fbd7"], "Angle": 90},
    "Buttons Pressed": {"Colours": ["#3e87a7", "#1b9fa2"], "Angle": 90},
    "Geodes Opened": {"Colours": ["#bc682d", "#d76d13"], "Angle": 90},
    "Dezyp": {"Colours": ["#333833", "#2e382d"], "Angle": 90},
    "Podrillium": {"Colours": ["#7DDAFF", "#D97652", "#952DD6", "#8BC389", "#EDDD53"], "Angle": 9},
    "Digenite": {"Colours": ["#525742", "#435359"], "Angle": 90},
    "Oneillite": {"Colours": ["#a7fbd7", "#abf7ff", "#b5fbde"], "Angle": 90},
    "Alum": {"Colours": ["#d0d7d7", "#a9aeab"], "Angle": 90},
    "Chaoite": {"Colours": ["#391515", "#291715"], "Angle": 180},
    "Amethyst": {"Colours": ["#5517ff", "#553eff"], "Angle": 90},
    "Paradoxite": {"Colours": ["#5500ff", "#55007f"], "Angle": 135},
    "Silver": {"Colours": ["#eaeaea", "#bfbfbf"], "Angle": 180},
    "Platinum": {"Colours": ["#7b7b7b", "#dbdbdb"], "Angle": 180},
    "Mythril": {"Colours": ["#202dc0", "#57d5f4"], "Angle": 180},
    "Yellow Beryl": {"Colours": ["#76bace", "#dbee35"], "Angle": 180},
    "Opal": {"Colours": ["#ddf490", "#298fff", "#fe00ff", "#acf807"], "Angle": 90},
    "Holeyum": {"Colours": ["#a8ffff", "#56ffff"], "Angle": 180},
    "Pink Quartz": {"Colours": ["#badeff", "#ee79ff"], "Angle": 180},
    "Cyan Quartz": {"Colours": ["#81ffff", "#2cffff"], "Angle": 180},
    "Black Quartz": {"Colours": ["#89cece", "#2c4242"], "Angle": 180},
    "Garnet": {"Colours": ["#e70101", "#b70000"], "Angle": 180},
    "Milky Quartz": {"Colours": ["#f1f1f1", "#272727"], "Angle": 180},
    "Jurite": {"Colours": ["#36aa7f", "#36aa7f"], "Angle": 90},
    "Molybendum": {"Colours": ["#959595", "#192732"], "Angle": 90},
    "Rbadam's Smokestackite": {"Colours": ["#0f0f0f","#173e1e" ,"#1a591b"], "Angle": 170},
    ":3": {"Colours": ["#000000", "#000000"], "Angle": 0, "File": "3"},
    "O_O": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "^_^": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "'-'": {"Colours": ["#000000", "#000000"], "Angle": 0},
    ":D": {"Colours": ["#000000", "#000000"], "Angle": 0, "File": "smiley"},
    "OwO": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "UwU": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "Draconite": {"Colours": ["#d943ff", "#740fff"], "Angle": 180},
    "Burneite": {"Colours": ["#f14769", "#b90f17"], "Angle": 180},
    "Dragonglass": {"Colours": ["#550095", "#5401f5"], "Angle": 180},
    "Hellyerite": {"Colours": ["#7bc700", "#f10a02"], "Angle": 180},
    "Palladium": {"Colours": ["#939d6c", "#00ffff"], "Angle": 90},
    "Osumillite": {"Colours": ["#074f0b", "#104d73", "#a40304"], "Angle": 0},
    "Pascoite": {"Colours": ["#f09465", "#ff6417"], "Angle": 180},
    "Roselite": {"Colours": ["#ff8738", "#ff5a31"], "Angle": 180},
    "Wulfenite": {"Colours": ["#ff5300", "#ff0100"], "Angle": 180},
    "Olivine": {"Colours": ["#55f169", "#55be1d"], "Angle": 180},
    "Heazlewoodite": {"Colours": ["#43ff9c", "#0fffe8"], "Angle": 180},
    "Gaspeite": {"Colours": ["#53ac7f", "#01fe7f"], "Angle": 180},
    "Talc": {"Colours": ["#a9fffd", "#56ff81"], "Angle": 180},
    "Lapis": {"Colours": ["#006bcf", "#000e89"], "Angle": 180},
    "Ringwoodite": {"Colours": ["#0ff0de", "#4cff8c"], "Angle": 180},
    "Kyanite": {"Colours": ["#0caaff", "#4caaff"], "Angle": 180},
    "Azurite": {"Colours": ["#5355fc", "#015581"], "Angle": 90},
    "Cobalt": {"Colours": ["#53fcff", "#0258ff"], "Angle": 180},
    "Spatial Dust": {"Colours": ["#baba96", "#46426d"], "Angle": 90},
    "Astrophyllite": {"Colours": ["#2b9cd6", "#5e17fe"], "Angle": 90},
    "Niter": {"Colours": ["#f60986", "#5ca3f9", "#f60986", "#5ca3f9"], "Angle": 180},
    "Yrnote": {"Colours": ["#ffad05", "#fffe7d"], "Angle": 180},
    "Sercense": {"Colours": ["#feabf8", "#fffe03"], "Angle": 180},
    "Neuron": {"Colours": ["#e2c7ff", "#c7e2ff"], "Angle": 90},
    "Antimatter": {"Colours": ["#4d06ff", "#191bff"], "Angle": 90},
    "Sphene": {"Colours": ["#1baaff", "#3baaff"], "Angle": 90},
    "Acid": {"Colours": ["#8ca758", "#7257a8"], "Angle": 90},
    "Niflhemite": {"Colours": ["#61006c", "#c20029"], "Angle": 90},
    "Reactivite": {"Colours": ["#8aff93", "#aeff71"], "Angle": 990},
    "Plutonerite": {"Colours": ["#ff6400", "#fffc00", "#ff5900"], "Angle": 135},
    "Grail": {"Colours": ["#faa701", "#f3f37a"], "Angle": 90},
    "Box": {"Colours": ["#a25320", "#aa555c"], "Angle": 90},
    "Lead": {"Colours": ["#1e2020", "#191b1c"], "Angle": 90},
    "Pseudomalachite": {"Colours": ["#00b995", "#00f1ea"], "Angle": 90},
    "Osmium": {"Colours": ["#a9cec7", "#7fc4b6"], "Angle": 90},
    "Yhed": {"Colours": ["#2c251b", "#2c251b"], "Angle": 90},
    "Hexaferrum": {"Colours": ["#8ee2fd", "#d5ffc7"], "Angle": 90},
    "Spectrolite": {"Colours": ["#1f1c3f", "#d5ffcf"], "Angle": 180},
    "Hectam": {"Colours": ["#5510ff", "#5544ff"], "Angle": 180},
    "Frostone": {"Colours": ["#00d6db", "#005a6d"], "Angle": 180},
    "Neptunian": {"Colours": ["#0015ff", "#0050ff"], "Angle": 180},
    "Clouminance": {"Colours": ["#6dded0", "#2a565f"], "Angle": 180},
    "Galarium": {"Colours": ["#7700ff", "#090088", "#7700ff"], "Angle": 145},
    "Unova": {"Colours": ["#00ffff", "#000000", "#00ffff"], "Angle": 145},
    "Borax": {"Colours": ["#ac5353", "#52adad"], "Angle": 90},
    "Axiom": {"Colours": ["#1d72ff", "#388dff"], "Angle": 90},
    "Vergemite": {"Colours": ["#cd3d00", "#7e1900"], "Angle": 90},
    "Zanyte": {"Colours": ["#cb4eb1", "#5af609"], "Angle": 90},
    "Secretum": {"Colours": ["#ff7700", "#ff6161"], "Angle": 180},
    "Mortalstone": {"Colours": ["#ff00ff", "#ff00ff", "#000000", "#000000"], "Angle": 145},
    "Uzik": {"Colours": ["#269069", "#2cb196"], "Angle": 90},
    "Omet": {"Colours": ["#55D946", "#55D946"], "Angle": 0},
    "Badges": {"Colours": ["#b50202","#b50202","#9af119","#ea5bda","#a356ef", "#a356ef"],"Angle": 9},
    "Stellarite": {"Colours": ["#094887", "#015e8c"], "Angle": 90},
    "Galaxite": {"Colours": ["#821ced", "#2f2f2f", "#6e2eea"], "Angle": 180},
    "Graphite": {"Colours": ["#ed3636", "#757780", "#4866d0"], "Angle": 90},
    "Darkmatter": {"Colours": ["#000000", "#000000"], "Angle": 90},
    "Starglass": {"Colours": ["#1b74ff", "#4226ff"], "Angle": 90, "S_Colour": "#000000", "S_Width": 1.5},
    "Testium": {"Colours": ["#4747f3", "#34348c", "#0000ff"], "Angle": 145},
    "Ivory": {"Colours": ["#fef5ba", "#d3f5ea"], "Angle": 90},
    "Alpha Point": {"Colours": ["#ff7fff", "#d935e6"], "Angle": 90},
    "Leaf": {"Colours": ["#ffdc7f", "#ffdc7f"], "Angle": 0},
    "Acorn": {"Colours": ["#787822", "#787822"], "Angle": 0},
    "Pine": {"Colours": ["#6d3800", "#6d3800"], "Angle": 0},
    "Chestnut": {"Colours": ["#643920", "#724a33"], "Angle": 135},
    "Candy": {"Colours": ["#ffffff", "#ffaa01", "#ffffff", "#ffaa01", "#edca86"], "Angle": 90},
    "Bat": {"Colours": ["#000000", "#18181e"], "Angle": 135},
    "Wicked Branch": {"Colours": ["#0a1f28", "#1d1811"], "Angle": 135},
    "Bone": {"Colours": ["#e0e0e0", "#8c8c8c"], "Angle": 180},
    "Mushroom": {"Colours": ["#ff8a8a", "#ff0c0c", "#ffffff", "#ff0c0c", "#ffffff", "#ff5959"], "Angle": 90},
    "Pumpkin": {"Colours": ["#ffff00", "#ffbc63"], "Angle": 135},
    "Clover": {"Colours": ["#40ff7f", "#14ff74"], "Angle": 135},
    "Heart": {"Colours": ["#ff007f", "#ff004e"], "Angle": 135},
    "Orange Pumpkin": {"Colours": ["#c8640c", "#5b3311"], "Angle": 135},
    "Ray": {"Colours": ["#ffeca7", "#fff2c0"], "Angle": 90},
    "Patriotic Crystal": {"Colours": ["#ff7e7e", "#ffffff", "#8bbfff"], "Angle": 135},
    "Aureal Gem": {"Colours": ["#ffff7f", "#f890ff"], "Angle": 135},
    "Fragment": {"Colours": ["#ffffff", "#434343"], "Angle": 135},
    "Sweet": {"Colours": ["#f9a7f9", "#ffaa7f"], "Angle": 90},
    "Ichor Flower": {"Colours": ["#ffaa7f", "#aa0000"], "Angle": 90},
    "Halved Heart": {"Colours": ["#ff0000", "#000000"], "Angle": 90},
    "Rainbow": {"Colours": ["#ff0000", "#ff7600", "#eee300", "#7bf72e", "#01fcc7", "#005dfe", "#ff00ea"], "Angle": 90},
    "Unicorn": {"Colours": ["#55aaff", "#ffaaff"], "Angle": 90},
    "Rose": {"Colours": ["#fe577e", "#a0fa03"], "Angle": 90},
    "Wickedite": {"Colours": ["#55557f", "#aa557f"], "Angle": 90},
    "Heartium": {"Colours": ["#ff53fa", "#f70202"], "Angle": 90},
    "Eternal Rose": {"Colours": ["#4a68f9", "#01fdfe"], "Angle": 90},
    "Lucky Clover": {"Colours": ["#d0f37a", "#1aff7f"], "Angle": 180},
    "Golden Clover": {"Colours": ["#ffec1d", "#f0af7f"], "Angle": 180},
    "Diamond Clover": {"Colours": ["#3ec1ff", "#00ffad"], "Angle": 90},
    "Leprechaun's Hat": {"Colours": ["#55ff00", "#000000", "#ffff00", "#000000", "#55ff00"], "Angle": 90},
    "Supreme Clover": {"Colours": ["#54c8fa", "#8affff"], "Angle": 90},
    "Cloverite": {"Colours": ["#3d3d3d", "#59a57e", "#777979", "#57f608", "#777979", "#59a57e", "#3d3d3d"], "Angle": 145},
    "Ace": {"Colours": ["#000000", "#fe0000", "#00003a", "#0000ec", "#00003a", "#fe0000", "#000000"], "Angle": 145},
    "777": {"Colours": ["#000000", "#ffff00", "#000000", "#ffff00", "#000000", "#ffff00", "#000000"], "Angle": 145},
    "Holy Clover": {"Colours": ["#87ffe5", "#23ff99"], "Angle": 90},
    "Red Clover": {"Colours": ["#c8371b", "#36c965"], "Angle": 90},
    "Death Clover": {"Colours": ["#00351a", "#00cc66"], "Angle": 90},
    "Oblivion Clover": {"Colours": ["#2b297f", "#08d87f"], "Angle": 90},
    "Giant Clover": {"Colours": ["#009c61", "#00e376"], "Angle": 90},
    "Albino Clover": {"Colours": ["#ffffff", "#ff0000", "#ffffff", "#55ffaa"], "Angle": 90},
    "Tripetaled": {"Colours": ["#00ff7f", "#00b915"], "Angle": 90},
    "Oddium": {"Colours": ["#585800", "#000000", "#5d0000"], "Angle": 90},
    "Dualpetaled": {"Colours": ["#3dc25c", "#17e823"], "Angle": 90},
    "Core Clover": {"Colours": ["#00c3e8", "#00e6ca"], "Angle": 90},
    "Luckant": {"Colours": ["#55ff00", "#55fff6", "#55ff00"], "Angle": 145},
    "Jackpotium": {"Colours": ["#000000", "#ffff00", "#000000", "#fa6801", "#ffff00", "#fa6801", "#000000", "#ffff00", "#000000"], "Angle": 145},
    "Reality": {"Colours": ["#ffffff", "#ffffff", "#2f2f2f", "#ffffff", "#ffffff"], "Angle": 145, "S_Colour": "#8f93bc", "S_Width": 1},
    "Goldenium": {"Colours": ["#ffff7f", "#ffff7f"], "Angle": 90},
    "Lightroom": {"Colours": ["#ffdfff", "#f255f2", "#ffdfff"], "Angle": 180},
    "Dazzlium": {"Colours": ["#f9a754", "#ff7c00"], "Angle": 180},
    "Juled": {"Colours": ["#47f17f", "#18c27f"], "Angle": 180},
    "Tempested": {"Colours": ["#07004c", "#260148"], "Angle": 180},
    "Cyclone": {"Colours": ["#103e3f", "#103e3f", "#103e3f", "#00d7dc", "#103e3f", "#103e3f", "#103e3f"], "Angle": 180},
    "Koanite": {"Colours": ["#100e02", "#282602", "#100e02"], "Angle": 180},
    "Torbdenum": {"Colours": ["#1f5340", "#39845f", "#1f5340"], "Angle": 180},
    "Darnite": {"Colours": ["#170d00", "#3e7300", "#390800"], "Angle": 180},
    "Wubium": {"Colours": ["#5500ff", "#55557f", "#5500ff"], "Angle": 145},
    "Woofern": {"Colours": ["#47475c", "#47475c", "#525277", "#474761", "#474761"], "Angle": 180, "S_Colour": "#353675", "S_Width": 1},
    "Acastar": {"Colours": ["#ffff0d", "#a2ff5d", "#5cffa3", "#1bffff"], "Angle": 90},
    "Zinction": {"Colours": ["#ffff00", "#ffff00"], "Angle": 90},
    "Prismatum": {"Colours": ["#000000", "#02a3f2", "#54f303", "#fd0d0d", "#ffffff"], "Angle": 90},
    "Vine": {"Colours": ["#047354", "#00674a", "#007f5d"], "Angle": 90},
    "Dew": {"Colours": ["#9ed5b5", "#a7d8d8"], "Angle": 90},
    "Daisy": {"Colours": ["#fbff82", "#edf074"], "Angle": 90},
    "Tulip": {"Colours": ["#f24e25", "#faea04"], "Angle": 180},
    "Aster": {"Colours": ["#c426ff", "#c426ff"], "Angle": 90},
    "Honeysuckle": {"Colours": ["#ffffb8", "#fcff49", "#ffffb8"], "Angle": 90},
    "Trollius": {"Colours": ["#ffeda6", "#ffeda6"], "Angle": 90},
    "Nymphea": {"Colours": ["#ffc765", "#d4bafb", "#ffc765"], "Angle": 90},
    "Sunflower": {"Colours": ["#f4ff6a", "#fefd97", "#ffdd52"], "Angle": 90},
    "Yarrow": {"Colours": ["#ff858c", "#f44d6c", "#ff6f89"], "Angle": 90},
    "Windflower": {"Colours": ["#8cf3f4", "#70c0b8", "#a3f3cf"], "Angle": 90},
    "Bachelor's Button": {"Colours": ["#091df9", "#63adba", "#091df9"], "Angle": 90},
    "Egg": {"Colours": ["#fed1ab", "#fcabd9"], "Angle": 90},
    "Tainted Egg": {"Colours": ["#d5badb", "#a6fea1", "#b3dadb"], "Angle": 90},
    "Spotted Egg": {"Colours": ["#f5ff9b", "#000000", "#a1fbff", "#000000", "#acffaa"], "Angle": 90},
    "Equinox Egg": {"Colours": ["#323232", "#c0c0c0"], "Angle": 90},
    "Sugar Egg": {"Colours": ["#e188d6", "#fda5e3", "#e188d6"], "Angle": 90},
    "Time Egg": {"Colours": ["#8f743a", "#44371a", "#8f743a"], "Angle": 90},
    "Malicious Egg": {"Colours": ["#246800", "#c2fe9d", "#246800", "#86ff79"], "Angle": 145},
    "Stained Glass Egg": {"Colours": ["#9ff8fc", "#b4aaff", "#fcabd9"], "Angle": 90},
    "Space Egg": {"Colours": ["#382932", "#332b56"], "Angle": 90},
    "Gravitational Egg": {"Colours": ["#0008b2", "#0039ff"], "Angle": 90},
    "EGG9000": {"Colours": ["#ff005a", "#ff0087", "#ff005a"], "Angle": 90},
    "Dust Devil Egg": {"Colours": ["#ffbb45", "#ffd07e", "#ffbb45"], "Angle": 90},
    "Black Iron Fabergé": {"Colours": ["#101010", "#2a2a2a", "#101010"], "Angle": 90},
    "Gilded Fabergé": {"Colours": ["#857608", "#f6d519", "#99771f"], "Angle": 90},
    "Royal Fabergé": {"Colours": ["#a811ff", "#fc279d"], "Angle": 90},
    "Easter Basket": {"Colours": ["#fcb1ad", "#fbfca6", "#c4feb4", "#aaaaf5", "#f5a4f7", "#ffa4b0"], "Angle": 90},
    "Egg of Destiny": {"Colours": ["#ffffff", "#ffffff", "#000000", "#ffffff", "#ffffff"], "Angle": 145},
    "Shinestone": {"Colours": ["#383838", "#ffff7f"], "Angle": 90},
    "Yen": {"Colours": ["#a59a43", "#fefea5", "#bfc043"], "Angle": 90},
    "Ascension": {"Colours": ["#0016fe", "#003fff"], "Angle": 90},
    "Translucid Gem": {"Colours": ["#99fdff", "#5cffff", "#98ffd2"], "Angle": 90},
    "Luminant Crystal": {"Colours": ["#e981ff", "#f166f4", "#80c3f3"], "Angle": 90},
    "Exotic Metal": {"Colours": ["#a8a985", "#f4f5a6", "#9c9d7a"], "Angle": 90},
    "Polyhedral Gold": {"Colours": ["#728f5d", "#b3b507", "#728f5d"], "Angle": 90},
    "Luxurious Quartz": {"Colours": ["#86e6db", "#d09ff9", "#f3d1aa"], "Angle": 90},
    "Scarlet Jade": {"Colours": ["#b15291", "#43654a", "#b15291"], "Angle": 90},
    "Reflected Obsidian": {"Colours": ["#1d181a", "#7a636e", "#5b4c62", "#151117"], "Angle": 90},
    "Chromio": {"Colours": ["#868700", "#22f300", "#0d857a"], "Angle": 90},
    "Clusterized Diamond": {"Colours": ["#fbb4ff", "#bdf8f2", "#fbb4ff", "#bdf8f2", "#fbb4ff", "#bdf8f2", "#fbb4ff", "#bdf8f2", "#fbb4ff"], "Angle": 90},
    "Cosmodryal": {"Colours": ["#6826ff", "#9483fa"], "Angle": 90},
    "Augmented Ion": {"Colours": ["#ff0000", "#000000", "#52ec04"], "Angle": 90},
    "Symmetrite": {"Colours": ["#5500fd", "#f10014", "#51e606"], "Angle": 90},
    "Levigated Bismuth": {"Colours": ["#cbc7ff", "#b4ddc0", "#e9e5a9", "#f0afc2", "#cbc7ff"], "Angle": 90},
    "Niflhemic Boracite": {"Colours": ["#00ffff", "#5500ff"], "Angle": 90},
    "Encored Nissonite": {"Colours": ["#aaffff", "#5fffff", "#aaffff", "#5fffff"], "Angle": 90},
    "Ethereal Orpiment": {"Colours": ["#ff5500", "#049fed"], "Angle": 90},
    "Charged Tetra": {"Colours": ["#0055ff", "#fc0103", "#0055ff"], "Angle": 90},
    "Overclocked Volt": {"Colours": ["#ffff00", "#ffffff", "#ffff00"], "Angle": 90},
    "Agate": {"Colours": ["#afffff", "#ffffff"], "Angle": 90},
    "Bustamite": {"Colours": ["#555500", "#551800"], "Angle": 90},
    "Polycrase": {"Colours": ["#ffff7f", "#ffaa7f"], "Angle": 90},
    "Stolzite": {"Colours": ["#fc5400", "#aaaa00"], "Angle": 90},
    "Zeunerite": {"Colours": ["#f50202", "#ff5500"], "Angle": 90},
    "Phosphophyllite": {"Colours": ["#5555ff", "#00ffff", "#00aaff"], "Angle": 90},
    "Haxonite": {"Colours": ["#55ff7f", "#000000"], "Angle": 90},
    "Glaucodot": {"Colours": ["#ffffff", "#8a694c", "#ffffff"], "Angle": 90},
    "Dyscrasite": {"Colours": ["#5e5e5e", "#ffffff"], "Angle": 90},
    "Bazzite": {"Colours": ["#97e1f5", "#3fd2ff"], "Angle": 90},
    "Cornubite": {"Colours": ["#a9fd7e", "#a9fd00"], "Angle": 90},
    "Kostovite": {"Colours": ["#eea0ee", "#ffffff", "#eea0ee", "#ffffff", "#eea0ee"], "Angle": 90},
    "Minium": {"Colours": ["#5e5e12", "#a7a77a", "#5e5e12"], "Angle": 90},
    "Nyerereite": {"Colours": ["#00aa05", "#33aa7f"], "Angle": 90},
    "Peridot": {"Colours": ["#07a07b", "#54fefe", "#02ac82"], "Angle": 90},
    "Realgar": {"Colours": ["#ff0300", "#fffa00"], "Angle": 90},
    "Ereus": {"Colours": ["#ffff84", "#ffffff", "#ffff84"], "Angle": 90},
    "Existence": {"Colours": ["#000000", "#000000", "#000000", "#ffffff", "#000000", "#000000", "#000000"], "Angle": 90},
    "Master Cash": {"Colours": ["#5dbc20", "#4fa61c"], "Angle": 90},
    "Master Multiplier": {"Colours": ["#f7916a","#e13f30"], "Angle": 90},
    "Master Rebirths": {"Colours": ["#b2909e","#6d5c96"], "Angle": 90},
    "Master Stone": {"Colours": ["#b08f73","#9a795d"], "Angle": 90},
    "Master White Gems": {"Colours": ["#e0b791","#ddae87"], "Angle": 90},
    "Master Crystal": {"Colours": ["#502971","#511d7c"], "Angle": 90},
    "Master Iron": {"Colours": ["#42340a","#373010"], "Angle": 90},
    "Master Gold": {"Colours": ["#fdc84d","#fec887","#ffc800"], "Angle": 135},
    "Master Quartz": {"Colours": ["#ffc89b","#48c69b","#cac89b"], "Angle": 135},
    "Master Jade": {"Colours": ["#004300","#004300","#038e4c","#00a244"], "Angle": 135},
    "Master Obsidian": {"Colours": ["#000000","#000000","#140202","#000000","#000000"], "Angle": 135},
    "Master Ruby": {"Colours": ["#f93026","#f9231c"], "Angle": 90},
    "Master Emerald": {"Colours": ["#98c953","#bdc861","#aac84f"], "Angle": 90},
    "Master Sapphire": {"Colours": ["#2a219b","#41349b"], "Angle": 90},
    "Master Diamond": {"Colours": ["#00859b","#00859b","#00859b","#f7c69b","#00859b","#f7c69b","#00859b","#00859b"], "Angle": 90},
    "Master Starlight": {"Colours": ["#ffc89b","#ffc89b","#ffc816","#3fc881","#f7c69b","#3fc881","#ffc816","#ffc89b","#ffc89b"], "Angle": 90},
    "Master Ion": {"Colours": ["#ffc800", "#ffc800","#000000","#007f96","#000000"], "Angle": 135},
    "Master Uranium": {"Colours": ["#55c84d","#00c800"], "Angle": 90},
    "Master Bismuth": {"Colours": ["#ff906f","#ff906f","#9ac86e","#ae9d98","#ff747f"], "Angle": 90},
    "Master Boracite": {"Colours": ["#00859b","#fbc89b","#0186a7"], "Angle": 90},
    "Master Nissonite": {"Colours": ["#9ac9a5","#53439e"], "Angle": 90},
    "Master Orpiment": {"Colours": ["#ba0101","#ff4000"], "Angle": 90},
    "Master Tetra": {"Colours": ["#275b43","#3f3a93"], "Angle": 90},
    "Master Volt": {"Colours": ["#000000","#000000","#f8bd00","#000000","#493a00"], "Angle": 90},
    "Master Aquamarine": {"Colours": ["#283055","#0c9240"], "Angle": 90},
    "Master Lollipop": {"Colours": ["#ffc89b","#ff1712"], "Angle": 90},
    "Prime Alpha Key": {"Colours": ["#bc0164","#ea008e"], "Angle": 90},
    "Master Mint": {"Colours": ["#b1c880","#61c488"], "Angle": 180},
    "Master Gems": {"Colours": ["#f9fb7c", "#fefe01"], "Angle": 180},
    "Master Event Power": {"Colours": ["#00ff7c", "#00ff02"], "Angle": 180},
    "Charcoal": {"Colours": ["#111111","#190d0d"], "Angle": 90},
    "Flamecrystal": {"Colours": ["#ff861c","#ff861c","#ffa404","#ff1008","#ff1008"], "Angle": 135},
    "Torbernite": {"Colours": ["#212121","#212121","#37fe87","#212121","#212121"], "Angle": 135},
    "Manganite": {"Colours": ["#15191d","#15191d"], "Angle": 90},
    "Pyrrhoite": {"Colours": ["#d2fbff","#d2fbff","#1a2205","#d2fbff","#d2fbff"], "Angle": 135},
    "Norbergite": {"Colours": ["#ff5500","#ffaa00","#ff5500","#ffaa00","#ff5500","#ffaa00","#ff5500","#ffaa00","#ff5500","#ffaa00"], "Angle": 135},
    "Moolooite": {"Colours": ["#0fffe3","#0cff79"], "Angle": 90},
    "Lizardite": {"Colours": ["#ffff7f","#ffff7f","#000000","#ff0000","#000000","#ffff7f","#000000","#ff0000","#000000","#ffff7f","#ffff7f"], "Angle": 165},
    "Kassite": {"Colours": ["#1d1d1d","#909049","#1d1d1d"], "Angle": 135},
    "Geocronite": {"Colours": ["#010d02","#110f04"], "Angle": 90},
    "Dioptase": {"Colours": ["#20cbf1","#4097ff","#6bf3f0","#78c8ff"], "Angle": 135},
    "Corkite": {"Colours": ["#b6fbac","#b6fbac","#b6fbac","#000000","#204e3c","#204e3c","#204e3c"], "Angle": 90},
    "Thorium": {"Colours": ["#51fbf8","#fda357","#51fbf8"], "Angle": 90},
    "Qusongite": {"Colours": ["#ab58fd","#fee098"], "Angle": 90},
    "Vulcanite": {"Colours": ["#bca193","#6c584c","#bca193"], "Angle": 90},
    "Carnelite": {"Colours": ["#a8527d","#aa013c"], "Angle": 90},
    "Matter": {"Colours": ["#ffffff","#ffffff","#000000","#ffffff","#ffffff","#000000","#ffffff","#ffffff","#000000","#ffffff","#ffffff"], "Angle": 145},
    "PROT5409-Irosfagum": {"Colours": ["#ffffff","#ffffff","#000000","#ffffff","#ffffff"], "Angle": 90},
    "Radiobarite": {"Colours": ["#41ddff","#1eff69"], "Angle": 90},
    "Uramarsite": {"Colours": ["#ff814f","#472601"], "Angle": 90},
    "Uranopolycrase": {"Colours": ["#476fff","#adff31"], "Angle": 90},
    "Yttrobetafite": {"Colours": ["#ffd12a","#5d00ff"], "Angle": 90},
    "IMA2008-047": {"Colours": ["#c6ffc2","#ffcaf4"], "Angle": 90},
    "Ludlockite": {"Colours": ["#000cff","#000000"], "Angle": 90},
    "Cattite": {"Colours": ["#dba899","#854ff7"], "Angle": 90},
    "Schorl": {"Colours": ["#851e16","#5a5c39"], "Angle": 90},
    "Mixite": {"Colours": ["#49ff6d","#000000","#39ff56","#000000","#26ff39","#000000","#09ff0e"], "Angle": 95},
    "Tellurium": {"Colours": ["#f0f7d9","#dbe9fe"], "Angle": 90},
    "Eyselite": {"Colours": ["#60ffff","#ffffff","#60ffff","#ffffff","#60ffff"], "Angle": 90},
    "Water": {"Colours": ["#a4caff","#b4e0ff"], "Angle": 90},
    "Beach Ball": {"Colours": ["#ff421c","#ff42c9","#58ce9b","#e0da2b","#4b4bff"], "Angle": 95},
    "Ice Cream": {"Colours": ["#532c0f","#b692c1"], "Angle": 90},
    "Umbrella": {"Colours": ["#aea7ba","#ffffff","#bfff0e","#ffffff","#bfff0e"], "Angle": 90},
    "Salt": {"Colours": ["#aea7ba","#5f5c62","#b6a9b9"], "Angle": 90},
    "Rockbottom": {"Colours": ["#464646","#222222"], "Angle": 180},
    "Fossil": {"Colours": ["#9e897b","#807f7f"], "Angle": 90},
    "Bedrock": {"Colours": ["#171717","#161616"], "Angle": 90},
    "Tryglogem": {"Colours": ["#c0e345","#e59044","#bdea45"], "Angle": 135},
    "American Flag": {"Colours": ["#ff0000","#ffffff","#0000ff"], "Angle": 135},
    "Fluorescent Iron": {"Colours": ["#b39848","#a0a659"], "Angle": 90},
    "Fluorite": {"Colours": ["#a5f0a1","#cef1ca","#a5f0a1"], "Angle": 90},
    "Patriotic Opal": {"Colours": ["#0000ff","#ffffff","#ff0000","#0000ff","#ffffff"], "Angle": 90},
    "Silver of Justice": {"Colours": ["#f3f3f3","#898989"], "Angle": 90},
    "Epidote of Liberty": {"Colours": ["#c6e80e","#dcbc36"], "Angle": 90},
    "Fireworks": {"Colours": ["#f85d5d","#ffffff","#5a61f9"], "Angle": 135},
    "Firecracker": {"Colours": ["#f85d5d","#ffffff","#5a61f9"], "Angle": 135},
    "Shinepowder": {"Colours": ["#faeba9","#ffda98"], "Angle": 90},
    "Lightray": {"Colours": ["#ffe5a2","#f6c286"], "Angle": 90},
    "Chalice": {"Colours": ["#e9c262","#cc9545"], "Angle": 90},
    "Halo": {"Colours": ["#ffffd6","#ffffa7"], "Angle": 90},
    "Dimwidth Diamond": {"Colours": ["#79afff","#6de0ff"], "Angle": 90},
    "Eldritch Moonstone": {"Colours": ["#c057ed","#5c5061"], "Angle": 90},
    "Polarstone": {"Colours": ["#dcdcdc","#adadad"], "Angle": 90},
    "Ophanim": {"Colours": ["#ffc72b","#ffe254"], "Angle": 90},
    "Sunstone": {"Colours": ["#c1f92d","#e1ff55"], "Angle": 90},
    "Judgemental Jade": {"Colours": ["#82ee15","#23c443"], "Angle": 90},
    "Glassomophore": {"Colours": ["#C1EDD5","#3EBD7A"], "Angle": 90},
    "Aurora Borealis": {"Colours": ["#9873f4","#fad078","#0db555"], "Angle": 135},
    "Archangel Meridianiite": {"Colours": ["#ffdf8a","#ff645a"], "Angle": 90},
    "Overpurified Sculptanium": {"Colours": ["#84c6f4","#f4cc8f"], "Angle": 90},
    "Bloodstone": {"Colours": ["#8a0b0b","#040000"], "Angle": 90},
    "Soul": {"Colours": ["#606362","#616361"], "Angle": 90},
    "Menace": {"Colours": ["#090200","#451000","#2f0b00"], "Angle": 180},
    "Anger": {"Colours": ["#ff3e1c","#ff3d2e"], "Angle": 90},
    "Emptiness": {"Colours": ["#fffaeb","#767a7a","#b4a5b6"], "Angle": 90},
    "Vastness": {"Colours": ["#ffedf4","#2f2f2f"], "Angle": 155},
    "Fracture": {"Colours": ["#b7b7b7","#2f2f2f","#4b4b4b"], "Angle": 90},
    "Wickstone": {"Colours": ["#382a43","#482664"], "Angle": 180},
    "Chromatory": {"Colours": ["#fbff02","#20eddf","#f700ff"], "Angle": 90},
    "Shatterment": {"Colours": ["#000000","#ffffff","#000000"], "Angle": 175},
    "Deepenlor": {"Colours": ["#161616","#3f1066","#161616"], "Angle": 135},
    "Graphium": {"Colours": ["#9c9c9c","#979797"], "Angle": 90},
    "Vayonium": {"Colours": ["#8880df","#a442b5"], "Angle": 135},
    "Trimonia": {"Colours": ["#320000","#023000","#000032"], "Angle": 90},
    "Defragstone": {"Colours": ["#ae75d8","#ed8b70"], "Angle": 180},
    "Monochromia": {"Colours": ["#0f0f0f","#fafafa"], "Angle": 90},
    "Antaloptide": {"Colours": ["#293a3a","#2e2939"], "Angle": 90},
    "Astatine": {"Colours": ["#a6e4c8","#8cffb7"], "Angle": 90},
    "Vantablack": {"Colours": ["#000000", "#000000"], "Angle": 90},
    "Titanium": {"Colours": ["#6e5385","#b99ec0"], "Angle": 90},
    "Actuality": {"Colours": ["#ffffff", "#000000", "#ffffff"], "Angle": 135},
    "Mist": {"Colours": ["#a4a4a4","#7a7a7a"], "Angle": 180},
    "Vision": {"Colours": ["#690000","#a70000","#690000"], "Angle": 90},
    "Obscurity": {"Colours": ["#1e150e","#000000"], "Angle": 180},
    "The Mark": {"Colours": ["#300704","#491c12"], "Angle": 180},
    "Forgotten": {"Colours": ["#9ab9cf","#a2acf2"], "Angle": 180},
    "Pestilence": {"Colours": ["#256835","#1c5121"], "Angle": 180},
    "Forbidden": {"Colours": ["#6e60a1","#5f5c81"], "Angle": 180},
    "GL1TCH": {"Colours": ["#ffff00","#0000ff","#ff0000","#00ff00"], "Angle": 180},
    "Oblivion": {"Colours": ["#8169f9","#46218e"], "Angle": 90},
    "Brimstone": {"Colours": ["#000000","#ff0000"], "Angle": 135},
    "ù": {"Colours": ["#ffffff","#ffffff"], "Angle": 135},
    "Perishstone": {"Colours": ["#ed0000","#bc0000"], "Angle": 90},
    "Ghostly Gem": {"Colours": ["#adadad","#2f2f2f"], "Angle": 90},
    "Waxy Iron": {"Colours": ["#454133","#33271d"], "Angle": 90},
    "Moonlit Quartz": {"Colours": ["#6697a1","#578898"], "Angle": 90},
    "Looming Crystal": {"Colours": ["#614082","#3e2468"], "Angle": 90},
    "Perilous Gold": {"Colours": ["#c8b846","#ee9d68"], "Angle": 90},
    "Shadowy Jade": {"Colours": ["#54bf7a","#3c5779"], "Angle": 90},
    "Warped Obsidian": {"Colours": ["#554040","#201818","#737373","#756262","#261a1a","#545252","#534646","#000000"], "Angle": 135},
    "Mischievous Agate": {"Colours": ["#95bccb","#80585c"], "Angle": 90},
    "Dastard Emerald": {"Colours": ["#78b645","#7a943c"], "Angle": 90},
    "Rabid Diamond": {"Colours": ["#77a9ce","#c64d66"], "Angle": 90},
    "Preternatural Polybasite": {"Colours": ["#27313d","#282533","#2e2247"], "Angle": 90},
    "Wretched Orpiment": {"Colours": ["#f56b29","#9a6a7c"], "Angle": 90},
    "Cerussite": {"Colours": ["#c9a4f2","#9b89e9","#cb8ad7","#a877cb"], "Angle": 90},
    "Yunium": {"Colours": ["#cffe35","#c6ff68","#8ff22c"], "Angle": 135},
    "Cristobalite": {"Colours": ["#1d1a21","#292c2d","#1d1d1d","#1e2d30"], "Angle": 90},
    "Grimmetal": {"Colours": ["#4b435d","#444e5f"], "Angle": 90},
    "Sestrum": {"Colours": "#92d5d9,#81ffc4".split(","), "Angle": 90},
    "Klovonium": {"Colours": "#65b969,#45d365".split(","), "Angle": 180},
    "Goose's Gold": {"Colours": "#d5e36e,#d5e36e".split(","), "Angle": 180},
    "Concillite": {"Colours": "#aa7457,#c79855".split(","), "Angle": 180},
    "Ztarrium": {"Colours": "#fffb81,#fff99e".split(","), "Angle": 90},
    "Jongium": {"Colours": "#504239,#6b5339".split(","), "Angle": 90},
    "Revoolut": {"Colours": "#abc16d,#73862d".split(","), "Angle": 90},
    "Halandrite": {"Colours": "#6bfff5,#85ff85".split(","), "Angle": 90},
    "Zestrium": {"Colours": "#533f75,#3f3ba2".split(","), "Angle": 90},
    "Limitrite": {"Colours": "#00ff00,#000c01,#00ff00".split(","), "Angle": 90},
    "Aztekium": {"Colours": "#b2b553,#ede236".split(","), "Angle": 180},
    "Swordium": {"Colours": "#f26b56,#ff4c45".split(","), "Angle": 180},
    "Shieldium": {"Colours": "#44a2fa,#4164fb".split(","), "Angle": 180},
    "Spanchium": {"Colours": "#905b38,#44c15d".split(","), "Angle": 90},
    "Spearite": {"Colours": "#ca9e49,#ca9e49,#ca9e49,#ca9e49,#ca9e49,#ca9e49,#ca9e49,#ca9e49,#303030,#f3b232,#f3b232,#f3b232,#f3b232,#f3b232,#f3b232,#f3b232,#f3b232,#f3b232".split(","), "Angle": 180},
    "Vasolonio": {"Colours": "#4b3964,#745347".split(","), "Angle": 180},
    "Megabursite": {"Colours": "#51e255,#c96332,#51e255".split(","), "Angle": 90, "S_Colour": "#000000", "S_Width": 0},
    "Tematonium": {"Colours": "#6fc3bf,#6fc3bf,#53c54b,#53c54b,#6fc3bf,#6fc3bf".split(","), "Angle": 90},
    "Divinorum": {"Colours": "#75e9fd,#8ce3f3".split(","), "Angle": 180, "S_Colour": "#57a2d6", "S_Width": 1},
    "Limestone": {"Colours": "#999999,#dedede".split(","), "Angle": 90},
    "Amber": {"Colours": "#ffd71d,#ffb931".split(","), "Angle": 180},
    "Lustrous Amethyst": {"Colours": "#9042ff,#6749ff".split(","), "Angle": 90},
    "Molten Iron": {"Colours": "#ffb482,#f6d59f".split(","), "Angle": 90},
    "Fools Gold": {"Colours": "#f2eb50,#dbce35".split(","), "Angle": 90},
    "Exotic Quartz": {"Colours": "#ade4ff,#e0b3ff".split(","), "Angle": 90},
    "Grossular Jade": {"Colours": "#47a466,#80e47c".split(","), "Angle": 90},
    "Purple Obsidian": {"Colours": "#b359d1,#4b3454".split(","), "Angle": 90},
    "Black Diamond": {"Colours": "#346363,#60cbd0".split(","), "Angle": 90},
    "Enlightened Starlight": {"Colours": "#ff9f7c,#ffe45a".split(","), "Angle": 90},
    "Supercharged Ion": {"Colours": "#ecfb7b,#b2fe8f".split(","), "Angle": 90},
    "Chromatic Bismuth": {"Colours": "#d593bb,#8381fb,#d4d4bd".split(","), "Angle": 90},
    "Sparkling Nissonite": {"Colours": "#a5ffdb,#e8ffad".split(","), "Angle": 90},
    "Pure Orpiment": {"Colours": "#894444,#9a8484".split(","), "Angle": 90},
    "Indestructible Tetra": {"Colours": "#28bce9,#274e9a".split(","), "Angle": 90},
    "Hypercharged Volt": {"Colours": "#9a9749,#0d0d09,#a6a22c".split(","), "Angle": 90},
    "Galaxium": {"Colours": "#744fff,#807fff".split(","), "Angle": 90},
    "Mythralite": {"Colours": "#5a99ff, #4f85ff".split(","), "Angle": 90},
    "Phantasmite": {"Colours": "#72ff77,#4eff5a".split(","), "Angle": 90},
    "Eclipsium": {"Colours": "#ac6b21,#54340f".split(","), "Angle": 90},
    "Aetherite": {"Colours": "#dfdeaf,#c9c1d9".split(","), "Angle": 90},
    "Aurorite": {"Colours": "#31f9c0,#5ef8df".split(","), "Angle": 90},
    "Crysalith": {"Colours": "#b5ff92,#393939".split(","), "Angle": 90},
    "Vortexium": {"Colours": "#9d7ed7,#8867af".split(","), "Angle": 90},
    "Ignisium": {"Colours": "#ff5328,#ff3a1b".split(","), "Angle": 90},
    "Luminaris": {"Colours": "#ffc0d8,#ffdcb9".split(","), "Angle": 90, "S_Colour": "#000000", "S_Width": 0},
    "Chronicality": {"Colours": "#979797,#656565".split(","), "Angle": 90},
    "Amalgamation": {"Colours": "#c9f9af,#c9f9af,#c9f9af,#ce53ff,#fd8690,#fd8690,#fd8690".split(","), "Angle": 90},
    "Purity": {"Colours": "#a1ffa7,#a0ffa9".split(","), "Angle": 90},
    "Totality": {"Colours": "#494B3F,#EFF799".split(","), "Angle": 180},
    "Metal": {"Colours": "#a8a8a8,#c4c4c4".split(","), "Angle": 90},
    "Press": {"Colours": "#0f0f0f,#ff0000,#0f0f0f".split(","), "Angle": 90},
    "Microparticles": {"Colours": "#000000,#000000,#ffffff,#000000,#000000,#000000,#000000,#000000,#ffffff,#000000,#000000".split(","), "Angle": 90},
    "Star": {"Colours": "#55aa7f,#ffff14,#ff9f6e".split(","), "Angle": 135},
    "Robot": {"Colours": "#434343,#292929".split(","), "Angle": 135},
    "Prototype": {"Colours": "#838389,#5e5f6b".split(","), "Angle": 90},
    "Hardstone": {"Colours": "#2e2e2e,#222222,#838383,#838383".split(","), "Angle": 90},
    "Boomite": {"Colours": "#e7b005,#ff0000,#e7b005".split(","), "Angle": 90},
    "Plutonium": {"Colours": "#b9b9b9,#838383".split(","), "Angle": 90},
    "Cisophrase": {"Colours": "#d0a4c4,#cfd073".split(","), "Angle": 90},
    "Anatase": {"Colours": "#91976b,#d0db99,#868a66".split(","), "Angle": 90},
    "Oligoclase": {"Colours": "#a09b6f,#c0be84,#928f65".split(","), "Angle": 90},
    "Coral": {"Colours": "#dcc9aa,#9affa0,#d7ffa5".split(","), "Angle": 90},
    "Shardrite": {"Colours": "#c2c2c2,#ffffff,#adadad".split(","), "Angle": 90},
    "Serpentine": {"Colours": "#ecb438,#f8ce05,#e656fb,#ec42c2".split(","), "Angle": 90},
    "Tsavorite": {"Colours": "#39f300,#299000".split(","), "Angle": 90},
    "Tangeite": {"Colours": "#65c653,#58af4f,#92d766".split(","), "Angle": 90},
    "Labradorite": {"Colours": "#c6e5ba,#7190fd,#de9fa5".split(","), "Angle": 90},
    "Tetrahedrite": {"Colours": "#5d5d5d,#ffffff,#5d5d5d".split(","), "Angle": 90},
    "Dreamstone": {"Colours": "#b0a3ff,#9fd8e7".split(","), "Angle": 90},
    "Rhodium": {"Colours": "#d8d8d8,#ffffff,#d8d8d8".split(","), "Angle": 90},
    "Paragonite": {"Colours": "#9d947b,#bdbdbb,#9d947b".split(","), "Angle": 90},
    "Lautite": {"Colours": "#8ba787,#8ba787".split(","), "Angle": 90},
    "Tungsten": {"Colours": "#e2e1cd,#fbfadd,#e2e1cd".split(","), "Angle": 90},
    "Iranite": {"Colours": "#ff084e,#ff9a63".split(","), "Angle": 90},
    "Grandidierite": {"Colours": "#a1fdd4,#85ffc6".split(","), "Angle": 90},
    "Qernz": {"Colours": "#ffffff,#267d0c,#ffffff".split(","), "Angle": 90},
    "Benitoite": {"Colours": "#250047,#120024,#250047".split(","), "Angle": 90},
    "Plesside": {"Colours": "#ffa49c,#ff95ad,#eda7a2".split(","), "Angle": 90},
    "Zykaite": {"Colours": "#d9d694,#c5bf7a,#d9d694".split(","), "Angle": 90},
    "Abelsonite": {"Colours": "#ff2200,#ff3d00,#ff2200".split(","), "Angle": 90},
    "Devilline": {"Colours": "#328d75,#328d75".split(","), "Angle": 90},
    "Lazulite": {"Colours": "#52cceb,#50e5ff,#52cceb".split(","), "Angle": 90},
    "Pentagonite": {"Colours": "#4797fd,#378ab0,#4797fd".split(","), "Angle": 90},
    "Pigeonite": {"Colours": "#c78341,#faa54f,#c78341".split(","), "Angle": 90},
    "Vanuralite": {"Colours": "#ffef34,#fff56b,#ffef34".split(","), "Angle": 90},
    "Xanthoconite": {"Colours": "#b38820,#e9a338".split(","), "Angle": 90},
    "Uytenbogaardtite": {"Colours": "#6c7f67,#6c7463,#4b5446".split(","), "Angle": 90},
    "Taranakite": {"Colours": "#fbc3da,#edeea7,#fbc3da".split(","), "Angle": 90},
    "Quetzalcoatlite": {"Colours": "#47d9ab,#79fc8a,#47d9ab".split(","), "Angle": 90},
    "Playfairite": {"Colours": "#2c2c35,#1e1611,#2c2c35".split(","), "Angle": 90},
    "Hologram": {"Colours": "#9be8ff,#ffffff,#9be8ff".split(","), "Angle": 90},
    "X": {"Colours": "#ff5454,#ff5454".split(","), "Angle": 90},
    "Y": {"Colours": "#8dff6e,#8dff6e".split(","), "Angle": 90},
    "Z": {"Colours": "#7577ff,#7577ff".split(","), "Angle": 90},
    "Vectorlord": {"Colours": "#ff5454,#8dff6e,#7577ff".split(","), "Angle": 90},
    "Unholy Copper": {"Colours": "#6f3c00,#834200,#873500".split(","), "Angle": 90},
    "Wrath Amethyst": {"Colours": "#8a44c5,#7e60ff,#955aff".split(","), "Angle": 90},
    "Dark Gold": {"Colours": "#524300,#3e3400,#595000".split(","), "Angle": 90},
    "Tempered Quartz": {"Colours": "#d2ffc4,#a4ff94,#d2ffc4".split(","), "Angle": 90},
    "Volcanic Molybdenum": {"Colours": "#e9e7e7,#4c3c3c".split(","), "Angle": 90},
    "Deadly Obsidian": {"Colours": "#000000,#04003d,#000000".split(","), "Angle": 90},
    "Doomdilite": {"Colours": "#9d4700,#fd7200,#9d4700".split(","), "Angle": 90},
    "Rave Ectoplasm": {"Colours": "#07ecff,#ca10fd,#07ecff".split(","), "Angle": 90},
    "Cloom": {"Colours": "#1e063a,#9bee6f,#1e063a".split(","), "Angle": 90},
    "Pentagram": {"Colours": "#292843,#7d6ef4,#292843".split(","), "Angle": 90},
    "Nevercyan": {"Colours": "#09b8ac,#7ce6e0".split(","), "Angle": 90},
    "Core of Insurgence": {"Colours": "#000000,#000000,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#34e274,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#626262,#000000,#000000".split(","), "Angle": 145},
    "Starfury": {"Colours": "#e08d4f,#c570af".split(","), "Angle": 90},
    "Golden Glory": {"Colours": "#ffff60,#ffff1f".split(","), "Angle": 90},
    "Skylest": {"Colours": "#018af9,#0071ff".split(","), "Angle": 90},
    "Golest": {"Colours": "#ffaa54,#ffaa2b".split(","), "Angle": 90},
    "Prismo": {"Colours": "#136a5d,#008370,#136a5d".split(","), "Angle": 90},
    "Aragon": {"Colours": "#8cff7f,#c8ff7f".split(","), "Angle": 90},
    "Ephos": {"Colours": "#aa0200,#a75201".split(","), "Angle": 90},
    "Illudic": {"Colours": "#0044cb,#0000ff,#ffffff,#ff0000,#cf0000".split(","), "Angle": 90},
    "Magmit": {"Colours": "#502000,#4b1500".split(","), "Angle": 90},
    "Phelix": {"Colours": "#ff9aff,#ffffff,#98ccff".split(","), "Angle": 180},
    "Sepron": {"Colours": "#661f0c,#c44c00".split(","), "Angle": 90},
    "Ancar": {"Colours": "#354242,#01fcfc".split(","), "Angle": 90},
    "Taryl": {"Colours": "#65cbff,#05acff,#65cbff".split(","), "Angle": 90},
    "Goldermine": {"Colours": "#6c6c00,#000000,#6c6c00".split(","), "Angle": 90},
    "Prismarine": {"Colours": "#b5ffea,#ffffff,#b5ffea".split(","), "Angle": 90},
    "Intergalaxias": {"Colours": "#930093,#000000,#0000a5".split(","), "Angle": 90},
    "Eruptis": {"Colours": "#b23001,#5c0400,#5500af".split(","), "Angle": 90},
    "Dime": {"Colours": "#fe0070,#ff001b".split(","), "Angle": 90},
    "Calamity": {"Colours": "#900013,#200067".split(","), "Angle": 90},
    "Elysium": {"Colours": "#6cfefe,#ffffff,#6cfefe".split(","), "Angle": 90},
    "Equinox": {"Colours": "#000000,#ffffff,#000000".split(","), "Angle": 90},
    "Oculous": {"Colours": "#000000,#00f3f3,#000000".split(","), "Angle": 90},
    "Catalyst": {"Colours": "#d50808,#322626,#d50808".split(","), "Angle": 90},
    "Loyalty": {"Colours": "#000000,#f25100,#fc0d01,#f25100,#000000".split(","), "Angle": 90},
    "Omni": {"Colours": "#000000,#ffffff,#000000,#ffffff,#000000,#ffffff,#000000".split(","), "Angle": 90},
    "Excalibur": {"Colours": "#2d2b2a,#4a1e01".split(","), "Angle": 90},
    "Volùspa": {"Colours": "#ffffff,#000000,#ffffff".split(","), "Angle": 90},
    "Dynamo": {"Colours": "#0c04f3,#ea4f13".split(","), "Angle": 90},
    "Genesis": {"Colours": "#6bde21,#d43ec0".split(","), "Angle": 90},
    "Solomnium": {"Colours": "#fec044,#ffffff,#f9f952".split(","), "Angle": 90},
    "Immortality": {"Colours": "#8344ff,#ffffff,#8344ff".split(","), "Angle": 90},
    "Temperùs": {"Colours": "#000000,#eaea00,#000000".split(","), "Angle": 90},
    "Relictic Loyalty": {"Colours": "#ff2d00,#fff100,#ff2d00".split(","), "Angle": 90},
    "Relictic Volùspa": {"Colours": "#ffffff,#ce0000,#000000,#ce0000,#ffffff".split(","), "Angle": 90},
    "Lifender": {"Colours": "#ffffff,#beeae2".split(","), "Angle": 90},
    "Stone 2": {"Colours": "#999999,#383838,#686868,#222222".split(","), "Angle": 45},
    "Loocasium": {"Colours": "#a0a0a0,#a0a0a0".split(","), "Angle": 0},
    "Stone 3": {"Colours": "#000000,#999999,#383838,#999999,#686868,#222222,#000000".split(","), "Angle": 22.5},
    "Skilltriix": {"Colours": "#000000,#000000".split(","), "Angle": 0},
    "Hyka Gem": {"Colours": "#c7ff2b,#c7ff2b".split(","), "Angle": 0},
    "Mana": {"Colours": "#3c59f4,#2e67e6".split(","), "Angle": 0},
    "Enchantment": {"Colours": "#cc52c9,#af3dc2".split(","), "Angle": 90},
    "Spell": {"Colours": "#75acbc,#8abea2".split(","), "Angle": 180},
    "Eternabasite": {"Colours": ["#ffffff", "#111111" ,"#ffffff"], "Angle": 25, "S_Colour": "#ffffff", "S_Width": 1},
    "DENIAL": {"Colours": "#ff0000, #40020c, #f53958".split(", "), "Angle": 31.4159, "S_Colour": "#ff0000", "S_Width": 2},
    "Esadrhium": {"Colours": ["#1affd2", "1affd2"], "Angle": 0},
    "Tesseract": {"Colours": "#0077ff,#180848,#1423d1,#385dcd".split(","), "Angle": 44, "S_Colour": "#0000ff", "S_Width": 1},
    "Sloth": {"Colours": ["#23aaff", "#23aaff"], "Angle": 0},
    "Eveslogite": {"Colours": "#98f07b,#98f07b".split(","), "Angle": 90},
    "Spacelite": {"Colours": "#202343,#2d5485,#202343".split(","), "Angle": 90},
    "Astrolite": {"Colours": "#3867da,#6419d6,#9e46d5".split(","), "Angle": 0},
    "Cometium": {"Colours": "#a6efff,#a6efff,#a6efff,#a6efff,#39497c,#a6efff,#a6efff,#a6efff,#a6efff".split(","), "Angle": 125},
    "Planetium": {"Colours": "#3c664e,#3c664e,#3c664e,#3fa68c,#3fa68c,#3fa68c,#3fa68c,#696a4b,#696a4b,#696a4b".split(","), "Angle": 120},
    "Mercury": {"Colours": "#c2cedb,#c1cfd9".split(","), "Angle": 90},
    "Saturnite": {"Colours": "#81d6f7,#2a346e".split(","), "Angle": 90},
    "Constellar": {"Colours": "#b66ddf,#a48afb".split(","), "Angle": 0},
    "Neutronium": {"Colours": "#c7fbff,#c7fbff".split(","), "Angle": 0},
    "Magnetar": {"Colours": "#7c99af,#7c99af,#637ff1,#637ff1,#7c99af,#7c99af".split(","), "Angle": 90},
    "Uzoburnus": {"Colours": "#3e613d,#3c4b64,#7a5a3e".split(","), "Angle": 90},
    "Bit": {"Colours": "#5d7d8c,#6999b8".split(","), "Angle": 90},
    "Pixel": {"Colours": "#8ad3cf,#b5cce9".split(","), "Angle": 90},
    "Aluminium": {"Colours": "#80aabf,#80aabf".split(","), "Angle": 90},
    "Nickel": {"Colours": "#4c5054,#595b62".split(","), "Angle": 90},
    "Zinc": {"Colours": "#a3c4e3,#a3c4e3".split(","), "Angle": 0},
    "Electrolite": {"Colours": "#48d1ff,#52b3f6".split(","), "Angle": 0},
    "Livermorium": {"Colours": "#343058,#453a80".split(","), "Angle": 0},
    "Gygabittium": {"Colours": "#ab696f,#7668bb".split(","), "Angle": 90},
    "Pteracorite": {"Colours": "#84bfe3,#5577aa".split(","), "Angle": 90},
    "Oganesson": {"Colours": "#233d9a,#1c616f".split(","), "Angle": 90},
    "Apatite": {"Colours": "#8a9bf6,#afbffc,#8a9bf6".split(","), "Angle": 90},
    "Unbinilium": {"Colours": "#9ebeeb,#8096b0".split(","), "Angle": 0},
    "Watercrystal": {"Colours": "#27304d,#5560ca".split(","), "Angle": 90},
    "Sandstone": {"Colours": "#8a7f4d,#675b34".split(","), "Angle": 90},
    "Firecrystal": {"Colours": "#672a2c,#c6342b".split(","), "Angle": 90},
    "Leafstone": {"Colours": "#5d8442,#3f5c35".split(","), "Angle": 90},
    "Windirius": {"Colours": "#9cdad6,#9ad2c7".split(","), "Angle": 0},
    "Rockarnium": {"Colours": "#302b3f,#3c284c".split(","), "Angle": 180, "S_Width": 1, "S_Colour": "#202020"},
    "Drakan": {"Colours": "#3c15a0,#4e1b9a".split(","), "Angle": 180},
    "Chromatite": {"Colours": "#d5af5b,#80db87,#79a3f3".split(","), "Angle": 90},
    "Sognus": {"Colours": "#b94fc3,#b94fc3".split(","), "Angle": 0},
    "Ambrosia": {"Colours": "#ffd38c,#ffd38c".split(","), "Angle": 0},
    "Quintessence": {"Colours": "#f177eb,#f177eb".split(","), "Angle": 0},
    "Silicon": {"Colours": "#deddb3,#dccfbc".split(","), "Angle": 90},
    "Sulfur": {"Colours": "#8d8d43,#62602e".split(","), "Angle": 180},
    "Chlorine": {"Colours": "#caa1e6,#8a83e2".split(","), "Angle": 90},
    "Bromine": {"Colours": "#3e2d20,#3e2d20".split(","), "Angle": 0},
    "Technetium": {"Colours": "#225622,#42c150".split(","), "Angle": 180},
    "Scandium": {"Colours": "#231612,#231612".split(","), "Angle": 0},
    "Rhodimite": {"Colours": "#bbf7ff,#d1e8ff".split(","), "Angle": 180},
    "Vanadium": {"Colours": "#8e3229,#d44634,#8e3229".split(","), "Angle": 90},
    "Selenium": {"Colours": "#554576,#3b3762".split(","), "Angle": 180},
    "Yttrium": {"Colours": "#cbf029,#d5ff2a".split(","), "Angle": 90},
    "Polonium": {"Colours": "#66423a,#2f2f2f,#66423a".split(","), "Angle": 90},
    "Krypton": {"Colours": "#181628,#221c30".split(","), "Angle": 180},
    "Aeglestone": {"Colours": "#4a386c,#312a50".split(","), "Angle": 180},
    "Arctite": {"Colours": "#b570de,#586ed3".split(","), "Angle": 90},
    "Cuprite": {"Colours": "#311a16,#571c17".split(","), "Angle": 180},
    "Musgravite": {"Colours": "#b3c3c6,#d5e6f9".split(","), "Angle": 90},
    "Kainosite": {"Colours": "#e0df8b,#8d9b4f".split(","), "Angle": 180},
    "Neodymium": {"Colours": "#bd832d,#d8da16".split(","), "Angle": 90},
    "Beryllium": {"Colours": "#96c9ce,#b6a1eb".split(","), "Angle": 90},
    "Vergamite": {"Colours": "#573b2b,#462212".split(","), "Angle": 90},
    "Quamite": {"Colours": "#b6dec4,#d0d8ee".split(","), "Angle": 180},
    "Astralyte": {"Colours": "#2a3054,#131967".split(","), "Angle": 180, "S_Width": 1, "S_Colour": "#222437"},
    "Unobtainium": {"Colours": "#e56aff,#b34adf".split(","), "Angle": 90},
    "Vibranium": {"Colours": "#ffffff,#ffffff".split(","), "Angle": 90},
    "Stygium": {"Colours": "#fffa9d,#f8d47f".split(","), "Angle": 90},
    "Kyber Crystal": {"Colours": "#608ff0,#534eda".split(","), "Angle": 90, "S_Width": 1, "S_Colour": "#0000ff"},
    "Rune": {"Colours": "#ffffff,#6f6f6f".split(","), "Angle": 135},
    "Ultrabirth": {"Colours": "#ffffff,#546eff".split(","), "Angle": 145},
    "Cosmic Crystal": {"Colours": "#c398ff,#ffffff,#ffaaff".split(","), "Angle": 135},
    "Abstract Bar": {"Colours": "#ffaa00,#ffffff,#ff6c6c".split(","), "Angle": 135},
    "Chlorophyte": {"Colours": "#005500,#ffffff,#55fe00".split(","), "Angle": 135},
    "Chlorophyte Bar": {"Colours": "#13fb03,#aeff00,#55fe00".split(","), "Angle": 135},
    "Shroomite Bar": {"Colours": "#34a0ff,#b7d8ff,#8bbaff".split(","), "Angle": 135},
    "Sigil of The Unknown": {"Colours": "#000000,#000000,#ffffff,#000000,#000000".split(","), "Angle": 165},
    "King Crystal": {"Colours": "#cf25fc,#03c1fd,#83f335".split(","), "Angle": 135},
    "Anomaly": {"Colours": "#7700ff,#a601f9,#070257,#b700ff".split(","), "Angle": 135},
    "Rainbatar": {"Colours": "#f2ff00,#09ff00,#00ffe5".split(","), "Angle": 90},
    "Prototype_Millennial": {"Colours": "#42798e,#59ccef".split(","), "Angle": 180},
    "Primordial Delight": {"Colours": "#59f473,#ffa527".split(","), "Angle": 90},
    "Xylorian": {"Colours": "#3a2084,#381fed".split(","), "Angle": 180},
    "Aether": {"Colours": "#acf8ff,#77eafb".split(","), "Angle": 180},
    "Blackholium": {"Colours": "#000000,#000000,#000000,#000000,#d55920,#000000,#000000,#000000,#000000".split(","), "Angle": 135},
    "Chocolate": {"Colours": "#9c4d00,#713900".split(","), "Angle": 180},
    "Moonstone": {"Colours": "#f8ffff,#e4fcff".split(","), "Angle": 180},
    "Blue Crystal": {"Colours": "#0055ff,#0000ff".split(","), "Angle": 90, "S_Width": 0.3, "S_Colour": "#16168e"},
    "???": {"Colours": "#feccd3,#fbceeb".split(","), "Angle": 90},
    "Afkime": {"Colours": "#ffffff,#ce8bf7,#ffcb62".split(","), "Angle": 80},
    "Oortodium": {"Colours": "#55aa7f,#00ff00".split(","), "Angle": 90},
    "Possessed Quartz": {"Colours": "#267463,#75a1aa".split(","), "Angle": 135},
    "Brookite": {"Colours": "#984e04,#ec1300".split(","), "Angle": 90},
    "Christite": {"Colours": "#aa0000,#ed4747".split(","), "Angle": 90},
    "Voiridis": {"Colours": "#310492,#4cbc27".split(","), "Angle": 90},
    "12.99": {"Colours": "#6b1313,#1d1111".split(","), "Angle": 90},
    "Eternium": {"Colours": "#d6b1d9,#efc1b2".split(","), "Angle": 90},
    "Fisheode": {"Colours": "#699eb5,#595280".split(","), "Angle": 90},
    "Zentlyo": {"Colours": "#a16b2c,#ffc15d".split(","), "Angle": 90},
    "Noirment": {"Colours": "#16003d,#000f1a".split(","), "Angle": 90},
    "Nelhim": {"Colours": "#dd7bfc,#7386fd".split(","), "Angle": 90},
    "Banana": {"Colours": "#fff570,#ffb40e".split(","), "Angle": 90},
    "Alamost": {"Colours": "#0000ff,#00ffff,#0000ff".split(","), "Angle": 90},
    "Antimony": {"Colours": "#beffff,#edffff".split(","), "Angle": 180, "S_Colour": "#82eded", "S_Width": 1},
    "ARG": {"Colours": "#3e9520,#33612f,#3f981f".split(","), "Angle": 90},
    "Binarium": {"Colours": "#096a0c,#032704".split(","), "Angle": 90},
    "Biotite": {"Colours": "#866700,#209a00".split(","), "Angle": 180},
    "Celestial": {"Colours": "#c4ffff,#9bffff".split(","), "Angle": 90},
    "Chroma": {"Colours": "#ff0000,#ff0000,#ff9901,#f3ff00,#00ff22,#00f4ff,#010bff".split(","), "Angle": 90},
    "Chromatone": {"Colours": "#000000,#ff0000,#00ff00,#0000ff,#000000".split(","), "Angle": 90},
    "Confusion": {"Colours": "#8b5ac6,#bd5593".split(","), "Angle": 90},
    "Cytoplasm": {"Colours": "#62ff74,#ffd52a".split(","), "Angle": 90},
    "Desire": {"Colours": "#cb21ff,#cb21ff".split(","), "Angle": 90},
    "Ectoplasm": {"Colours": "#5ac6c6,#549f9f,#6cbcbc".split(","), "Angle": 90},
    "Envy": {"Colours": "#55dc4b,#55dc4b".split(","), "Angle": 90},
    "Exodal": {"Colours": "#000000,#027d02,#000000".split(","), "Angle": 90},
    "Frosterial": {"Colours": "#141e31,#1988ff".split(","), "Angle": 90},
    "Gluttony": {"Colours": "#c88c2c,#dd774b".split(","), "Angle": 90},
    "Grass": {"Colours": "#21da3e,#43f966".split(","), "Angle": 90},
    "Greed": {"Colours": "#ffde4e,#ffd039".split(","), "Angle": 90},
    "Hardystonite": {"Colours": "#610505,#000000,#000055".split(","), "Angle": 90},
    "Heavenlium": {"Colours": "#ffff00,#00ffff,#ffff00".split(","), "Angle": 90},
    "Iridium": {"Colours": "#e6f2ff,#add5ff".split(","), "Angle": 180, "S_Colour": "#cccce3", "S_Width": 1},
    "Kanoite": {"Colours": "#3f0202,#231919".split(","), "Angle": 180},
    "Lightmatter": {"Colours": "#ffffff,#ffffff".split(","), "Angle": 0},
    "Magnetite": {"Colours": "#222222,#020202".split(","), "Angle": 90},
    "Malware": {"Colours": "#9e1313,#480202,#a30c0c".split(","), "Angle": 90},
    "Megabasite": {"Colours": "#ffffff,#000000,#ffffff".split(","), "Angle": 90},
    "Meridianiite": {"Colours": "#000000,#000000,#ffffff,#000000,#ffffff,#ffffff".split(","), "Angle": 170},
    "Pigmentite": {"Colours": "#ff0000,#0000ff,#ffff00".split(","), "Angle": 90},
    "Painite": {"Colours": "#6a0000,#ff0000".split(","), "Angle": 135},
    "Paputal": {"Colours": "#000000,#a600fa,#000000,#a400f6,#000000".split(","), "Angle": 90},
    "Petrol": {"Colours": "#536467,#226771".split(","), "Angle": 180},
    "Phantoplasm": {"Colours": "#0085ff,#00ceff".split(","), "Angle": 90},
    "Polybasite": {"Colours": "#b7b7b7,#727272".split(","), "Angle": 180},
    "Pride": {"Colours": "#aa80ff,#aa80ff".split(","), "Angle": 90},
    "Primate": {"Colours": "#fff443,#fdfe70".split(","), "Angle": 90},
    "Pyroxene": {"Colours": "#f40000,#fda800".split(","), "Angle": 170},
    "Radiant": {"Colours": "#ffffff,#f6f683".split(","), "Angle": 90},
    "Red Quartz": {"Colours": "#ed0000,#ba0000".split(","), "Angle": 180},
    "Toxant": {"Colours": "#55ff00,#0c23d1".split(","), "Angle": 90},
    "TRU3_W0RLD": {"Colours": "#31732e,#010201,#336c3e".split(","), "Angle": 90},
    "Witherite": {"Colours": "#edffff,#baffff".split(","), "Angle": 90},
    "Wrath": {"Colours": "#aa0032,#aa0032".split(","), "Angle": 90},
    "Xenotime": {"Colours": "#ff0000,#0000ff".split(","), "Angle": 90},
    "Inception": {"Colours": "#8c8c8c,#8c8c8c,#fefefe,#4f4f4f,#4f4f4f".split(","), "Angle": 170},
    "==INFINITY==": {"Colours": ["#ffffff", "#888888", "#888888", "#000000"], "Angle": 135},
    "ant": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "unlucky stone": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "silly stat": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "mendozite": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "kinda lucky stone": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "womendozite": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "lucky stone": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "silly stat 2": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "silly stat 4": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "toiletum": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "upvotium": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "colourscriptsample": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "spectrafractum": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "very lucky stone": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "silly stat 5": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "hitbox": {"Colours": "#595959,#595959".split(","), "Angle": 90},
    "sotne": {"Colours": "#4f4f4f,#4f4f4f".split(","), "Angle": 90},
    "almost 💔": {"Colours": "#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#329cdc,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000,#000000".split(","), "Angle": 90},
    "silly stat 3": {"Colours": "#000000,#121212,#000000".split(","), "Angle": 90},
    "eulogy to the dead god": {"Colours": "#75ff75,#75ffff,#7575ff,#ff75ff,#ff7575".split(","), "Angle": 90},
    "legacy eyselite": {"Colours": "#72d8e4,#72d8e4,#72d8e4,#72d8e4,#72d8e4,#72d8e4,#72d8e4,#e86b7c,#72d8e4".split(","), "Angle": 90},
    "mayb3_w0rld": {"Colours": "#c9a300,#000000,#c5a000".split(","), "Angle": 90},
    "synthase": {"Colours": "#ffa01b,#f33f17".split(","), "Angle": 0},
    "flawless grandidierite": {"Colours":"#fce35b,#d26b7f".split(","), "Angle": 0},
    "silly stat 6": {"Colours": "#000000,#121212 #000000".split(","), "Angle": 90},
    "phosphoribosylaminoimidazolesuccinocarboxamide": {"Colours": "#ffa01b,#f33f17".split(","), "Angle": 0},
    "gullibilius": {"Colours": "#204a1f, #204a1f, #d3ac15, #ff0000, #d3ac15, #00ffff, #0800ff, #00ffff, #d3ac15, #ff0000, #d3ac15, #204a1f, #204a1f".split(", "), "Angle": 90},
    "Ascended Crystal": {"Colours": "#4210ff,#4210ff,#6130ff,#6130ff,#cc6bff,#7c46ff".split(","), "Angle": 90},
    "Bright Quartz": {"Colours": "#a7fff9,#ffffad".split(","), "Angle": 90},
    "Glowing Jade": {"Colours": "#59894e,#719e67,#27db12,#27db12".split(","), "Angle": 90},
    "Vivid Ruby": {"Colours": "#e2e92c,#f59716".split(","), "Angle": 0},
    "Glossy Diamond": {"Colours": "#62fff1,#7a2dff".split(","), "Angle": 90},
    "Polarized Ion": {"Colours": "#cdbc3e,#908734".split(","), "Angle": 90},
    "Illuminated Bismuth": {"Colours": "#94ff92,#ffa2cf".split(","), "Angle": 90},
    "Gleaming Nissonite": {"Colours": "#aadfff,#77c3ff".split(","), "Angle": 90},
    "Glaring Tetra": {"Colours": "#8c8eff,#83acfe".split(","), "Angle": 90},
    "Shining Lollipop": {"Colours": "#ffa79c,#ffab8c".split(","), "Angle": 90},
    "Glistening Gyge": {"Colours": "#7b554a,#8c6a60,#ce7970".split(","), "Angle": 90},
    "Scapolite": {"Colours": "#ff983b,#ffba50".split(","), "Angle": 90},
    "Phenakite": {"Colours": "#565656,#ffffff".split(","), "Angle": 90},
    "Unarovite": {"Colours": "#33ffa8,#4bff7f".split(","), "Angle": 90},
    "Sphalerite": {"Colours": "#470e0e,#1a0505".split(","), "Angle": 90},
    "Rhodochrosite": {"Colours": "#ff7878,#ff7878,#ff7878,#ff2121,#ff2121".split(","), "Angle": 90},
    "Tourmaline": {"Colours": "#ed7ae2,#d891f5".split(","), "Angle": 90},
    "Cosmillite": {"Colours": "#9955ff,#c929ff".split(","), "Angle": 90},
    "Vibranium": {"Colours": "#4c3fab,#342f46,#5805a3".split(","), "Angle": 90, "S_Width": 1, "S_Colour": "#24185f"},
    "Metactinium": {"Colours": "#6997b4,#77d6dc,#6ba7bd".split(","), "Angle": 0, "S_Width": 1, "S_Colour": "#374c5d"},
    "Obscenium": {"Colours": "#93436c,#d17342".split(","), "Angle": 90},
    "Timeless Quartz": {"Colours": "#ffe390,#dbdbdb,#ffe390".split(","), "Angle": 9},
    "Fallen": {"Colours": "#b77e2d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#b77e2d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#b77e2d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#b77e2d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#b77e2d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#392b1d,#b77e2d".split(","), "Angle": 9},
    "Moon Cash": {"Colours": "#a9a9a9,#97b58b".split(","), "Angle": 90},
    "Booster": {"Colours": "#ff897f,#fd557e".split(","), "Angle": 90},
    "Reincarnation": {"Colours": "#00557f,#1e359f".split(","), "Angle": 90},
    "Scoria": {"Colours": "#ff0000,#ff0000,#584c4c,#584c4c".split(","), "Angle": 135},
    "Brighterium": {"Colours": "#ffff7f,#ffff7f,#ffff00,#00ffff,#00ffff".split(","), "Angle": 135},
    "Baryte": {"Colours": "#01b7f2,#01edf5".split(","), "Angle": 180},
    "Gypsum": {"Colours": "#8d8d8b,#aeaba4,#6f6c67".split(","), "Angle": 180},
    "Pyrite": {"Colours": "#524d38,#cdcc32".split(","), "Angle": 180},
    "Cryon": {"Colours": "#aaffff,#d7ffff".split(","), "Angle": 90},
    "Kinetic": {"Colours": "#752fd0,#dac837".split(","), "Angle": 180},
    "Plasma": {"Colours": "#ff00ff,#ff00ff,#7707ff,#ffaaff".split(","), "Angle": 135},
    "Solargems": {"Colours": "#f8da51,#f7c632".split(","), "Angle": 180},
    "Fanite": {"Colours": "#7a797b,#99989a".split(","), "Angle": 180},
    "Showerite": {"Colours": "#2992bd,#85612e".split(","), "Angle": 180},
    "Hexadron": {"Colours": "#717171,#d4d4d4".split(","), "Angle": 180},
    "Glitchared": {"Colours": "#7d9088,#7b82ad,#9d4ab8,#5ed7ca,#c32542,#d23035,#6a57d3,#4e8fbc".split(","), "Angle": 180},
    "Yalkènzar": {"Colours": "#ffff40,#ffff40,#ffff40,#ffff40,#ffff40,#ff22ff,#ff22ff,#ff22ff,#ff22ff,#ff22ff".split(","), "Angle": 180},
    "Imperium": {"Colours": "#eddc1f,#fbb766".split(","), "Angle": 180},
    "Electron": {"Colours": "#063147,#000305,#00a9fe,#0078b3".split(","), "Angle": 90},
    "Byte": {"Colours": "#0b8101,#0b8101,#000000,#0b8101,#0b8101".split(","), "Angle": 18},
    "Binary": {"Colours": "#0c7500,#000000,#0c7500,#000000,#0c7500,#000000,#0c7500,#000000".split(","), "Angle": 70},
    "Script": {"Colours": "#ffffff,#ff8800,#ff8800,#804d00,#d09f2c,#804d00,#ff8800,#ff8800,#ffffff".split(","), "Angle": 9},
    "Language": {"Colours": "#cccc00,#cccc00,#000000,#0000cc,#0000cc".split(","), "Angle": 109},
    "RAM": {"Colours": "#5e5e5e,#555555,#9d9d9d".split(","), "Angle": 75},
    "Default": {"Colours": ["#ffffff", "#ffffff"], "Angle": 0},
}
cythrex_data = {
    "Cash": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "The most basic currency to exist, provided to you by AIHA Corp.",
        "obtainment": "Always obtainable, never runs out"
    },
    "Multiplier": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A technology created by AIHA Corp. It generates Cash at a faster speed.",
        "obtainment": '''First found in the Spawn realm. Also can be obtained by:
- Stone Geode at a 1/2 chance
- Buttons found in: C, CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Rebirths": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Further technology created AIHA Corp. Requires the recreation of the body, in turn more funds are given by AIHA Corp.",
        "obtainment": '''First found in the Spawn realm. Also can be obtained by:
- Stone Geode at a 1/10 chance
- Buttons found in: C, CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Stone": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "The first true ore. Has marginal value to AIHA Corp and hence leads to more Cash and Rebirths being given.",
        "obtainment": '''First found in the Spawn realm. Also can be obtained by:
- Stone Geode at a 1/20 chance
- White Gems Geode at a 1/6 Chance
- Crystal Geode at a 1/5 Chance
- Buttons found in: C, CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "White Gems": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A less common Ore, can be found in Caves of minimal depth.",
        "obtainment": '''First found in the Caves realm. Also can be obtained by:
- Stone Geode at a 1/333 chance
- White Gems Geode at a 1/10 Chance
- Crystal Geode at a 1/4 Chance
- Iron Geode at a 1/20 Chance
- Buttons found in: CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Crystal": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A minorly rare Ore, typically found in deeper segments of Caves.",
        "obtainment": '''First found in the Crystal Beneaths realm. Also can be obtained by:
- White Gems Geode at a 1/20 Chance
- Crystal Geode at a 1/4 Chance
- Iron Geode at a 1/10 Chance
- Buttons found in: IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Iron": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather sturdy metal that can be useful to create simple items. Because of its various uses Iron often has more proper mining efforts.",
        "obtainment": '''First found in the Iron Shafts realm. Also can be obtained by:
- Crystal Geode at a 1/1,162 Chance
- Iron Geode at a 1/5 Chance
- Gold Geode at a 1/6 Chance
- Buttons found in: GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Gold": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Although Gold lacks common use, it is often used for jewellary and with its rarity gains value from that.",
        "obtainment": '''First found in the Golden Quarry realm. Also can be obtained by:
- Gold Geode at a 1/4 Chance
- Quartz Geode at a 1/8 Chance
- Jade Geode at a 1/2 Chance
- Buttons found in: QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Quartz": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A semi-precious stone, contains more value in its non-white variants.",
        "obtainment": '''First found in the Quartz Walkway realm. Also can be obtained by:
- Gold Geode at a 1/33 Chance
- Quartz Geode at a 1/5 Chance
- Jade Geode at a 1/4 Chance
- Buttons found in: QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Jade": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A semi-precious stone that to some has minor spirtiual value.",
        "obtainment": '''First found in the Jade Forest realm. Also can be obtained by:
- Quartz Geode at a 1/16 Chance
- Jade Geode at a 1/10 Chance
- Obsidian Geode at a 1/10 Chance
- Buttons found in: OA, CT, UW, VS, Recover Hall'''
    },
    "Obsidian": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Obsidian is known to be volcanic glass formed upon the cooling of lava. Due to its nature Obsidian is abundant in the Obsidian Abyss however AIHA Corp. has brought it to many of the other realms of Buttonia.",
        "obtainment": '''First found in the Obsidian Abyss realm. Also can be obtained by:
- Jade Geode at a 1/1,000 Chance
- Obsidian Geode at a 1/5 Chance
- Buttons found in: CT, UW, VS, Recover Hall'''
    },
    "Ruby": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather precious, typically red gem. Ruby is apart of the RGB gem trifecta.",
        "obtainment": '''First found in the Colour Temple realm. Also can be obtained by:
- Obsidian Geode at a 1/20 Chance
- Ruby Geode at a 1/5 Chance
- Emerald Geode at a 1/10 Chance
- Sapphire Geode at a 1/20 Chance
- Diamond Geode at a 1/3 Chance
- Buttons found in: ET, UW, VS, Recover Hall'''
    },
    "Emerald": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather precious, typically green gem. Emerald is apart of the RGB gem trifecta.",
        "obtainment": '''First found in the Colour Temple realm. Also can be obtained by:
- Ruby Geode at a 1/10 Chance
- Emerald Geode at a 1/5 Chance
- Sapphire Geode at a 1/10 Chance
- Diamond Geode at a 1/3 Chance
- Buttons found in: ET, UW, VS, Recover Hall'''
    },
    "Sapphire": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather precious, typically blue gem. Sapphire is apart of the RGB gem trifecta.",
        "obtainment": '''First found in the Colour Temple realm. Also can be obtained by:
- Sapphire Geode at a 1/20 Chance
- Emerald Geode at a 1/20 Chance
- Sapphire Geode at a 1/5 Chance
- Diamond Geode at a 1/3 Chance
- Buttons found in: ET, UW, VS, Recover Hall'''
    },
    "Diamond": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Often considered the most precious gem and has the highest natural toughness. Its value exponentially decreased after AIHA Corp.'s innovation of asteroid mining.",
        "obtainment": '''First found in the Extraterrestrial Orbits realm. Also can be obtained by:
- Starlight Geode at a 1/10 Chance
- Ion Geode at a 1/2 Chance
- Buttons found in: EI, UW, SD, IP, VS, Recover Hall'''
    },
    "Starlight": {
        "tags": ["Main", "BS:ED", "Stats", "Star", "Space"],
        "lore": "The first ore to transcend regular bounds. Starlight is formed from an endless refraction of... starlight, eventually some of its essence fuses with the rock it touches and forms this ore. AIHA Corp. has patented a method to forcefully condense starlight into rock hence forming the Starlight ore.",
        "obtainment": '''First found in the Extraterrestrial Orbits realm. Also can be obtained by:
- Diamond Geode at a 1/1,666 Chance
- Starlight Geode at a 1/5 Chance
- Ion Geode at a 1/4 Chance
- Buttons found in: EI, UW, SD, IP, VS, Recover Hall'''
    },
    "Ion": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Ion was an ore first created by AIHA Corp. It was formed by continuously bombarding stone with various ions, eventually this caused a transformation to be undergone creating a highly conductive and reactive material that we now call Ion.",
        "obtainment": '''First found in the Empyrean Island realm. Also can be obtained by:
- Starlight Geode at a 1/333 Chance
- Ion Geode at a 1/10 Chance
- Buttons found in: UW, SD, IP, FP, VS, Recover Hall'''
    },
    "Uranium": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "This Uranium is not true uranium, for safety purposes all the radioactive segments of Uranium have been extracted and removed condensed into a different ore and sent to planet [REDACTED] by AIHA Corp. The desolation seen in Uranium Wastelands was caused by the initial radioactivity of Uranium.",
        "obtainment": '''First found in the Uranium Wastelands realm. Also can be obtained by:
- Ion Geode at a 1/4,000 Chance
- Uranium Geode at a 1/5 Chance
- Boracite Geode at a 1/20 Chance
- Buttons found in: SD, IP, FP, VS, Recover Hall'''
    },
    "Bismuth": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Bismuth is a rather colourful ore and a stat Uranium often reaches during the decay process. AIHA Corp. has patented a method to prevent further decay upon reaching Bismuth.",
        "obtainment": '''First found in the Smooth Depths realm. Also can be obtained by:
- Uranium Geode at a 1/666 Chance
- Bismuth Geode at a 1/4 Chance
- Boracite Geode at a 1/10 Chance
- Nissonite Geode at a 1/20 Chance
- Buttons found in: IP, FP, VS, Recover Hall'''
    },
    "Boracite": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Boracite is known to be extremely similar to Bismuth, the reason for this is simply due to the formation process of Boracite. Boracite is formed by fusing a small amount of Nissonite with Bismuth giving it its aquamarine colour.",
        "obtainment": '''First found in the Icy Palace realm. Also can be obtained by:
- Bismuth Geode at a 1/100 Chance
- Boracite Geode at a 1/5 Chance
- Nissonite Geode at a 1/10 Chance
- Buttons found in: FP, T, VS, Recover Hall'''
    },
    "Nissonite": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Nissonite is an unusually rare mineral. Nissonite is specifically formed by long-term exposure to perma-frost requiring billions of years in perfect conditions to form small amounts.",
        "obtainment": '''First found in the Icy Palace realm. Also can be obtained by:
- Boracite Geode at a 1/150 Chance
- Nissonite Geode at a 1/5 Chance
- Orpiment Geode at a 1/100 Chance
- Buttons found in: FP, T, VS, Recover Hall'''
    },
    "Orpiment": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Orpiment is a highly valuable ore having many technological uses and being the basis for the creation of most artifical ores. AIHA Corp. is known to have a monopoly over the Orpiment supply, generating Orpiment on an artificial floating island.",
        "obtainment": '''First found in the Floating Purgatory realm. Also can be obtained by:
- Orpiment Geode at a 1/20 Chance
- Buttons found in: T, VS, AT, FC Recover Hall'''
    },
    "Tetra": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Tetra is an entirely artificial ore, created by AIHA Corp. as the perfect building material. It is believed that Tetratum was entirely made using Tetra.",
        "obtainment": '''First found in the Tetratum realm. Also can be obtained by:
- Buttons found in: VS, AT, FC Recover Hall'''
    },
    "Volt": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Volt is not a traditional ore. Rather Volt is formed by the forced condension of trillions of electrons to create this highly conductive ore. Volt is known to hold an extreme negative charge that is dangerous without proper equipment.",
        "obtainment": '''First found in the Voltaic Sector realm. Also can be obtained by:
- Buttons found in: AT, FC Recover Hall'''
    },
    "Aquamarine": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Aquamarine is known to only be found at the bottom of extremely deep oceans, only being found on approximately 0.001% of planets. The process of forming Aquamarine is still unknown even to AIHA Corp.",
        "obtainment": '''First found in the Abyssal Trenches realm. Also can be obtained by:
- Buttons found in: FC'''
    },
    "Lollipop": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "This ore is not to be confused with the typical sweet treat, it was first discovered on a far-off planet and its supplies is stil extremely limited hence it has high value.",
        "obtainment": '''First found in the Flourish Candylands realm. Also can be obtained by:
- Buttons found in: Anticovery Hall'''
    },
    "C0RR8PT10N": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "This ore is considered to be highly unnatural, it was first created by continuously bombarding rocks with various unstable elements, its believed this eventually led to a 'data overflow' which caused the ore to corrupt into what it is now, experiments are still ongoing hence any quantity of this ore is extremely valuable yet extremely dangerous.",
        "obtainment": '''Only found in the Mechanical Room realm'''
    },
    "Stargazed Metal": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "Stats"],
        "lore": "The first of the transcended ores, AIHA Corp. has no information about its contents as it is simply theorised to exist, it is thought to be created by exposing metal to the extreme cosmic radiation created by the Singularity. Further research is needed, any proof of existence is highly appreciated.",
        "obtainment": '''It is unknown if this ore exists, if it were to exist it would likely be obtained in a place that unites dimensions.'''
    },
    "Gyge": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "Stats"],
        "lore": "Gyge is a member of the theoritical transcendant ores, it is theorised to be the perfect catalyst reducing activation energy for experiments to zero or even into the negatives. If Gyge were to exist it would revolutionise the field of science as we know it. AIHA Corp. will reward any proof of its existence.",
        "obtainment": '''It is unknown if this ore exists, if it were to exist it would likely be obtained in a place that unites dimensions.'''
    },
    "Auly Plate": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "Stats"],
        "lore": "Auly Plate is theorised to be an almost perfect material, easily malleable but also extremely rigid when necessary, it is also theorised to be harder than nearly all known and theorised materials. Any proof to Auly Plate's existence will lead to massive rewards from AIHA Corp.",
        "obtainment": '''It is unknown if this ore exists, if it were to exist it would likely be obtained in a place that unites dimensions.'''
    },
    "Shell Piece": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "The Shell", "Universe", "Finale", "Stats"],
        "lore": '''Shell Piece is the only material capable of containing the Singularity, although it does require the help of some other materials for such a difficult task, the world needs someone to obtain Shell Piece lest the universe collapses. Good luck, you shall need it.''',
        "obtainment": '''The location of this ore is unknown, but it is theorised that it would be found in a place that unites dimensions.'''
    },
    "Singularity": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "The Shell", "Universe", "Finale", "Stats"],
        "lore": '''The Singularity must be contained lest the universe collapses. Search for it, search for it, it must be somewhere, somewhere that we cannot see.''',
        "obtainment": '''We do not know where the Singularity is, as if it was an illusion beyond our vision.'''
    },
    "Capsuled Singularity": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "The Shell", "Universe", "Finale", "Stats"],
        "lore": '''An impossibility, if this were to be created the universe would be saved.''',
        "obtainment": '''5 Shell Piece, 1 Prime Alpha Key, 1 Singularity, 250Sx Shroomite Bars, 1UDe Gems. Combine them and seal away the Singularity for good.'''
    },
    "Starglass": {
        "tags": ["Secret", "BS:ED", "Starglass", "Stats"],
        "lore": "Starglass is formed from the very essence of stars, its first fragment was created by the God of Miners in the core of a dying neutron star, it is thought that looking through the glass will allow you peer into other universes. It is also theorised that Starglass may act as a catalyst for many multiversal reactions perhaps allowing the user to reach a state of mind that transcends consciousness allowing for easy to travel to most dimensions. However due to its power the God of Miners has hidden Starglass within his own home, it is known that 10 keys must be found, each one unlocking the path to the next, to create a spatial rift that upon reaching its closure will bring the daring person to the God of Miners home. It is unlikely that the God of Miners will give the ore even then.",
        "obtainment": "Find another path in a place where you meet the God."
    },
    "Darkmatter": {
        "tags": ["Secret", "BS:ED", "Darkmatter", "Stats"],
        "lore": "In the light of recent discoveries Darkmatter is not only a mysterious matter taking up the necessary mass for gravity to act as observed but it also is the fabric between dimension actively preventing multiversal collapse with its mere presence however Darkmatter seems to be almost as elusive as the legendary Starglass hence research attempts are still ongoing.",
        "obtainment": "Some theorise Darkmatter to be made of Weakly Interacting Massive Particles (WIMPs), if this were true it would theoritically be possible to catch microscopic amounts of these WIMPs given the right technology. There have already been attempts with electrons however so far all have failed. Perhaps a place with a more condensed and chaotic amount of such may rarely catch a few of these mysterious WIMPs."
    },
    "Lightmatter": {
        "tags": ["Secret", "BS:ED", "Lightmatter", "Stats"],
        "lore": "In light of Noether's theorem energy is known to not be conserved on a universal scale, as the expansion of the universe leads to a lack of time-based symmetry. However studies in this universe have shown otherwise, energy seems to be generated by an unknown source, this source has been dubbed 'Lightmatter' by some as a nod to how Darkmatter was used to explain the unusual amount of mass expected from galaxies.",
        "obtainment": "Antithesis of darkness."
    },
    "Ivory": {
        "tags": ["Exclusive", "P2W", "BS:ED", "Stats"],
        "lore": "An extremely rare ore that seems to only have one copy available at any given time.",
        "obtainment": "Given to VIPs in AIHA Corp."
    },
    "Totality": {
        "tags": ["Revival", "BS:ED", "Finale", "Insanely Rare", "Geode", "Stats"],
        "lore": "Gods do not just die, their essence is split across the multiverse their many aspects absorbed by what they once controlled. You once feared the Singularity, how foolish. This was the greatest reality, look beyond the remnants of what once was and ascend. All those worlds mean nothing to you anymore, that pitiful God of Miners, the little ant they call 'Rodrigo' and even the man behind the desk who calls himself The Administrator or perhaps your old friend Dommy. They all don't matter now. Look at what you have and smile, you are beyond the Gods, you do not simply hold power you are power. TRANSMISSION INTERRUPTED. Totality i$ thought t0 h@ve b3en formed 8y the de4th of the God of M!ners, h1s essenc3 be!ng split !n two, 1nto Purity, his heart, and Totality, his power. B0th are !ncr3d18ly unst48l3.",
        "obtainment": "Obtained from the Revival Geode at a 1 in 47145471001 chance."
    },
    "Eternabasite": {
        "tags": ["Whitespace", "-Basite", "Secret", "Stats"],
        "lore": "The theoritical final ore of the Polybasite series, existing in a place far beyond regular dimensions, existing in a place hidden within Eternity. It is unclear to any member of AIHA Corp. on how Eternabasite may be obtained, or if it even exists, such an ore is likely beyond the power of even the God of Miners. It is theorised that the first step to obtaining the ore may be accquring the Obliterator's Amulet, however the amulet is thought to be long lost.",
        "obtainment": "Rodrigo had a strange amulet last time you saw him... perhaps he is hiding within the Whitespace"
    },
    "DENIAL": {
        "tags": ["Secret", "Stats"],
        "lore": "ACCESS DENIED",
        "obtainment": "ADMINISTRATOR ACCESS REQUIRED"
    },
    "Master Cash": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "It is thought that the Elysian Stratosphere is a divine reflection of the world of Buttionia, hence the ores here seem to be superior versions of its very own. Master Cash has been supplied to you by AIHA Corp. as the inhabitants do not accept regular Cash in this world.",
        "obtainment": "Enter the Elysian Stratosphere"
    },
    "Master Multiplier": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "The ultimate form of Multiplier, increasing your gain of Master Cash.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Elysian Highway but also can be found in: CR, RoF, DC, L, FA"
    },
    "Master Rebirths": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "The ultimate form of Rebirths, a massive improvement when compared to the original.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Elysian Highway but also can be found in: CR, RoF, DC, L, FA"
    },
    "Master Stone": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Regular stone is weak and brittle. Master Stone is far superior than any earthly materials being far stronger than most conventional and unconventional materials such as Diamond.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Elysian Highway but also can be found in: CR, RoF, DC, L, FA"
    },
    "Master White Gems": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "It is overall unknown what makes Master White Gems superior to White Gems... is it... whiter..?",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Elysian Highway but also can be found in: CR, RoF, DC, L, FA"
    },
    "Master Crystal": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Although Crystal is typically a mineral of low value Master Crystal far surpasses the value of almost all earthly minerals.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Elysian Highway but also can be found in: CR, RoF, DC, L, FA"
    },
    "Master Iron": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "A much sturdier version of the generic metal, it is thought to be capable of rivalling the mythical Mythril",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Cosmic Road but also can be found in: RoF, DC, L, FA",
    },
    "Master Gold": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Gold does not seem to have much physical advantage over regular Gold, however it holds a value to the Elysian Stratosphere's inhabitants similar to how we value Gold",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Cosmic Road but also can be found in: RoF, DC, L, FA"
    },
    "Master Quartz": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Quartz seems to have higher value than Master Gold for reasons currently unknown...",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on the Cosmic Road but also can be found in: RoF, DC, L, FA"
    },
    "Master Jade": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Jade does not seem to only hold spiritual value but also contain some spirits of the dead. Truly a divine reflection of the earthly mineral.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in the Room of Fate but also can be found in: DC, L, FA",
    },
    "Master Obsidian": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "The formation process of Master Obsidian is currently Unknown to AIHA Corp. More is to be desired from this unique mineral",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in the Room of Fate but also can be found in: DC, L, FA"
    },
    "Master Ruby": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "The first member of the mastered gem trifecta, Master Ruby is considered noticeably more valuable then the prior master minerals.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in the Room of Fate but also can be found in: DC, AA, L, FA"
    },
    "Master Emerald": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "The second member of the mastered gem trifecta, Master Emerald has similar value to Master Ruby but still stands as a marginally more valuable mineral",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in Dark Council but also can be found in: AA, L, FA"
    },
    "Master Sapphire": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "The third and final member of the mastered gem trifecta, Master Sapphire holds similar value to Master Ruby and Master Emerald but still stands above both as the better mineral. Of course it still lays below Master Diamond in value.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in Dark Council but also can be found in: AA, L, FA"
    },
    "Master Diamond": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "The earthly variant of this mineral is both valuable and a sturdy material, similar applies to Master Diamond, it is highly valuable within the Elysian Stratosphere and is extremely difficult to scratch, it is approximated to be 1Sx times higher on the hardness scale.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in Dark Council but also can be found in: AA, L, TLG, FA"
    },
    "Master Starlight": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Starlight is formed by the endless refraction of the light originating from distant supernovae eventually condensing into a near-solid form.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in the Astral Archipelago but it may also be found in: L, TLG, FA"
    },
    "Master Ion": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Just like Ion, Master Ion was at first an artifical ore being formed by continuous bombardment of rare ions such as those of Oganesson on Master Stone, eventually forming Master Ion.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in the Astral Archipelago but it can also be found in: L, TLG, FA"
    },
    "Master Uranium": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Unlike the Uranium found in the Uranium Wastelands, Master Uranium has retained a minor amount of it radioactivity, although most of it has still been extracted and condensed into an ore located in planet [REDACTED].",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in the Astral Archipelago but it may also be found in: L, TLG, FA"
    },
    "Master Bismuth": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Bismuth is the remnant of when Master Uranium once decayed with an extremely small portion managing to stop in the midst of the cycle retaining itself as Master Bismuth",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in Limbo but it may also be found in: TLG, FA"
    },
    "Master Boracite": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Boracite is formed in a similar fashion to Boracite requring the fusion of Master Bismuth with a fragment of Master Nissonite.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in Limbo but it may also be found in: TLG, FA"
    },
    "Master Nissonite": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Nissonite requires Master Stone to be exposed to subzero-kelvin temperatures to be slowly formed over thousands of years the bose-einstein condensate eventually forming into this ore.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found in Limbo but it may also be found in: TLG, FA"
    },
    "Master Orpiment": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Orpiment is a highly valuable ore being responsible for much of the advanced technology found in the Elysian Stratosphere, however Master Orpiment has incredibly strict compatibility issues.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on The Lost Grounds but it may also be found in: FA"
    },
    "Master Tetra": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Many consider Master Tetra to be the final building material, it fills almost every possible need other than the potential to contain the Singularity...",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on The Lost Grounds but it may also be found in: FA"
    },
    "Master Volt": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Volt is created by the extreme condension of countless electrons into a small space, creating this unique mineral that acts as a universal superconductor. Master Volt is highly compatible with both Master Orpiment and Master Tetra.",
        "obtainment": "Obtained through various buttons in the Elysian Stratosphere, first found on The Lost Grounds but it may also be found in: FA"
    },
    "Master Aquamarine": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Aquamarine requires extreme oceanic pressure to be formed, hence the only known planet where Master Aquamarine has been naturally formed is Atlanta-497, it is also believed that Atlanta-497 contains [REDACTED].",
        "obtainment": "Obtained through a singular button in the Elysian Stratosphere and is only found within the Forbidden Altar."
    },
    "Master Lollipop": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Lollipop is an ore so valuable that perhaps enough of it could be traded for the Prime Alpha Key, nothing is known about its formation process.",
        "obtainment": "Approach the Forbidden Altar, it will stand nearby."
    },
    "Master Mint": {
        "tags": ["Mastery", "BS:ED", "Stats"],
        "lore": "Master Mint is an ore that exists in relatively small amounts, its only known uses are for 'recovery buttons' and to craft one of the 3 Demigod Stats",
        "obtainment": "Accessible in the Elysian Stratosphere in the Astral Archipelago."
    },
    "Prime Alpha Key": {
        "tags": ["Mastery", "BS:ED", "Finale", "The Shell", "Stats"],
        "lore": "No copy of the Prime Alpha Key has ever been obtained by AIHA Corp. hence information is extremely limited. It is known to be the most valuable item that exists within the Elysian Stratosphere and a key part of creating a capsule for the Singularity, due to its extreme value the Prime Alpha Key is highly guarded, it is theorised that the key is protected by the God of Miners himself, it is believed that making a sufficient offering at a specific altar may earn you the key, but the theory has not been proven.",
        "obtainment": "Find the Forbidden Altar somewhere in the Elysian Stratosphere and make a sufficient offering."
    },
    "Gems": {
        "tags": ["BS:ED", "Stats"],
        "lore": "A simple yellow gem, it's value seems to increase exponentially in larger numbers. AIHA Corp. supplies it regularly to employees and also uses it as a currency for general trading, it is known that Gems can be traded back for 'boosts'.",
        "obtainment": "Gems are passively given by AIHA Corp."
    },
    "Event Power": {
        "tags": ["BS:ED", "Stats"],
        "lore": "Not much is known about this mineral, it is regularly supplied by AIHA Corp. and is rarely usable.",
        "obtainment": "Event Power is passively given by AIHA Corp."
    },
    "Purity": {
        "tags": ["BS:ED", "Stats", "Geode", "Revival", "Insanely Rare"],
        "lore": "Gods don't just die, they only fade from memory until nothing remains, but in the time between their remnants will still be visible. When the God of Miners met its end its essence was split into countless ores, but most of it was concentrated into two parts. Purity and Totality. The former was the essence of the God's soul whilst the other was of its power. Its thought that if all the ores containing its essence were combined then perhaps the God of Miners could be reborn. Purity is a unique gem, it is thought that somewhere deep into the colossal crystal is a figure, forever crystalised, who that figure is has been left to theory. Some believe that Purity acts as a beating heart, without it, although the universe would not collapse, the universe would lose its inherent beauty.",
        "obtainment": "Obtained from the Revival Geode at a 1/17891091451 chance."
    },
    "Buttons Pressed": {
        "tags": ["BS:ED", "Stats", "Statistic"],
        "lore": "A record of the total amount of buttons the user has pressed, can very rarely be traded in for other currencies.",
        "obtainment": "Obtained from the pressing of most buttons, excludes recoveries."
    },
    "Geodes Opened": {
        "tags": ["BS:ED", "Stats", "Statistic"],
        "lore": "A record of the total amount of geodes the user has opened, can very rarely be traded in for other currencies.",
        "obtainment": "Obtained from the opening of any and all geodes."
    },
    "Alpha Point": {
        "tags": ["BS:ED", "Stats", "Event"],
        "lore": "A strange item which seems to only exist as a remnant of times long gone.",
        "obtainment": "Obtained from the 'Alpha Event' or from the Mint Geode at a 1/2 Chance."
    },
    "Graphite": {
        "tags": ["BS:ED", "Stats", "Secret", "Bolical"],
        "lore": "An ore previously given the name 'Desmos', it is believed that a user having high mathematical capabilities may help in the obtainment of this ore.",
        "obtainment": "Found in a place of great geometry, what may seem simple at first will quickly become complex."
    },
    "Stellarite": {
        "tags": ["BS:ED", "Stats", "Secret", "Star", "Space"],
        "lore": "Stellarite is an ore formed from the dust of stars and is often confused with its much more common counterpart: Starlight, it's location was once known but due to solar flares disrupting the database only fragments of its co-ordinates are known.",
        "obtainment": "Somewhere floating around in Earth's orbit, perhaps it may be caught by some stations in orbit. It's co-ordinates are currently unknown, however it is theorised to be one of the following: (3,243.2583, 5,261.8927), (3,540.2385, 237.8977), (3,040.8689, 7,290.8997), (3,240.228, 1,203.8957)"
    },
    "Galaxite": {
        "tags": ["BS:ED", "Stats", "Secret", "Star", "Space"],
        "lore": "Galaxite is much more condensed version of Stellarite, it not made of just the dust of stars but the dust of entire galaxies. It is believed that it may have been lost to a fracture in the spacetime continuum.",
        "obtainment": "Lost in a Wormhole, perhaps you can find a way in."
    },
    "Esadrhium": {
        "tags": ["BS:ED", "Stats", "Secret", "Bolical"],
        "lore": "Esadrhium is an extremely versatile mineral capable of shifting its shape to match any need making it the perfect building material.",
        "obtainment": "Prove yourself an mathematical architect in a place of great geometry."
    },
    "Tesseract": {
        "tags": ["BS:ED", "Stats", "Secret", "Bolical"],
        "lore": "Tesseract is a 4th dimensional mineral easily capable of bending 3rd dimensional logic, due to this it would be extremely useful for architecture.",
        "obtainment": "Become a master of the art of mathematics."
    },
    "Sloth": {
        "tags": ["BS:ED", "Stats", "Secret", "Sin"],
        "lore": "Sloth is one of the 7 cardinal sins, an ore created when Kanoite was split into its fundamental fragments. It is thought to only appear to those who dare to demonstrate immense amounts of lethargy.",
        "obtainment": "You're a bad person. (Start in Spawn)"
    },
    "Pride": {
        "tags": ["BS:ED", "Stats", "Secret", "Sin"],
        "lore": "Pride is one of the 7 cardinal sins, an ore created when Kanoite was split into its fundamental fragments. It is thought to appear to those who demonstrate immense hubris.",
        "obtainment": "You're a bad person. (Unimplemented)"
    },
    "Gluttony": {
        "tags": ["BS:ED", "Stats", "Secret", "Sin"],
        "lore": "Sloth is one of the 7 cardinal sins, an ore created when Kanoite was split into its fundamental fragments. It is thought to only appear to those who prove themselves to be gluttonous.",
        "obtainment": "You're a bad person. (Start in the Quartz Walkway)"
    },
    "==INFINITY==": {
        "tags": ["BS:ED", "Stats", "Secret", "Lightmatter", "Darkmatter", "Final"],
        "lore": "Some things were not made for mortal comprehension.",
        "obtainment": "Omnipresence, Omnipotence, Omniscience"
    },
    "Mint": {
        "tags": ["BS:ED", "Stats"],
        "lore": "Mint, it seems to have many similarities to its earthly variant, for unknown reasons this ore is exclusively found in the Minty Grooves.",
        "obtainment": "Mint can be obtained from buttons exclusively found in the Minty Grooves, including from the Mint Geode at a 1/2 chance"
    },
    "Metal": {
        "tags": ["BS:ED", "Stats", "Stardustry"],
        "lore": "A generic piece of metal, all attempts to identify what the metal is have failed.",
        "obtainment": "Obtainable from buttons exclusively found in the Stardustry"
    },
    "Press": {
        "tags": ["BS:ED", "Stats", "Stardustry"],
        "lore": "A hydraulic press, likely used to compress Metal, its material remains unidentified.",
        "obtainment": "Obtainable from buttons exclusively found in the Stardustry"
    },
    "Microparticles": {
        "tags": ["BS:ED", "Stats", "Stardustry"],
        "lore": "Microscopic particles of star dust, its believed that these may be used to give Metal and Press their unique properties.",
        "obtainment": "Obtainable from buttons exclusively found in the Stardustry"
    },
    "Star": {
        "tags": ["BS:ED", "Stats", "Stardustry"],
        "lore": "An artificial, miniature star, it is unclear as to why stardust is being used to create these miniature stars.",
        "obtainment": "Obtainable from buttons exclusively found in the Stardustry"
    },
    "Robot": {
        "tags": ["BS:ED", "Stats", "Stardustry"],
        "lore": "A basic robot that seems to use the minature stars as a source of its energy. Is this perhaps the purpose of the Stardustry?",
        "obtainment": "Obtainable from buttons exclusively found in the Stardustry"
    },
    "Prototype": {
        "tags": ["BS:ED", "Stats", "Stardustry"],
        "lore": "A prototype for a machine that as of now serves no clear purpose.",
        "obtainment": "Obtainable from buttons exclusively found in the Stardustry"
    },
    "Rune": {
        "tags": ["BS:ED", "Stats", "Craftable"],
        "lore": "A generic rune, its magic seems to increase the production of some of your early stats.",
        "obtainment": "Combine 100Oc Rebirths with 150 Stone"
    },
    "Ultrabirth": {
        "tags": ["BS:ED", "Stats", "Craftable"],
        "lore": "An improved variant of the Rebirth, it sacrifices Multiplier gain for increased Cash production.",
        "obtainment": "Combine 1No Cash with 5 Rebirths"
    },
    "Cosmic Crystal": {
        "tags": ["BS:ED", "Stats", "Craftable"],
        "lore": "A sample of Crystal imbued with minor amounts of cosmic energy.",
        "obtainment": "Infuse 1Oc Rebirths into a Crystal, infuse 150k White Gems into another and proceed to fuse the Crystals together"
    },
    "Abstract Bar": {
        "tags": ["BS:ED", "Stats", "Craftable"],
        "lore": "A completely useless item, the bar acts as an abstract base and can easily be infused with other materials to give it unique properties.",
        "obtainment": "With 1e+5000 Iron, 100No Tetra, 10 Runes and a Cosmic Crystal this bar can be forged, the Iron welding together the Tetra and the Runes with the Cosmic Crystal allowing for easier infusion with other minerals"
    },
    "Chlorophyte": {
        "tags": ["BS:ED", "Stats", "Craftable"],
        "lore": "A failed product of AIHA Corp. It was made in an attempt to absorb rays of starlight to ease the creation of the Starlight ore.",
        "obtainment": "Create a perfect lattice of 5e+2500 Stone, 7e+777 Uranium and 5e+555 Boracite to create a system that is capable of converting 100% of incoming starlight into a source of condensed energy."
    },
    "Chlorophyte Bar": {
        "tags": ["BS:ED", "Stats", "Craftable"],
        "lore": "An Abstract Bar infused with Chlorophyte, it's properties allow it to condense all forms of energy, easing the creation of countless ores.",
        "obtainment": "Such a material is not easy to create, it requires 1Qd Abstract Bars, 1M Chlorophyte and 1k Lollipop, the mix of materials give it its unique properties."
    },
    "Shroomite Bar": {
        "tags": ["BS:ED", "Stats", "Craftable"],
        "lore": "An Abstract Bar infused with C0RR8PT10N, the mix of it with Chlorophyte Bars creates the unique mineral of Shroomite, which has virtually endless uses. Only one bar of Shroomite has ever been made by AIHA Corp.",
        "obtainment": "Infuse 10Qd Abstract Bars with 10 Chlorophyte Bars and 1 C0RR8PT10N, the C0RR8PT10N changes the properties of the Chlorophyte Bars, leading to this unique mineral."
    },
    "Sigil of The Unknown": {
        "tags": ["BS:ED", "Stats", "Craftable", "Demigod"],
        "lore": "The Sigil of The Unknown is one of the few Demigod Stats, stats which are so difficult to obtain that anyone capable of obtaining them is thought to be a demigod. The Sigil is thought to be the mark of an unknown god from the early stages of this universe. It's properties are unknown as at most AIHA Corp. has only observed it from afar.",
        "obtainment": "It is theorised with a sufficient offering the Sigil may appear. The estimated offering is: 5Qn Gems, 5 C0RR8PT10N, 1No Mint, 10 Master Lollipop, 12.5M Master Mint, 1e+303 Rune, 1e+303 Ultrabirth, 1 Shroomite Bar, 1 Sloth, 1 ARG, 1 Meridianiite, 100 Neuron, 3 Volcanic Molybdenum, 10 Osmium, 3 Sphene, 1 Talc, 1 Equinox and 1 Molybdenum."
    },
    "King Crystal": {
        "tags": ["BS:ED", "Stats", "Craftable", "Demigod"],
        "lore": "This crystal is one of the few Demigod Stats, stats which are so difficult to obtain that anyone capable of obtaining them is thought to be a demigod. The King Crystal is generally agreed to be beautiful, it is believed to have been owned by a king from an age long past. Only mere fragments of the crystal have survived to this day, its components have been found through atomic inspection but no attempt to recreate the crystal has been successful.",
        "obtainment": "This ore can be created through infusing crystals and ores into other ores, a grand total of: 1Qn Gems, 1 Witherite, 1 Antimony, 1 Biotite, 1 Red Quartz, 1 Iridium, 1 Possessed Quartz, 1 Oortodium, 750 Amethyst, 2 Paradoxite, 1k Grail, 1 Mythril, 2 Opal, 2 Uzik, 30 Tungsten, 10 Heazlewoodite, 25 Dragonglass, 5 Prismarine, 2 Garnet and 2 Grandidierite."
    },
    "Anomaly": {
        "tags": ["BS:ED", "Stats", "Craftable", "Demigod"],
        "lore": "This substance is thought to be an especially volatile fragment of the unnamed substance that makes up this Reality. The Anomaly has undefined properties, all attempts to discern any particular details have failed. Only theories exist as to how to possibly create another sample of this substance. Ignore the 'obtainment' passage below, it is unknown who put it there.",
        "obtainment": "Combining 1Qn Gems, 1 Prime Alpha Key, 50 Prototype, 1 Unova, 1e+1000 Cosmic Crystal, 1 Heavenlium, 1 Omet, 1 Chroma, 1 Polybasite, 3 Mortalstone, 6 Rune, 3 Cloom, 1k Wicked Branch and 1 Megabasite should temporarily destabilise a portion of Reality."
    },
    "Timeless Quartz": {
        "tags": ["BS:ED", "Stats", "Craftable", "Demigod"],
        "lore": "This unique variant of Quartz is thought to be only obtainable by a true architect of eternity. It is believed to have formed from a multiversal collision between this Universe and another, far more 'nostalgic' universe. This collision has only ever occured once hence limiting the amount that can exist.",
        "obtainment": "100 Master Lollipop, 1 Prime Alpha Key, 250 C0RR8PT10N, 1De Gems, 1 Brookite, 1.75k Wicked Branch, 600 Mushroom, 7 Galarium, 75 Zanyte, 1 Holeyum, 1 Quetzalcoatlite, 25 Doomdilite, 200 Ancar, 10 Dime, 1 Milky Quartz, 1 Angelicas and 1 Ectoplasm, it was never going to be easy."
    },
    "Glitchared": {
        "tags": ["BS:ED", "Stats", "Secret", "Moonbase"],
        "lore": "The ore seems to be consistently changing its nature as some of its properties seem uncertain.",
        "obtainment": "Get Glitchared FOR FREE using EasyKidsMalware.exe, just follow the instructions and you'll get a free Glitchared :D\nThere have been several reports that the program may corrupt 'savefiles', it is highly recommended you 'save' by 'closing' the 'program' before attempting to use the 'service'"
    },
    "Test Page": {
        "tags": ["Test"],
        "raw_text": f'''<h1>Test Page</h1><br>
        <img src="{global_path_reference}/Program/Stats/777.webp"><br>
        {{exec:test_function()|Command test}}<br>
        Congrats, you found the test page! {{stat:Testium|Why not go here?}}'''
    },
    "Tutorial": {
        "tags": ["Tutorial"],
        "raw_text": '''<h1>Tutorial</h1><br>
        Hello!<br>
        It seems as if you've found the tutorial page!<br>
        So I presume you need a guide as to how the world of {link:Buttonia|Buttonia} works right?<br>
        Well, you've come to the right place.<br>
        Below are some explanations for some of the key features of this {link:Worlds|World!}<br><br>
        {link:Tutorial: Cost Buttons|Cost Buttons}<br>
        {link:Tutorial: Reset Buttons|Reset Buttons}<br>
        {link:Tutorial: Recoveries|Recovery Buttons}<br>
        {link:Tutorial: CY47|Cytherax-47}<br>
        {link:Tutorial: Crafting|Crafting}<br>
        {link:Tutorial: Geode|Geode Buttons}<br>
        {link:Tutorial: Boosts|Boosts}<br>
        {link:Tutorial: World Badges|World Badges}'''
    },
    "Tutorial: Cost Buttons": {
        "tags": ["Tutorial"],
        "raw_text": '''<h1>Tutorial: Cost Buttons</h1><br>
        Cost buttons are rather self explanatory, they give you a given amount of stat for a given amount of a lower stat.<br>
        No, this is not something that will be explicitly telegraphed to you.<br>
        Unluckily for you not many buttons will be using this mechanic are most will instead {link:Tutorial: Reset Buttons|reset} your stats instead.<br>
        {stat:Multiplier|Multiplier}, {stat:Emerald|Emerald}, {stat:Sapphire|Sapphire} and their {search:Mastery|Master Stat} equivalents all use this mechanic, so do the {link:Discount Buttons|Discount Buttons} in {link:Colour Temple|Colour Temple}.<br>
        Also the multiplier equivalent in most {link:Worlds|Worlds} will use this mechanic for obvious reasons.<br>
        Enjoy the use of those buttons when you can, they might take a while sometimes, but the pain the {link:Tutorial: Reset Buttons|reset buttons} will cause you.<br>
        <br>
        {link:Tutorial|Want to go back to the central Tutorial page?}'''
    },
    "Tutorial: Reset Buttons": {
        "tags": ["Tutorial"],
        "raw_text": '''<h1>Tutorial: Reset Buttons</h1><br>
        Reset buttons are rather self explanatory, they give you a given amount of a stat but reset all prior stats in the progression.<br>
        Almost all buttons you will find are reset buttons, abiding by the usual incremental progression of reseting for boosts of earlier stats.<br>
        A minority of stats that exist outside of the {search:Main|Main Progression} will reset some of your stats up to a certain point, of course these stats will boost your main progression stats.<br>
        These buttons, unsurprisingly, are extremely punishing, hence {link: Tutorial: Recoveries|Recovery Buttons} exist to help you, well, recover.<br>
        <br>
        {link:Tutorial|Want to go back to the central Tutorial page?}'''
    },
    "Tutorial: Recoveries": {
        "tags": ["Tutorial"],
        "raw_text": '''<h1>Recovery Buttons</h1><br>
        Recovery Buttons are self explanatory, they allow you to recover from the otherwise harsh resets that come from {link:Tutorial: Reset Buttons|reset buttons}, although in some cases they will only slightly help you.<br>
        There are 2 types of recovery buttons:<br>
        - MHLTCP (Must Have Less Than Currency Purchased) Buttons (labelled as "Sets" buttons in this game) which set the given currency to a set amount, ignoring any stat multipliers you have and not adding anything if you already have more than the given amount of that currency.<br>
        - WFC (Won't Fetch Currency) Buttons (labelled as "Fetches" buttons in this game) which give you an amount of that stat as if you were using a cost/reset button WITHOUT costing/reseting you at all, which means that your stat multipliers WILL apply, these buttons will be EXTREMELY useful when attempting to get leaderboard positions.<br>
        DO NOT FORGET YOUR RECOVERIES IT WILL COST YOU<br>
        AND DO NOTE THAT NOT ALL {link:Worlds|WORLDS} WILL HAVE A {link:Recover Hall|RECOVER HALL} SO IF YOU LEAVE THAT {link:Realms|REALM} YOU WILL NOT BE ABLE TO ACCESS THE RECOVERIES IN IT<br>
        <br>
        {link:Tutorial|Want to go back to the central Tutorial page?}'''
    },
    "Tutorial: CY47": {
        "tags": ["Tutorial", "Cytherax-47"],
        "raw_text": '''<h1>Tutorial: Cytherax-47</h1><br>
        Wait, wait, wait, you're telling me you successfully navigated this far into the system without having a the faintest idea on how this thing is meant to work?<br>
        Well, worry no more, as now you can finally understand how this system works!<br>
        So the whole search system is rather simple:<br>
        - The system searches for exact name matches<br>
        - The system searches for exact tag matches (tags include stuff like: Mastery, Tutorial, Stats, BS:ED)<br>
        - As a last resort the system checks for partial name or tag matches<br>
        Simple, right?<br>
        <br>
        Also, just for your convenience, there are links to other pages on pages!<br>
        Why aren't the links highlighted? Because uh...<br>
        Anyway, in the case you haven't seen any stat pages yet, just know that they look entirely different to these pure text pages.<br>
        You're going to need those pages, they'll give you all the information you need about them, including information about how to obtain them and arguably most importantly: the stat multipliers.<br>
        Have fun :)<br>
        <br>
        {link:Tutorial|Want to go back to the central Tutorial page?}<br>
        <br>
        <br>
        Probably useful to mention that some links execute commands...'''
    },
    "Tutorial: Crafting": {
        "tags": ["Tutorial"],
        "raw_text": '''<h1>Tutorial: Crafting</h1><br>
        Crafting is a pretty simple mechanic, you spend an amount of stats to craft one singular stat which give you stat boosts, what's new?<br>
        There's also a menu for it, I guess.<br>
        You cannot even begin to comprehend how hard it was to make for how simple the actual mechanic is.<br>
        <br>
        Just a word of warning, but after a {stat:Stargazed Metal|certain point in main progression}, the stats will reset your craftable stats other than the "demigod stats" (craftable stats that are insanely difficult to craft)<br>
        <br>
        {link:Tutorial|Want to go back to the central Tutorial page?}'''
    },
    "Tutorial: Geode": {
        "tags": ["Tutorial"],
        "raw_text": '''<h1>Tutorial: Geode Buttons</h1><br>
        Geodes are the game's major RNG mechanic, when you press a geode button it will take the amount of currency that it advertises, and then in return it will give you a random item, with the chances being listed on their respective page in this database.<br>
        It should be noted that event geodes are known to be much much more powerful than regular geodes, most of these previous event geodes can be found in the {link:Geode Site|Geode Site}.<br>
        To increase your geode luck and geode speed you have to increase your {link:Tutorial: Boosts|Boosts}.<br>
        Geode speed begins at a maxiumum of 1s and can eventually fall down to 0.15s, the value determines the manual cooldown that exists between button presses.<br>
        <br>
        {link:Tutorial|Want to go back to the central Tutorial page?}'''
    },
    "Tutorial: Boosts": {
        "tags": ["Tutorial"],
        "raw_text": '''<h1>Tutorial: Boosts</h1><br>
        Boosts are a major mechanic of the game and can be bought with {stat:Gems|gems}, a vast majority of boosts are self-explanatory, but a few are not.<br>
        The "Lucky Draw" boost increases the random chance of you having a random 100x cash boost when gaining cash, increasing by 1% per upgrade.<br>
        The "Lucky Multiplier" boost increases the multiplication of the boost that you get from the Lucky Draw.<br>
        Geode Express is simply a faster geode speed boost<br>
        Offline Geodes allows you to run geodes whilst not actively playing the game itself.<br>
        These boosts are essential for progression and it is recommened that you buy them when possible.<br>
        <br>
        {link:Tutorial|Want to go back to the central Tutorial page?}'''
    },
    "Tutorial: World Badges": {
        "tags": ["Tutorial"],
        "raw_text": '''Tutorial is coming never<br>{link:Tutorial|Return?}'''
    },
    "EasyKidsMalware.exe": {
        "tags": ["Antivirus"],
        "raw_text": f'''How to obtain Glitchared!<br>
        1. Press win+R<br>
        2. Copy and paste the text below into the "Run" window and press enter<br>
        {f'''powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File {global_path_reference}\\TotallySafeScript.ps1'''}<br>
        3. Enjoy!!!'''
    }
}
badge_data = {
    "Pre-existence": {
        "Byte 1": {
            "Display": "Kilobyte",
            "Gradient": "Byte",
            "Reqs": {
                "Byte": 1024
            },
            "Consume": True,
            "Multis": {
                "Byte": 3
            }
        },
        "Byte 2": {
            "Display": "Megabyte",
            "Gradient": "Byte",
            "Reqs": {
                "Byte": 1048576
            },
            "Consume": True,
            "Multis": {
                "Byte": 10
            }
        },
        "Byte 3": {
            "Display": "Gigabyte",
            "Gradient": "Byte",
            "Reqs": {
                "Byte": 1048576
            },
            "Consume": True,
            "Multis": {
                "Byte": 1024
            }
        },
      "Binary 1": {
              "Display": "Boolean",
              "Gradient": "Binary",
              "Reqs": {
                  "Binary": 1e6
              },
              "Consume": True,
              "Multis": {
                  "Byte": 2,
                  "Binary": 2
              }
          },
      "Script 1": {
              "Display": "Initialisation",
              "Gradient": "Script",
              "Reqs": {
                  "Script": 10
              },
              "Consume": True,
              "Multis": {
                  "Byte": 10,
                  "Binary": 4,
                  "Script": 1.5
              }
          },
      "Script 2": {
              "Display": "Programmatic Basics",
              "Gradient": "Script",
              "Reqs": {
                  "Script": 1e6
              },
              "Consume": True,
              "Multis": {
                  "Byte": 100,
                  "Script": 4
              }
          },
      "Script 3": {
              "Display": "Module",
              "Gradient": "Script",
              "Reqs": {
                  "Script": 1e33
              },
              "Consume": True,
              "Multis": {
                  "Byte": 1e6,
                  "Binary": 100,
                  "Script": 100,
                  "Language": 10
              }
          },
      "Language 1": {
              "Display": "Pseudocode",
              "Gradient": "Language",
              "Reqs": {
                  "Language": 1
              },
              "Consume": True,
              "Multis": {
                  "Binary": 2,
                  "Language": 1.1
              }
          },
      "Language 2": {
              "Display": "Python",
              "Gradient": "Language",
              "Reqs": {
                  "Language": 10
              },
              "Consume": True,
              "Multis": {
                  "Byte": 10,
                  "Binary": 4,
                  "Script": 15,
                  "Language": 2
              }
          },
      "Language 3": {
              "Display": "C",
              "Gradient": "Language",
              "Reqs": {
                  "Language": 1000
              },
              "Consume": True,
              "Multis": {
                  "Byte": 15,
                  "Binary": 6,
                  "Language": 3
              }
          },
      "Language 4": {
              "Display": "C#",
              "Gradient": "Language",
              "Reqs": {
                  "Language": 1e6
              },
              "Consume": True,
              "Multis": {
                  "Binary": 3.5,
                  "Script": 20,
                  "Language": 5
              }
          },
      "Language 5": {
              "Display": "Whose idea was it to make Javascript?",
              "Gradient": "Language",
              "Reqs": {
                  "Language": 1e7
              },
              "Consume": True,
              "Multis": {
                  "Byte": 0.5,
                  "Binary": 0.5,
                  "Script": 0.5,
                  "Language": 7
              }
          },
      "Language 6": {
              "Display": "C++",
              "Gradient": "Language",
              "Reqs": {
                  "Language": 1e9
              },
              "Consume": True,
              "Multis": {
                  "Byte": 16,
                  "Binary": 7,
                  "Script": 21,
                  "Language": 8
              }
          },
      "Language 7": {
              "Display": "Assembly",
              "Gradient": "Language",
              "Reqs": {
                  "Language": 1
              },
              "Consume": True,
              "Multis": {
                  "Byte": 1e6,
                  "Binary": 1e5,
                  "Script": 0.2,
                  "Language": 100
              }
          },
      "RAM 1": {
              "Display": "SSD",
              "Gradient": "RAM",
              "Reqs": {
                  "RAM": 10
              },
              "Consume": True,
              "Multis": {
                  "RAM": 2
              }
          },
    },
    "Moonbase": 
        {
          "Booster 1": {
              "Display": "Outerspace Inflation",
              "Gradient": "Booster",
              "Reqs": {
                  "Booster": 1e20
              },
              "Consume": True,
              "Multis": {
                  "Moon Cash": 10,
                  "Booster": 0.9,
                  "Reincarnation": 0.9
              }
          }, 
          "Booster 2": {
              "Display": "Primary Route Fluctuation",
              "Gradient": "Booster",
              "Reqs": {
                  "Booster": 1e42
              },
              "Consume": True,
              "Multis": {
                  "Moon Cash": 5,
                  "Booster": 3,
                  "Reincarnation": 2,
                  "Scoria": 2
              }
          },
          "Booster 3": {
              "Display": "Planetary Inflation",
              "Gradient": "Booster",
              "Reqs": {
                  "Booster": 1e51
              },
              "Consume": True,
              "Multis": {
                  "Moon Cash": 30,
                  "Booster": 2,
                  "Reincarnation": 0.7,
                  "Scoria": 0.6
              }
          },
          "Booster 4": {
              "Display": "Concussion Totem Lv.1",
              "Gradient": "Booster",
              "Reqs": {
                  "Booster": 1e125
              },
              "Consume": True,
              "Multis": {
                  "Booster": 15
              }
          },
          "Reincarnation 1": {
              "Display": "Better Afterlife",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 200
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 3
                         }
          }, 
          "Reincarnation 2": {
              "Display": "Better Afterlife II",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 50000
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 2,
                         "Reincarnation": 4
              }
          },
          "Reincarnation 3": {
              "Display": "Better Afterlife III",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 1e6
              },
              "Consume": True,
              "Multis": {
                         "Booster": 3,
                         "Reincarnation": 6
            }
          },
          "Reincarnation 4": {
              "Display": "Small Sacrifice",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 4e8
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 0.8,
                         "Scoria": 2.5
               }
          },
          "Reincarnation 5": {
              "Display": "Life Totem Lv.1",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 3e10
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 7,
               }
          },
          "Reincarnation 6": {
              "Display": "Soul Stealer",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 1e15
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 0.5,
                         "Booster": 0.75,
                         "Reincarnation": 8.5
               }
          },
          "Reincarnation 7": {
              "Display": "Aspiring Beam",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 1e50
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 20,
                         "Brighterium": 5,
                         "Baryte": 2
               }
          },
          "Reincarnation 8": {
              "Display": "Mediocre Sacrifice",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 1e56
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 0.5,
                         "Scoria": 5,
                         "Brighterium": 8,
                         "Baryte": 2
               }
          },
          "Reincarnation 9": {
              "Display": "Life Totem Lv.2",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 1e57
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 18
               }
          },
          "Reincarnation 10": {
              "Display": "Father Figure",
              "Gradient": "Reincarnation",
              "Reqs": {
                  "Reincarnation": 1e69
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 20,
                         "Booster": 20,
                         "Reincarnation": 50,
                         "Scoria": 0.3,
                         "Brighterium": 8,
                         "Baryte": 4
               }
          },
          "Scoria 1": {
              "Display": "Excavation Zone Expansion",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 7
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 0.75,
                         "Scoria": 1.5
              }
          },
          "Scoria 2": {
              "Display": "Nuclear Infection",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 45
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 0.25,
                         "Booster": 0.5,
                         "Reincarnation": 1.1,
                         "Scoria": 3.4
              }
          },
          "Scoria 3": {
              "Display": "Even Bigger Mines",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 300
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 0.5,
                         "Scoria": 3
              }
          },
          "Scoria 4": {
              "Display": "Scoria Statue",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 2490
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 2,
                         "Booster": 2,
                         "Scoria": 3.6
              }
          },
          "Scoria 5": {
              "Display": "Scoria Totem Lv.1",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 1e9
              },
              "Consume": True,
              "Multis": {
                         "Scoria": 5
              }
          },
          "Scoria 6": {
              "Display": "Poisonus Talisman",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 3e9
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 1.5,
                         "Booster": 1.2,
                         "Reincarnation": 0.8,
                         "Scoria": 4
              }
          },
          "Scoria 7": {
              "Display": "Erosive Shell",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 1e12
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 3,
                         "Booster": 0.9,
                         "Reincarnation": 2,
                         "Scoria": 6
              }
          },
          "Scoria 8": {
              "Display": "Scoria Totem Lv.2",
              "Gradient": "Scoria",
              "Reqs": {
                  "Scoria": 1e69
              },
              "Consume": True,
              "Multis": {
                         "Scoria": 25
              }
          },
          "Brighterium 1": {
              "Display": "Radiant Manners",
              "Gradient": "Brighterium",
              "Reqs": {
                  "Brighterium": 5
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 8,
                         "Booster": 8,
                         "Reincarnation": 2,
              }
          },
          "Brighterium 2": {
              "Display": "Optic Erosion",
              "Gradient": "Brighterium",
              "Reqs": {
                  "Brighterium": 20
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 4,
                         "Brighterium": 2.5
              }
          },
          "Brighterium 3": {
              "Display": "Visual Bliss",
              "Gradient": "Brighterium",
              "Reqs": {
                  "Brighterium": 260
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 5,
                         "Scoria": 0.9,
                         "Brighterium": 4
              }
          },
          "Brighterium 4": {
              "Display": "Solar Array",
              "Gradient": "Brighterium",
              "Reqs": {
                  "Brighterium": 6000
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 0.7,
                         "Booster": 2,
                         "Reincarnation": 0.5,
                         "Scoria": 3,
                         "Brighterium": 7
              }
          },
          "Brighterium 5": {
              "Display": "Optic Oasis",
              "Gradient": "Brighterium",
              "Reqs": {
                  "Brighterium": 1e45
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 17,
                         "Scoria": 0.4,
                         "Brighterium": 0.4,
                         "Baryte": 3,
                         "Gypsum": 1.2,
                         "Solargems": 0.7
              }
          },
          "Baryte 1": {
              "Display": "Resin Gel",
              "Gradient": "Baryte",
              "Reqs": {
                  "Baryte": 1
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 10,
                         "Booster": 5,
                         "Reincarnation": 9,
                         "Scoria": 0.8,
                         "Brighterium": 0.9,
                         "Baryte": 3
              }
          },
          "Baryte 2": {
              "Display": "Waterfowl Shards",
              "Gradient": "Baryte",
              "Reqs": {
                  "Baryte": 17
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 2,
                         "Booster": 3,
                         "Reincarnation": 2,
                         "Scoria": 4,
                         "Brighterium": 5,
                         "Baryte": 2
              }
          },
          "Baryte 3": {
              "Display": "X-rays",
              "Gradient": "Baryte",
              "Reqs": {
                  "Baryte": 1e9
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 0.75,
                         "Scoria": 3,
                         "Brighterium": 5,
                         "Baryte": 6,
                         "Gypsum": 0.925
              }
          },
          "Gypsum 1": {
              "Display": "Ancient Glyphs",
              "Gradient": "Gypsum",
              "Reqs": {
                  "Gypsum": 20
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 5,
                         "Scoria": 2,
                         "Brighterium": 1.5,
                         "Baryte": 1.2,
                         "Gypsum": 3
              }
          },
          "Gypsum 2": {
              "Display": "Wisp of Wills",
              "Gradient": "Gypsum",
              "Reqs": {
                  "Gypsum": 50
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 100,
                         "Booster": 100,
                         "Reincarnation": 100,
                         "Brighterium": 7.5,
              }
          },
          "Gypsum 3": {
              "Display": "The Zenith",
              "Gradient": "Gypsum",
              "Reqs": {
                  "Gypsum": 777777
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 7,
                         "Booster": 0.7,
                         "Scoria": 0.4,
                         "Brighterium": 12,
                         "Baryte": 3,
                         "Gypsum": 15
              }
          },
          "Solargems 1": {
              "Display": "Solar Chaos",
              "Gradient": "Solargems",
              "Reqs": {
                  "Solargems": 300
              },
              "Consume": True,
              "Multis": {
                         "Booster": 3,
                         "Reincarnation": 6,
                         "Scoria": 5,
                         "Baryte": 0.85,
                         "Solargems": 2
              }
          },
          "Solargems 2": {
              "Display": "Infernal Protrusions",
              "Gradient": "Solargems",
              "Reqs": {
                  "Solargems": 6000
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 2,
                         "Booster": 3,
                         "Reincarnation": 0.8,
                         "Scoria": 10,
                         "Brighterium": 6,
                         "Baryte": 0.72,
                         "Solargems": 1.5
              }
          },
          "Solargems 3": {
              "Display": "Average Star Frequency Increment",
              "Gradient": "Solargems",
              "Reqs": {
                  "Solargems": 15000
              },
              "Consume": True,
              "Multis": {
                         "Scoria": 3,
                         "Brighterium": 4,
                         "Solargems": 2
              }
          },
          "Solargems 4": {
              "Display": "Burning Passion",
              "Gradient": "Solargems",
              "Reqs": {
                  "Solargems": 50000
              },
              "Consume": True,
              "Multis": {
                         "Reincarnation": 0.6,
                         "Scoria": 14,
                         "Brighterium": 9,
                         "Baryte": 0.8,
                         "Solargems": 2
              }
          },
          "Solargems 5": {
              "Display": "Solarium",
              "Gradient": "Solargems",
              "Reqs": {
                  "Solargems": 120000
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 0.05,
                         "Booster": 0.05,
                         "Reincarnation": 30,
                         "Scoria": 20,
                         "Brighterium": 18,
                         "Baryte": 3,
                         "Gypsum": 10,
                         "Solargems": 0.75
              }
          },
          "Pyrite 1": {
              "Display": "Fool's Gold",
              "Gradient": "Pyrite",
              "Reqs": {
                  "Pyrite": 5
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 150,
                         "Booster": 80,
                         "Brighterium": 10,
                         "Pyrite": 2
              }
          },
          "Pyrite 2": {
              "Display": "Cheese Moon",
              "Gradient": "Pyrite",
              "Reqs": {
                  "Pyrite": 333
              },
              "Consume": True,
              "Multis": {
                         "Moon Cash": 200,
                         "Booster": 200,
                         "Scoria": 50,
                         "Brighterium": 3,
                         "Pyrite": 4.5
              }
          },
        },
    "Miscellaneous": 
        {"Test Badge 1": 
            {"Display": "Tester's Glory", 
             "Gradient": "Testium", 
             "Reqs": {
                 "Testium": 1
                 }, 
             "Consume": False,
             "Multis": {"Cash": 1e10}
             },
          "Test Badge 2":
              {"Display": "Tester's Wealth", 
             "Gradient": "Testium", 
             "Reqs": {
                 "Testium": 1
                 }, 
             "Consume": False,
             "Multis": {"Moon Cash": 1e10}
             },
           "Test Badge 3":
              {"Display": "Tester's Memory", 
             "Gradient": "Testium", 
             "Reqs": {
                 "Testium": 1
                 }, 
             "Consume": False,
             "Multis": {"Robuck": 1e10}
             },
            "Test Badge 4":
              {"Display": "Tester's Vacation", 
             "Gradient": "Testium", 
             "Reqs": {
                 "Testium": 1
                 }, 
             "Consume": False,
             "Multis": {"Penny": 1e10}
             },
            "Test Badge 5":
              {"Display": "Tester's i fogor", 
             "Gradient": "Testium", 
             "Reqs": {
                 "Testium": 1
                 }, 
             "Consume": False,
             "Multis": {"Mony": 1e10}
             },   
        }
    }
craftable_items = []
def_upgrades = {
    "Buttonia": {
      "cash_speed": {
        "name": "Cash Speed",
        "max_level": 22,
        "base_cost": 30,
        "cost_growth": 1.05,
        "effect": 1,
        "current_lvl": 0,
        "difficulty": "Easy"
      },
      "gem_speed": {
          "name": "Faster Gems",
          "max_level": 17,
          "base_cost": 60,
          "cost_growth": 1.15,
          "effect": 30,
          "current_lvl": 0,
          "difficulty": "Easy"
      },
      "cash_multi": {
          "name": "Cash Multiplier",
          "max_level": 10,
          "base_cost": 300,
          "cost_growth": 1.2,
          "effect": 0.2,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "gem_timer_amount": {
          "name": "More Gems From Timer",
          "max_level": 36,
          "base_cost": 500,
          "cost_growth": 1.2,
          "effect": 10000,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "lucky_draw": {
          "name": "Lucky Draw [random x100 Cash]",
          "max_level": 100,
          "base_cost": 15000,
          "cost_growth": 1.05,
          "effect": 0.01,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "lucky_draw_multi": {
          "name": "Lucky Multiplier",
          "max_level": 30,
          "base_cost": 100000,
          "cost_growth": 1.2,
          "effect": 1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "geode_speed": {
          "name": "Geode Speed [min 0.25s]",
          "max_level": 25,
          "base_cost": 25000,
          "cost_growth": 1.2,
          "effect": 0.03,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "geode_luck": {
          "name": "Geode Luck [max 2.5x]",
          "max_level": 15,
          "base_cost": 50000,
          "cost_growth": 1.25,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "crit_luck": {
          "name": "Critical Luck [max 2x]",
          "max_level": 20,
          "base_cost": 50000,
          "cost_growth": 1.15,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "event_timer_amount": {
          "name": "More Event Power From Timer",
          "max_level": 800,
          "base_cost": 600000,
          "cost_growth": 1.005,
          "effect": 500,
          "current_lvl": 0,
          "difficulty": "Insane"
      },
      "event_speed": {
          "name": "Faster Event Power From Timer",
          "max_level": 88,
          "base_cost": 250000,
          "cost_growth": 1.1,
          "effect": 1.3,
          "current_lvl": 0,
          "difficulty": "Insane"
      },
      "cash_multi_2": {
          "name": "More Cash Multiplier",
          "max_level": 1000,
          "base_cost": 5e7,
          "cost_growth": 1.01,
          "effect": 0.5,
          "current_lvl": 0,
          "difficulty": "Impossible"
      },
      "super_lucky": {
          "name": "Super Lucky",
          "max_level": 6,
          "base_cost": 6e26,
          "cost_growth": 10,
          "effect": 0.5,
          "current_lvl": 0,
          "difficulty": "Relentless"
      },
      "geode_express": {
          "name": "Geode Express",
          "max_level": 1,
          "base_cost": 1e57,
          "cost_growth": 1,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Unreal"
      },
      "offline_roll": {
          "name": "Offline Geodes",
          "max_level": 1,
          "base_cost": 1e63,
          "cost_growth": 1,
          "current_lvl": 0,
          "difficulty": "Absurd"
      }
    },
    "Afterlife Domain": {
      "cash_speed": {
        "name": "Cash Speed",
        "max_level": 22,
        "base_cost": 30,
        "cost_growth": 1.05,
        "effect": 1,
        "current_lvl": 0,
        "difficulty": "Easy"
      },
      "gem_speed": {
          "name": "Faster Gems",
          "max_level": 17,
          "base_cost": 60,
          "cost_growth": 1.15,
          "effect": 30,
          "current_lvl": 0,
          "difficulty": "Easy"
      },
      "cash_multi": {
          "name": "Cash Multiplier",
          "max_level": 10,
          "base_cost": 300,
          "cost_growth": 1.2,
          "effect": 0.2,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "gem_timer_amount": {
          "name": "More Gems From Timer",
          "max_level": 36,
          "base_cost": 500,
          "cost_growth": 1.2,
          "effect": 10000,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "lucky_draw": {
          "name": "Lucky Draw [random x100 Cash]",
          "max_level": 100,
          "base_cost": 15000,
          "cost_growth": 1.05,
          "effect": 0.01,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "lucky_draw_multi": {
          "name": "Lucky Multiplier",
          "max_level": 30,
          "base_cost": 100000,
          "cost_growth": 1.2,
          "effect": 1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "geode_speed": {
          "name": "Geode Speed [min 0.25s]",
          "max_level": 25,
          "base_cost": 25000,
          "cost_growth": 1.2,
          "effect": 0.03,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "geode_luck": {
          "name": "Geode Luck [max 2.5x]",
          "max_level": 15,
          "base_cost": 50000,
          "cost_growth": 1.25,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "crit_luck": {
          "name": "Critical Luck [max 2x]",
          "max_level": 20,
          "base_cost": 50000,
          "cost_growth": 1.15,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "event_timer_amount": {
          "name": "More Event Power From Timer",
          "max_level": 800,
          "base_cost": 600000,
          "cost_growth": 1.005,
          "effect": 500,
          "current_lvl": 0,
          "difficulty": "Insane"
      },
      "event_speed": {
          "name": "Faster Event Power From Timer",
          "max_level": 88,
          "base_cost": 250000,
          "cost_growth": 1.1,
          "effect": 1.3,
          "current_lvl": 0,
          "difficulty": "Insane"
      },
      "cash_multi_2": {
          "name": "More Cash Multiplier",
          "max_level": 1000,
          "base_cost": 5e7,
          "cost_growth": 1.01,
          "effect": 0.5,
          "current_lvl": 0,
          "difficulty": "Impossible"
      },
      "super_lucky": {
          "name": "Super Lucky",
          "max_level": 6,
          "base_cost": 6e26,
          "cost_growth": 10,
          "effect": 0.5,
          "current_lvl": 0,
          "difficulty": "Relentless"
      },
      "geode_express": {
          "name": "Geode Express",
          "max_level": 1,
          "base_cost": 1e57,
          "cost_growth": 1,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Unreal"
      },
      "offline_roll": {
          "name": "Offline Geodes",
          "max_level": 1,
          "base_cost": 1e63,
          "cost_growth": 1,
          "current_lvl": 0,
          "difficulty": "Absurd"
      }
    },
    "Elysian Stratosphere": {
      "cash_speed": {
        "name": "Cash Speed",
        "max_level": 22,
        "base_cost": 30,
        "cost_growth": 1.05,
        "effect": 1,
        "current_lvl": 0,
        "difficulty": "Easy"
      },
      "gem_speed": {
          "name": "Faster Gems",
          "max_level": 17,
          "base_cost": 60,
          "cost_growth": 1.15,
          "effect": 30,
          "current_lvl": 0,
          "difficulty": "Easy"
      },
      "cash_multi": {
          "name": "Cash Multiplier",
          "max_level": 10,
          "base_cost": 300,
          "cost_growth": 1.2,
          "effect": 0.2,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "gem_timer_amount": {
          "name": "More Gems From Timer",
          "max_level": 36,
          "base_cost": 500,
          "cost_growth": 1.2,
          "effect": 10000,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "lucky_draw": {
          "name": "Lucky Draw [random x100 Cash]",
          "max_level": 100,
          "base_cost": 15000,
          "cost_growth": 1.05,
          "effect": 0.01,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "lucky_draw_multi": {
          "name": "Lucky Multiplier",
          "max_level": 30,
          "base_cost": 100000,
          "cost_growth": 1.2,
          "effect": 1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "geode_speed": {
          "name": "Geode Speed [min 0.25s]",
          "max_level": 25,
          "base_cost": 25000,
          "cost_growth": 1.2,
          "effect": 0.03,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "geode_luck": {
          "name": "Geode Luck [max 2.5x]",
          "max_level": 15,
          "base_cost": 50000,
          "cost_growth": 1.25,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "crit_luck": {
          "name": "Critical Luck [max 2x]",
          "max_level": 20,
          "base_cost": 50000,
          "cost_growth": 1.15,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
      "event_timer_amount": {
          "name": "More Event Power From Timer",
          "max_level": 800,
          "base_cost": 600000,
          "cost_growth": 1.005,
          "effect": 500,
          "current_lvl": 0,
          "difficulty": "Insane"
      },
      "event_speed": {
          "name": "Faster Event Power From Timer",
          "max_level": 88,
          "base_cost": 250000,
          "cost_growth": 1.1,
          "effect": 1.3,
          "current_lvl": 0,
          "difficulty": "Insane"
      },
      "cash_multi_2": {
          "name": "More Cash Multiplier",
          "max_level": 1000,
          "base_cost": 5e7,
          "cost_growth": 1.01,
          "effect": 0.5,
          "current_lvl": 0,
          "difficulty": "Impossible"
      },
      "super_lucky": {
          "name": "Super Lucky",
          "max_level": 6,
          "base_cost": 6e26,
          "cost_growth": 10,
          "effect": 0.5,
          "current_lvl": 0,
          "difficulty": "Relentless"
      },
      "geode_express": {
          "name": "Geode Express",
          "max_level": 1,
          "base_cost": 1e57,
          "cost_growth": 1,
          "effect": 0.1,
          "current_lvl": 0,
          "difficulty": "Unreal"
      },
      "offline_roll": {
          "name": "Offline Geodes",
          "max_level": 1,
          "base_cost": 1e63,
          "cost_growth": 1,
          "current_lvl": 0,
          "difficulty": "Absurd"
      }
    },
    "Moonbase": {
      "mb_cash_speed": {
        "name": "Cash Speed",
        "max_level": 22,
        "base_cost": 30,
        "cost_growth": 1.05,
        "effect": 1,
        "current_lvl": 0,
        "difficulty": "Easy"
      },
      "mb_gem_speed": {
          "name": "Faster Gems",
          "max_level": 17,
          "base_cost": 60,
          "cost_growth": 1.15,
          "effect": 30,
          "current_lvl": 0,
          "difficulty": "Easy"
      },
      "mb_cash_multi": {
          "name": "Cash Multiplier",
          "max_level": 10,
          "base_cost": 300,
          "cost_growth": 1.2,
          "effect": 0.2,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "mb_gem_timer_amount": {
          "name": "More Gems From Timer",
          "max_level": 36,
          "base_cost": 500,
          "cost_growth": 1.2,
          "effect": 10000,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
    },
    "Nostalgia World": {
      "nw_cash_speed": {
        "name": "Cash Speed",
        "max_level": 22,
        "base_cost": 30,
        "cost_growth": 1.05,
        "effect": 1,
        "current_lvl": 0,
        "difficulty": "Easy"
      },
      "nw_gem_speed": {
          "name": "Faster Gems",
          "max_level": 17,
          "base_cost": 60,
          "cost_growth": 1.15,
          "effect": 30,
          "current_lvl": 0,
          "difficulty": "Easy"
      },
      "nw_cash_multi": {
          "name": "Cash Multiplier",
          "max_level": 10,
          "base_cost": 300,
          "cost_growth": 1.2,
          "effect": 0.2,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "nw_gem_timer_amount": {
          "name": "More Gems From Timer",
          "max_level": 36,
          "base_cost": 500,
          "cost_growth": 1.2,
          "effect": 10000,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
    },
    "Secluded Oasis": {
      "so_cash_speed": {
        "name": "Cash Speed",
        "max_level": 22,
        "base_cost": 30,
        "cost_growth": 1.05,
        "effect": 1,
        "current_lvl": 0,
        "difficulty": "Easy"
      },
      "so_gem_speed": {
          "name": "Faster Gems",
          "max_level": 17,
          "base_cost": 60,
          "cost_growth": 1.15,
          "effect": 30,
          "current_lvl": 0,
          "difficulty": "Easy"
      },
      "so_cash_multi": {
          "name": "Cash Multiplier",
          "max_level": 10,
          "base_cost": 300,
          "cost_growth": 1.2,
          "effect": 0.2,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "so_gem_timer_amount": {
          "name": "More Gems From Timer",
          "max_level": 36,
          "base_cost": 500,
          "cost_growth": 1.2,
          "effect": 10000,
          "current_lvl": 0,
          "difficulty": "Hard"
      },
    },
    "The Penumbra of Infinity": {
      "ip_cash_speed": {
        "name": "Upload Speed",
        "max_level": 22,
        "base_cost": 30,
        "cost_growth": 1.05,
        "effect": 1,
        "current_lvl": 0,
        "difficulty": "Easy"
      },
      "ip_gem_speed": {
          "name": "Faster Processing",
          "max_level": 17,
          "base_cost": 60,
          "cost_growth": 1.15,
          "effect": 30,
          "current_lvl": 0,
          "difficulty": "Easy"
      },
      "ip_cash_multi": {
          "name": "Greater Bytes",
          "max_level": 10,
          "base_cost": 300,
          "cost_growth": 1.2,
          "effect": 0.2,
          "current_lvl": 0,
          "difficulty": "Medium"
      },
      "ip_gem_timer_amount": {
          "name": "Greater Processing",
          "max_level": 36,
          "base_cost": 500,
          "cost_growth": 1.2,
          "effect": 10000,
          "current_lvl": 0,
          "difficulty": "Hard"
      }
    }
}
for key, value in abs_stat_info.items():
 for key, value in value.items():
     try:
         value["Recipe"]
         craftable_items.append(key)
     except:
      pass
def_stat_increment = {"Stats": {key: 0 for cat, item in abs_stat_info.items() for g_cat, g_item in (item.items() if cat in ("Geode", "Afterlife Domain (Geode)") else [("", item)]) for key in g_item.keys()}, "Badges": {key: False  for badge in badge_data.values()  for key in badge.keys()}}
abs_stat_info["Exclusive"]["Ivory"] = {"Multis": {item: 1.5 for item in def_stat_increment["Stats"].keys()}}
def_stat_increment["Stats"]["Ivory"] = 0