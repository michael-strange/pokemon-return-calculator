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
17 Double Rare 0.81% (0.19%)
26 Ultra Rare 0.26% (0.11%)
36 Illustration Rare 0.21% (0.1%)
15 Special Illustration Rare 0.21% (0.1%)
9 Hyper Rare 0.2% (0.09%)
'''
double_rare_probability = 0.0081
ultra_rare_probability = 0.0026
illustration_rare_probability = 0.0021
special_illustration_rare_probability = 0.0021
hyper_rare_probability = 0.002

conn = sqlite3.connect("alpha.db")
cur = conn.cursor()

# Create the table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS paldea_evolved_cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    probability REAL NOT NULL,
    price REAL,
    date TEXT)
''')

# Array of cards with id, name, and probability
cards = [
('sv2-5', 'Forretress ex', double_rare_probability),
('sv2-15', 'Meowscarada ex', double_rare_probability),
('sv2-27', 'Wo-Chien ex', double_rare_probability),
('sv2-37', 'Skeledirge ex', double_rare_probability),
('sv2-40', 'Chi-Yu ex', double_rare_probability),
('sv2-52', 'Quaquaval ex', double_rare_probability),
('sv2-61', 'Chien-Pao ex', double_rare_probability),
('sv2-63', 'Pikachu ex', double_rare_probability),
('sv2-79', 'Bellibolt ex', double_rare_probability),
('sv2-86', 'Slowking ex', double_rare_probability),
('sv2-93', 'Dedenne ex', double_rare_probability),
('sv2-117', 'Lycanroc ex', double_rare_probability),
('sv2-127', 'Ting-Lu ex', double_rare_probability),
('sv2-130', 'Paldean Clodsire ex', double_rare_probability),
('sv2-150', 'Copperajah ex', double_rare_probability),
('sv2-153', 'Noivern ex', double_rare_probability),
('sv2-169', 'Squawkabilly ex', double_rare_probability),
('sv2-194', 'Heracross', illustration_rare_probability),
('sv2-195', 'Tropius', illustration_rare_probability),
('sv2-196', 'Sprigatito', illustration_rare_probability),
('sv2-197', 'Floragato', illustration_rare_probability),
('sv2-198', 'Bramblin', illustration_rare_probability),
('sv2-199', 'Fletchinder', illustration_rare_probability),
('sv2-200', 'Pyroar', illustration_rare_probability),
('sv2-201', 'Fuecoco', illustration_rare_probability),
('sv2-202', 'Crocalor', illustration_rare_probability),
('sv2-203', 'Magikarp', illustration_rare_probability),
('sv2-204', 'Marill', illustration_rare_probability),
('sv2-205', 'Eiscue', illustration_rare_probability),
('sv2-206', 'Quaxly', illustration_rare_probability),
('sv2-207', 'Quaxwell', illustration_rare_probability),
('sv2-208', 'Frigibax', illustration_rare_probability),
('sv2-209', 'Arctibax', illustration_rare_probability),
('sv2-210', 'Baxcalibur', illustration_rare_probability),
('sv2-211', 'Raichu', illustration_rare_probability),
('sv2-212', 'Mismagius', illustration_rare_probability),
('sv2-213', 'Gothorita', illustration_rare_probability),
('sv2-214', 'Sandygast', illustration_rare_probability),
('sv2-215', 'Rabsca', illustration_rare_probability),
('sv2-216', 'Tinkatink', illustration_rare_probability),
('sv2-217', 'Tinkatuff', illustration_rare_probability),
('sv2-218', 'Paldean Tauros', illustration_rare_probability),
('sv2-219', 'Sudowoodo', illustration_rare_probability),
('sv2-220', 'Nacli', illustration_rare_probability),
('sv2-221', 'Paldean Wooper', illustration_rare_probability),
('sv2-222', 'Tyranitar', illustration_rare_probability),
('sv2-223', 'Grafaiai', illustration_rare_probability),
('sv2-224', 'Orthworm', illustration_rare_probability),
('sv2-225', 'Rookidee', illustration_rare_probability),
('sv2-226', 'Maushold', illustration_rare_probability),
('sv2-227', 'Flamigo', illustration_rare_probability),
('sv2-228', 'Farigiraf', illustration_rare_probability),
('sv2-229', 'Dudunsparce', illustration_rare_probability),
('sv2-230', 'Forretress ex', ultra_rare_probability),
('sv2-231', 'Meowscarada ex', ultra_rare_probability),
('sv2-232', 'Wo-Chien ex', ultra_rare_probability),
('sv2-233', 'Skeledirge ex', ultra_rare_probability),
('sv2-234', 'Chi-Yu ex', ultra_rare_probability),
('sv2-235', 'Quaquaval ex', ultra_rare_probability),
('sv2-236', 'Chien-Pao ex', ultra_rare_probability),
('sv2-237', 'Bellibolt ex', ultra_rare_probability),
('sv2-238', 'Slowking ex', ultra_rare_probability),
('sv2-239', 'Dedenne ex', ultra_rare_probability),
('sv2-240', 'Tinkaton ex', ultra_rare_probability),
('sv2-241', 'Lycanroc ex', ultra_rare_probability),
('sv2-242', 'Annihilape ex', ultra_rare_probability),
('sv2-243', 'Ting-Lu ex', ultra_rare_probability),
('sv2-244', 'Paldean Clodsire ex', ultra_rare_probability),
('sv2-245', 'Copperajah ex', ultra_rare_probability),
('sv2-246', 'Noivern ex', ultra_rare_probability),
('sv2-247', 'Squawkabilly ex', ultra_rare_probability),
('sv2-248', 'Boss\'s Orders (Ghetsis)', ultra_rare_probability),
('sv2-249', 'Clavell', ultra_rare_probability),
('sv2-250', 'Dendra', ultra_rare_probability),
('sv2-251', 'Falkner', ultra_rare_probability),
('sv2-252', 'Giacomo', ultra_rare_probability),
('sv2-253', 'Grusha', ultra_rare_probability),
('sv2-254', 'Iono', ultra_rare_probability),
('sv2-255', 'Saguaro', ultra_rare_probability),
('sv2-256', 'Meowscarada ex', special_illustration_rare_probability),
('sv2-257', 'Wo-Chien ex', special_illustration_rare_probability),
('sv2-258', 'Skeledirge ex', special_illustration_rare_probability),
('sv2-259', 'Chi-Yu ex', special_illustration_rare_probability),
('sv2-260', 'Quaquaval ex', special_illustration_rare_probability),
('sv2-261', 'Chien-Pao ex', special_illustration_rare_probability),
('sv2-262', 'Tinkaton ex', special_illustration_rare_probability),
('sv2-263', 'Ting-Lu ex', special_illustration_rare_probability),
('sv2-264', 'Squawkabilly ex', special_illustration_rare_probability),
('sv2-265', 'Boss\'s Orders (Ghetsis)', special_illustration_rare_probability),
('sv2-266', 'Dendra', special_illustration_rare_probability),
('sv2-267', 'Giacomo', special_illustration_rare_probability),
('sv2-268', 'Grusha', special_illustration_rare_probability),
('sv2-269', 'Iono', special_illustration_rare_probability),
('sv2-270', 'Saguaro', special_illustration_rare_probability),
('sv2-271', 'Meowscarada ex', hyper_rare_probability),
('sv2-272', 'Skeledirge ex', hyper_rare_probability),
('sv2-273', 'Quaquaval ex', hyper_rare_probability),
('sv2-274', 'Chien-Pao ex', hyper_rare_probability),
('sv2-275', 'Ting-Lu ex', hyper_rare_probability),
('sv2-276', 'Super Rod', hyper_rare_probability),
('sv2-277', 'Superior Energy Retrieval', hyper_rare_probability),
('sv2-278', 'Basic Grass Energy', hyper_rare_probability),
('sv2-279', 'Basic Water Energy', hyper_rare_probability),

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
    cur.execute('SELECT date FROM paldea_evolved_cards WHERE card_id = ?', (card_id,))
    result = cur.fetchone()

    if result and result[0] == current_date:
        continue  # Skip update if the card is already updated today

    # Retrieve the current price
    current_price = get_current_price(card_id)

    # Update or insert card information
    cur.execute('''
    INSERT INTO paldea_evolved_cards (card_id, card_name, probability, price, date)
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
    cur.execute('SELECT price, probability FROM paldea_evolved_cards')
    paldea_evolved_cards = cur.fetchall()

    # Calculate the total value
    for price, probability in paldea_evolved_cards:
        total_value += price * probability

    # Close the database connection
    conn.commit()
    conn.close()

    return total_value


# Example usage of the function

