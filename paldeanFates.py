import time

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pokemontcgsdk import RestClient
import json
from datetime import datetime
import os
import sqlite3


'''
PROBABILITIES
COUNT and RARITY with PULL RATE (95% CONFIDENCE INTERVAL)
10 Double Rare - 1.59% (0.58%) DONE
5 Ultra Rare - 1.32% (0.53%) DONE
120 Shiny Rare - 0.21% (0.21%)
12 Shiny Ultra Rare - 0.64% (0.37%) DONE
3 Illustration Rare - 2.41% (0.71%)
8 Special Illustration Rare - 0.22% (0.21%)
6 Hyper Rare - 0.27% (0.24%)
'''

conn = sqlite3.connect("alpha.db")
cur = conn.cursor()

# Create the table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS paldean_fates_cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    probability REAL NOT NULL,
    price REAL,
    date TEXT)
''')

# Array of cards with id, name, and probability
cards = [
    #Double Rares (10)
    ('sv4pt5-2', 'Forretress ex', 0.0159),
    ('sv4pt5-5', 'Toedscruel ex', 0.0159),
    ('sv4pt5-6', 'Espathra ex', 0.0159),
    ('sv4pt5-29', 'Gardevoir ex', 0.0159),
    ('sv4pt5-53', 'Great Tusk ex', 0.0159),
    ('sv4pt5-54', 'Charizard ex', 0.0159),
    ('sv4pt5-59', 'Pladean Clodsire ex', 0.0159),
    ('sv4pt5-66', 'Iron Treads ex', 0.0159),
    ('sv4pt5-69', 'Noivern ex', 0.0159),
    ('sv4pt5-75', 'Squawkabilly ex', 0.0159),

    #Ultra Rare (5)
    ('sv4pt5-227', 'Clive', 0.0132),
    ('sv4pt5-228', 'Judge', 0.0132),
    ('sv4pt5-229', 'Nemona', 0.0132),
    ('sv4pt5-230', 'Paldean Student', 0.0132),
    ('sv4pt5-231', 'Paldean Student', 0.0132),

    #Shiny Ultra Rare (12)
    ('sv4pt5-212', 'Forretress ex', 0.0064),
    ('sv4pt5-213', 'Toedscruel ex', 0.0064),
    ('sv4pt5-214', 'Espathra ex', 0.0064),
    ('sv4pt5-215', 'Alakazam ex', 0.0064),
    ('sv4pt5-216', 'Mew ex', 0.0064),
    ('sv4pt5-217', 'Gardevoir ex', 0.0064),
    ('sv4pt5-218', 'Glimorra ex', 0.0064),
    ('sv4pt5-219', 'Paldean Clodsire ex', 0.0064),
    ('sv4pt5-220', 'Noivern ex', 0.0064),
    ('sv4pt5-221', 'Pidgeotto ex', 0.0064),
    ('sv4pt5-222', 'Wigglytuff ex', 0.0064),
    ('sv4pt5-223', 'Squawkabilly ex', 0.0064),

    #Illustration Rare (3)
    ('sv4pt5-224', 'Wugtrio', 0.0241),
    ('sv4pt5-225', 'Palafin', 0.0241),
    ('sv4pt5-226', 'Pawmi', 0.0241),

    #Special Illustration Rare (8)
    ('sv4pt5-232', 'Mew ex', 0.0022),
    ('sv4pt5-233', 'Gardevoir ex', 0.0022),
    ('sv4pt5-234', 'Charizard ex', 0.0022),
    ('sv4pt5-235', 'Arven', 0.0022),
    ('sv4pt5-236', 'Clive', 0.0022),
    ('sv4pt5-237', 'Iono', 0.0022),
    ('sv4pt5-238', 'Nemona', 0.0022),
    ('sv4pt5-239', 'Penny', 0.0022),

    #Hyper Rare (6)
    ('sv4pt5-240', 'Wo-Chien ex', 0.0027),
    ('sv4pt5-241', 'Chi-Yu ex', 0.0027),
    ('sv4pt5-242', 'Chien-Pao ex', 0.0027),
    ('sv4pt5-243', 'Miraidon ex', 0.0027),
    ('sv4pt5-244', 'Ting-Lu ex', 0.0027),
    ('sv4pt5-245', 'Koraiden ex', 0.0027),

    #Shiny Rare (120)
    ('sv4pt5-92', 'Oddish', 0.0021),
    ('sv4pt5-93', 'Gloom', 0.0021),
    ('sv4pt5-94', 'Vileplume', 0.0021),
    ('sv4pt5-95', 'Scyther', 0.0021),
    ('sv4pt5-96', 'Hoppip', 0.0021),
    ('sv4pt5-97', 'Skiploom', 0.0021),
    ('sv4pt5-98', 'Jumpluff', 0.0021),
    ('sv4pt5-99', 'Pineco', 0.0021),
    ('sv4pt5-100', 'Snover', 0.0021),
    ('sv4pt5-101', 'Abomasnow', 0.0021),
    ('sv4pt5-102', 'Smoliv', 0.0021),
    ('sv4pt5-103', 'Dolliv', 0.0021),
    ('sv4pt5-104', 'Arboliva', 0.0021),
    ('sv4pt5-105', 'Toedscool', 0.0021),
    ('sv4pt5-106', 'Capsakid', 0.0021),
    ('sv4pt5-107', 'Scovillain', 0.0021),
    ('sv4pt5-108', 'Rellor', 0.0021),
    ('sv4pt5-109', 'Charmander', 0.0021),
    ('sv4pt5-110', 'Charmeleon', 0.0021),
    ('sv4pt5-111', 'Paldean Tauros', 0.0021),
    ('sv4pt5-112', 'Entei', 0.0021),
    ('sv4pt5-113', 'Oricorio', 0.0021),
    ('sv4pt5-114', 'Charcadet', 0.0021),
    ('sv4pt5-115', 'Armarouge', 0.0021),
    ('sv4pt5-116', 'Slowpoke', 0.0021),
    ('sv4pt5-117', 'Slowbro', 0.0021),
    ('sv4pt5-118', 'Staryu', 0.0021),
    ('sv4pt5-119', 'Starmie', 0.0021),
    ('sv4pt5-120', 'Paldean Tauros', 0.0021),
    ('sv4pt5-121', 'Wiglett', 0.0021),
    ('sv4pt5-122', 'Wugtrio', 0.0021),
    ('sv4pt5-123', 'Finizen', 0.0021),
    ('sv4pt5-124', 'Palafin', 0.0021),
    ('sv4pt5-125', 'Veluza', 0.0021),
    ('sv4pt5-126', 'Dondozo', 0.0021),
    ('sv4pt5-127', 'Tatsugiri', 0.0021),
    ('sv4pt5-128', 'Frigibax', 0.0021),
    ('sv4pt5-129', 'Arctibax', 0.0021),
    ('sv4pt5-130', 'Baxcalibur', 0.0021),
    ('sv4pt5-131', 'Pikachu', 0.0021),
    ('sv4pt5-132', 'Raichu', 0.0021),
    ('sv4pt5-133', 'Voltorb', 0.0021),
    ('sv4pt5-134', 'Electrode', 0.0021),
    ('sv4pt5-135', 'Shinx', 0.0021),
    ('sv4pt5-136', 'Luxio', 0.0021),
    ('sv4pt5-137', 'Luxray', 0.0021),
    ('sv4pt5-138', 'Pachirisu', 0.0021),
    ('sv4pt5-139', 'Thundurus', 0.0021),
    ('sv4pt5-140', 'Toxel', 0.0021),
    ('sv4pt5-141', 'Toxtricity', 0.0021),
    ('sv4pt5-142', 'Pawmi', 0.0021),
    ('sv4pt5-143', 'Pawmo', 0.0021),
    ('sv4pt5-144', 'Pawmot', 0.0021),
    ('sv4pt5-145', 'Wattrel', 0.0021),
    ('sv4pt5-146', 'Kilowattrel', 0.0021),
    ('sv4pt5-147', 'Wigglytuff', 0.0021),
    ('sv4pt5-148', 'Abra', 0.0021),
    ('sv4pt5-149', 'Kadabra', 0.0021),
    ('sv4pt5-150', 'Cleffa', 0.0021),
    ('sv4pt5-151', 'Natu', 0.0021),
    ('sv4pt5-152', 'Xatu', 0.0021),
    ('sv4pt5-153', 'Ralts', 0.0021),
    ('sv4pt5-154', 'Kirlia', 0.0021),
    ('sv4pt5-155', 'Drifloon', 0.0021),
    ('sv4pt5-156', 'Drifblim', 0.0021),
    ('sv4pt5-157', 'Mime Jr.', 0.0021),
    ('sv4pt5-158', 'Spiritomb', 0.0021),
    ('sv4pt5-159', 'Klefki', 0.0021),
    ('sv4pt5-160', 'Mimikyu', 0.0021),
    ('sv4pt5-161', 'Dachsbun', 0.0021),
    ('sv4pt5-162', 'Ceruledge', 0.0021),
    ('sv4pt5-163', 'Rabsca', 0.0021),
    ('sv4pt5-164', 'Flittle', 0.0021),
    ('sv4pt5-165', 'Tinkatink', 0.0021),
    ('sv4pt5-166', 'Tinkatuff', 0.0021),
    ('sv4pt5-167', 'Tinkaton', 0.0021),
    ('sv4pt5-168', 'Houndstone', 0.0021),
    ('sv4pt5-169', 'Mankey', 0.0021),
    ('sv4pt5-170', 'Primeape', 0.0021),
    ('sv4pt5-171', 'Annihilape', 0.0021),
    ('sv4pt5-172', 'Paldean Tauros', 0.0021),
    ('sv4pt5-173', 'Riolu', 0.0021),
    ('sv4pt5-174', 'Lucario', 0.0021),
    ('sv4pt5-175', 'Hawlucha', 0.0021),
    ('sv4pt5-176', 'Nacli', 0.0021),
    ('sv4pt5-177', 'Naclstack', 0.0021),
    ('sv4pt5-178', 'Garganacl', 0.0021),
    ('sv4pt5-179', 'Glimmet', 0.0021),
    ('sv4pt5-180', 'Paldean Wooper', 0.0021),
    ('sv4pt5-181', 'Murkrow', 0.0021),
    ('sv4pt5-182', 'Sneasel', 0.0021),
    ('sv4pt5-183', 'Weavile', 0.0021),
    ('sv4pt5-184', 'Sableye', 0.0021),
    ('sv4pt5-185', 'Pawniard', 0.0021),
    ('sv4pt5-186', 'Bisharp', 0.0021),
    ('sv4pt5-187', 'Kingambit', 0.0021),
    ('sv4pt5-188', 'Mabosstiff', 0.0021),
    ('sv4pt5-189', 'Shroodle', 0.0021),
    ('sv4pt5-190', 'Grafaiai', 0.0021),
    ('sv4pt5-191', 'Scizor', 0.0021),
    ('sv4pt5-192', 'Varoom', 0.0021),
    ('sv4pt5-193', 'Revavroom', 0.0021),
    ('sv4pt5-194', 'Noibat', 0.0021),
    ('sv4pt5-195', 'Cyclizar', 0.0021),
    ('sv4pt5-196', 'Pidgey', 0.0021),
    ('sv4pt5-197', 'Pidgeotto', 0.0021),
    ('sv4pt5-198', 'Jigglypuff', 0.0021),
    ('sv4pt5-199', 'Doduo', 0.0021),
    ('sv4pt5-200', 'Dodrio', 0.0021),
    ('sv4pt5-201', 'Ditto', 0.0021),
    ('sv4pt5-202', 'Snorlax', 0.0021),
    ('sv4pt5-203', 'Wingull', 0.0021),
    ('sv4pt5-204', 'Pelipper', 0.0021),
    ('sv4pt5-205', 'Skwovet', 0.0021),
    ('sv4pt5-206', 'Greedent', 0.0021),
    ('sv4pt5-207', 'Lechonk', 0.0021),
    ('sv4pt5-208', 'Oinkologne', 0.0021),
    ('sv4pt5-209', 'Tandemaus', 0.0021),
    ('sv4pt5-210', 'Maushold', 0.0021),
    ('sv4pt5-211', 'Flamigo', 0.0021)
]

# Function to get the current price from an API
def get_current_price(card_id):
    print('Getting price for', card_id)
    cardItem = Card.find(card_id)

    try:
        # Try to access the tcgplayer price
        price = cardItem.tcgplayer.prices.holofoil.market
    except AttributeError:
        # If it fails, fallback to the cardmarket price
        print("Using cardmarket price for", card_id)
        price = (cardItem.cardmarket.prices.avg7 * 1.08)

    time.sleep(0.5)

    return price

# Current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Check each card and update or insert data
for card_id, card_name, probability in cards:
    # Check if the card exists and the date is not today
    cur.execute('SELECT date FROM paldean_fates_cards WHERE card_id = ?', (card_id,))
    result = cur.fetchone()

    if result and result[0] == current_date:
        continue  # Skip update if the card is already updated today

    # Retrieve the current price
    current_price = get_current_price(card_id)

    # Update or insert card information
    cur.execute('''
    INSERT INTO paldean_fates_cards (card_id, card_name, probability, price, date)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(card_id) DO UPDATE SET
    card_name = excluded.card_name,
    probability = excluded.probability,
    price = excluded.price,
    date = excluded.date
    ''', (card_id, card_name, probability, current_price, current_date))
    conn.commit()

# Commit changes and close the connection
def get_value():
    # Initialize the total value
    total_value = 0.0

    # Retrieve price and probability for all cards
    cur.execute('SELECT price, probability FROM paldean_fates_cards')
    paldean_fates_cards = cur.fetchall()

    # Calculate the total value
    for price, probability in paldean_fates_cards:
        total_value += price * probability

    # Close the database connection
    conn.commit()
    conn.close()

    return total_value


# Example usage of the function
