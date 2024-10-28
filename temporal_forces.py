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
15 Double Rare 1.12% (0.22%)
18 Ultra Rare 0.37% (0.13%)
7 ACE SPEC 0.71% (0.18%)
22 Illustration Rare 0.35% (0.12%)
10 Special Illustration Rare 0.12% (0.07%)
6 Hyper Rare 0.12% (0.07%)
'''
double_rare_probability = 0.012
ultra_rare_probability = 0.0037
ace_spec_rare_probability = 0.0071
illustration_rare_probability = 0.0035
special_illustration_rare_probability = 0.0012
hyper_rare_probability = 0.0012

conn = sqlite3.connect("alpha.db")
cur = conn.cursor()

# Create the table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS temporal_forces_cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    probability REAL NOT NULL,
    price REAL,
    date TEXT)
''')

# Array of cards with id, name, and probability
cards = [
    ('sv5-12', 'Torterra ex', double_rare_probability),
    ('sv5-22', 'Scovillain ex', double_rare_probability),
    ('sv5-25', 'Iron Leaves ex', double_rare_probability),
    ('sv5-34', 'Incineroar ex', double_rare_probability),
    ('sv5-38', 'Gouging Fire ex', double_rare_probability),
    ('sv5-50', 'Walking Wake ex', double_rare_probability),
    ('sv5-60', 'Wugtrio ex', double_rare_probability),
    ('sv5-81', 'Iron Crown ex', double_rare_probability),
    ('sv5-99', 'Iron Boulder ex', double_rare_probability),
    ('sv5-104', 'Gengar ex', double_rare_probability),
    ('sv5-108', 'Farigiraf ex', double_rare_probability),
    ('sv5-111', 'Scizor ex', double_rare_probability),
    ('sv5-120', 'Koraidon ex', double_rare_probability),
    ('sv5-122', 'Miraidon ex', double_rare_probability),
    ('sv5-123', 'Raging Bolt ex', double_rare_probability),
    ('sv5-141', 'Awakening Drum', ace_spec_rare_probability),
    ('sv5-152', 'Hero\'s Cape', ace_spec_rare_probability),
    ('sv5-153', 'Master Ball', ace_spec_rare_probability),
    ('sv5-154', 'Maximum Belt', ace_spec_rare_probability),
    ('sv5-157', 'Prime Catcher', ace_spec_rare_probability),
    ('sv5-158', 'Reboot Pod', ace_spec_rare_probability),
    ('sv5-162', 'Neo Upper Energy', ace_spec_rare_probability),
    ('sv5-163', 'Shiftry', illustration_rare_probability),
    ('sv5-164', 'Grotle', illustration_rare_probability),
    ('sv5-165', 'Deerling', illustration_rare_probability),
    ('sv5-166', 'Sawsbuck', illustration_rare_probability),
    ('sv5-167', 'Litten', illustration_rare_probability),
    ('sv5-168', 'Snom', illustration_rare_probability),
    ('sv5-169', 'Charjabug', illustration_rare_probability),
    ('sv5-170', 'Bronzor', illustration_rare_probability),
    ('sv5-171', 'Reuniclus', illustration_rare_probability),
    ('sv5-172', 'Cutiefly', illustration_rare_probability),
    ('sv5-173', 'Relicanth', illustration_rare_probability),
    ('sv5-174', 'Excadrill', illustration_rare_probability),
    ('sv5-175', 'Mudsdale', illustration_rare_probability),
    ('sv5-176', 'Arbok', illustration_rare_probability),
    ('sv5-177', 'Gastly', illustration_rare_probability),
    ('sv5-178', 'Metagross', illustration_rare_probability),
    ('sv5-179', 'Meltan', illustration_rare_probability),
    ('sv5-180', 'Lickitung', illustration_rare_probability),
    ('sv5-181', 'Chatot', illustration_rare_probability),
    ('sv5-182', 'Minccino', illustration_rare_probability),
    ('sv5-183', 'Cinccino', illustration_rare_probability),
    ('sv5-184', 'Drampa', illustration_rare_probability),
    ('sv5-185', 'Torterra ex', ultra_rare_probability),
    ('sv5-186', 'Iron Leaves ex', ultra_rare_probability),
    ('sv5-187', 'Incineroar ex', ultra_rare_probability),
    ('sv5-188', 'Gouging Fire ex', ultra_rare_probability),
    ('sv5-189', 'Walking Wake ex', ultra_rare_probability),
    ('sv5-190', 'Wugtrio ex', ultra_rare_probability),
    ('sv5-191', 'Iron Crown ex', ultra_rare_probability),
    ('sv5-192', 'Iron Boulder ex', ultra_rare_probability),
    ('sv5-193', 'Gengar ex', ultra_rare_probability),
    ('sv5-194', 'Farigiraf ex', ultra_rare_probability),
    ('sv5-195', 'Scizor ex', ultra_rare_probability),
    ('sv5-196', 'Raging Bolt ex', ultra_rare_probability),
    ('sv5-197', 'Bianca\'s Devotion', ultra_rare_probability),
    ('sv5-198', 'Ciphermaniac\'s Codebreaking', ultra_rare_probability),
    ('sv5-199', 'Eri', ultra_rare_probability),
    ('sv5-200', 'Explorer\'s Guidance', ultra_rare_probability),
    ('sv5-201', 'Morty\'s Conviction', ultra_rare_probability),
    ('sv5-202', 'Salvatore', ultra_rare_probability),
    ('sv5-203', 'Iron Leaves ex', special_illustration_rare_probability),
    ('sv5-204', 'Gouging Fire ex', special_illustration_rare_probability),
    ('sv5-205', 'Walking Wake ex', special_illustration_rare_probability),
    ('sv5-206', 'Iron Crown ex', special_illustration_rare_probability),
    ('sv5-207', 'Iron Boulder ex', special_illustration_rare_probability),
    ('sv5-208', 'Raging Bolt ex', special_illustration_rare_probability),
    ('sv5-209', 'Bianca\'s Devotion', special_illustration_rare_probability),
    ('sv5-210', 'Eri', special_illustration_rare_probability),
    ('sv5-211', 'Morty\'s Conviction', special_illustration_rare_probability),
    ('sv5-212', 'Salvatore', special_illustration_rare_probability),
    ('sv5-213', 'Iron Leaves ex', hyper_rare_probability),
    ('sv5-214', 'Gouging Fire ex', hyper_rare_probability),
    ('sv5-215', 'Walking Wake ex', hyper_rare_probability),
    ('sv5-216', 'Iron Crown ex', hyper_rare_probability),
    ('sv5-217', 'Iron Boulder ex', hyper_rare_probability),
    ('sv5-218', 'Raging Bolt ex', hyper_rare_probability),
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
    cur.execute('SELECT date FROM temporal_forces_cards WHERE card_id = ?', (card_id,))
    result = cur.fetchone()

    if result and result[0] == current_date:
        continue  # Skip update if the card is already updated today

    # Retrieve the current price
    current_price = get_current_price(card_id)

    # Update or insert card information
    cur.execute('''
    INSERT INTO temporal_forces_cards (card_id, card_name, probability, price, date)
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
    cur.execute('SELECT price, probability FROM temporal_forces_cards')
    temporal_forces_cards = cur.fetchall()

    # Calculate the total value
    for price, probability in temporal_forces_cards:
        total_value += price * probability

    # Close the database connection
    conn.commit()
    conn.close()

    return total_value


# Example usage of the function

