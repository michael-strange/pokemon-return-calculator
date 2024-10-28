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
14 Double Rare 1.21% (0.23%)
21 Ultra Rare 0.31% (0.12%)
6 ACE SPEC rare 0.84% (0.19%)
21 Illustration Rare 0.37% (0.13%)
11 Special Illustration Rare 0.11% (0.07%)
6 Hyper Rare 0.11% (0.17%)
'''
double_rare_probability = 0.0121
ultra_rare_probability = 0.0031
ace_spec_rare_probability = 0.0084
illustration_rare_probability = 0.0037
special_illustration_rare_probability = 0.0011
hyper_rare_probability = 0.0011

conn = sqlite3.connect("alpha.db")
cur = conn.cursor()

# Create the table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS twilight_masquerade_cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    probability REAL NOT NULL,
    price REAL,
    date TEXT)
''')

# Array of cards with id, name, and probability
cards = [
('sv6-23', 'Sinistcha ex', double_rare_probability),
('sv6-25', 'Teal Mask Ogerpon ex', double_rare_probability),
('sv6-29', 'Magcargo ex', double_rare_probability),
('sv6-40', 'Hearthflame Mask Ogerpon ex', double_rare_probability),
('sv6-61', 'Palafin ex', double_rare_probability),
('sv6-64', 'Wellspring Mask Ogerpon ex', double_rare_probability),
('sv6-68', 'Luxray ex', double_rare_probability),
('sv6-77', 'Iron Thorns ex', double_rare_probability),
('sv6-94', 'Scream Tail ex', double_rare_probability),
('sv6-106', 'Greninja ex', double_rare_probability),
('sv6-112', 'Cornerstone Mask Ogerpon ex', double_rare_probability),
('sv6-130', 'Dragapult ex', double_rare_probability),
('sv6-134', 'Blissey ex', double_rare_probability),
('sv6-141', 'Bloodmoon Ursaluna ex', double_rare_probability),
('sv6-152', 'Hyper Aroma', ace_spec_rare_probability),
('sv6-162', 'Scoop Up Cyclone', ace_spec_rare_probability),
('sv6-163', 'Secret Box', ace_spec_rare_probability),
('sv6-164', 'Survival Brace', ace_spec_rare_probability),
('sv6-165', 'Unfair Stamp', ace_spec_rare_probability),
('sv6-167', 'Legacy Energy', ace_spec_rare_probability),
('sv6-168', 'Pinsir', illustration_rare_probability),
('sv6-169', 'Sunflora', illustration_rare_probability),
('sv6-170', 'Dipplin', illustration_rare_probability),
('sv6-171', 'Poltchageist', illustration_rare_probability),
('sv6-172', 'Torkoal', illustration_rare_probability),
('sv6-173', 'Infernape', illustration_rare_probability),
('sv6-174', 'Froslass', illustration_rare_probability),
('sv6-175', 'Phione', illustration_rare_probability),
('sv6-176', 'Cramorant', illustration_rare_probability),
('sv6-177', 'Heliolisk', illustration_rare_probability),
('sv6-178', 'Wattrel', illustration_rare_probability),
('sv6-179', 'Chimecho', illustration_rare_probability),
('sv6-180', 'Enamorus', illustration_rare_probability),
('sv6-181', 'Hisuian Growlithe', illustration_rare_probability),
('sv6-182', 'Probopass', illustration_rare_probability),
('sv6-183', 'Timburr', illustration_rare_probability),
('sv6-184', 'Lairon', illustration_rare_probability),
('sv6-185', 'Applin', illustration_rare_probability),
('sv6-186', 'Tatsugiri', illustration_rare_probability),
('sv6-187', 'Chansey', illustration_rare_probability),
('sv6-188', 'Eevee', illustration_rare_probability),
('sv6-189', 'Sinistcha ex', ultra_rare_probability),
('sv6-190', 'Teal Mask Ogerpon ex', ultra_rare_probability),
('sv6-191', 'Magcargo ex', ultra_rare_probability),
('sv6-192', 'Hearthflame Mask Ogerpon ex', ultra_rare_probability),
('sv6-193', 'Palafin ex', ultra_rare_probability),
('sv6-194', 'Wellspring Mask Ogerpon ex', ultra_rare_probability),
('sv6-195', 'Luxray ex', ultra_rare_probability),
('sv6-196', 'Iron Thorns ex', ultra_rare_probability),
('sv6-197', 'Scream Tail ex', ultra_rare_probability),
('sv6-198', 'Greninja ex', ultra_rare_probability),
('sv6-199', 'Cornerstone Mask Ogerpon ex', ultra_rare_probability),
('sv6-200', 'Dragapult ex', ultra_rare_probability),
('sv6-201', 'Blissey ex', ultra_rare_probability),
('sv6-202', 'Bloodmoon Ursaluna ex', ultra_rare_probability),
('sv6-203', 'Caretaker', ultra_rare_probability),
('sv6-204', 'Carmine', ultra_rare_probability),
('sv6-205', 'Hassel', ultra_rare_probability),
('sv6-206', 'Kieran', ultra_rare_probability),
('sv6-207', 'Lana\'s Aid', ultra_rare_probability),
('sv6-208', 'Lucian', ultra_rare_probability),
('sv6-209', 'Perrin', ultra_rare_probability),
('sv6-210', 'Sinistcha ex', special_illustration_rare_probability),
('sv6-211', 'Teal Mask Ogerpon ex', special_illustration_rare_probability),
('sv6-212', 'Hearthflame Mask Ogerpon ex', special_illustration_rare_probability),
('sv6-213', 'Wellspring Mask Ogerpon ex', special_illustration_rare_probability),
('sv6-214', 'Greninja ex', special_illustration_rare_probability),
('sv6-215', 'Cornerstone Mask Ogerpon ex', special_illustration_rare_probability),
('sv6-216', 'Bloodmoon Ursaluna ex', special_illustration_rare_probability),
('sv6-217', 'Carmine', special_illustration_rare_probability),
('sv6-218', 'Kieran', special_illustration_rare_probability),
('sv6-219', 'Lana\'s Aid', special_illustration_rare_probability),
('sv6-220', 'Perrin', special_illustration_rare_probability),
('sv6-221', 'Teal Mask Ogerpon ex', hyper_rare_probability),
('sv6-222', 'Bloodmoon Ursaluna ex', hyper_rare_probability),
('sv6-223', 'Buddy-Buddy Poffin', hyper_rare_probability),
('sv6-224', 'Enhanced Hammer', hyper_rare_probability),
('sv6-225', 'Rescue Board', hyper_rare_probability),
('sv6-226', 'Luminous Energy', hyper_rare_probability),
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
    cur.execute('SELECT date FROM twilight_masquerade_cards WHERE card_id = ?', (card_id,))
    result = cur.fetchone()

    if result and result[0] == current_date:
        continue  # Skip update if the card is already updated today

    # Retrieve the current price
    current_price = get_current_price(card_id)

    # Update or insert card information
    cur.execute('''
    INSERT INTO twilight_masquerade_cards (card_id, card_name, probability, price, date)
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
    cur.execute('SELECT price, probability FROM twilight_masquerade_cards')
    twilight_masquerade_cards = cur.fetchall()

    # Calculate the total value
    for price, probability in twilight_masquerade_cards:
        total_value += price * probability

    # Close the database connection
    conn.commit()
    conn.close()

    return total_value


# Example usage of the function

