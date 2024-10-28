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
20 Double Rare 0.78% (0.19%)
28 Ultra Rare 0.24% (0.1%)
34 Illustration Rare 0.23% (0.1%)
15 Special Illustration Rare 0.14% (0.08%)
7 Hyper Rare 0.17% (0.09%)
'''
double_rare_probability = 0.0078
ultra_rare_probability = 0.0024
illustration_rare_probability = 0.0023
special_illustration_rare_probability = 0.0014
hyper_rare_probability = 0.0017

conn = sqlite3.connect("alpha.db")
cur = conn.cursor()

# Create the table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS paradox_rift_cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    probability REAL NOT NULL,
    price REAL,
    date TEXT)
''')

# Array of cards with id, name, and probability
cards = [
('sv4-3', 'Froslass ex', double_rare_probability),
('sv4-27', 'Armarouge ex', double_rare_probability),
('sv4-38', 'Garchomp ex', double_rare_probability),
('sv4-68', 'Tapu Koko ex', double_rare_probability),
('sv4-70', 'Iron Hands ex', double_rare_probability),
('sv4-46', 'Tsareena ex', double_rare_probability),
('sv4-50', 'Golisopod ex', double_rare_probability),
('sv4-58', 'Mewtwo ex', double_rare_probability),
('sv4-76', 'Cofagrigus ex', double_rare_probability),
('sv4-100', 'Toxtricity ex', double_rare_probability),
('sv4-108', 'Sandy Shocks ex', double_rare_probability),
('sv4-89', 'Iron Valiant ex', double_rare_probability),
('sv4-98', 'Hoopa ex', double_rare_probability),
('sv4-124', 'Roaring Moon ex', double_rare_probability),
('sv4-135', 'Aegislash ex', double_rare_probability),
('sv4-137', 'Skeledirge ex', double_rare_probability),
('sv4-139', 'Gholdengo ex', double_rare_probability),
('sv4-140', 'Altaria ex', double_rare_probability),
('sv4-155', 'Maushold ex', double_rare_probability),
('sv4-156', 'Bombirdier ex', double_rare_probability),
('sv4-183', 'Crustle', illustration_rare_probability),
('sv4-184', 'Dottler', illustration_rare_probability),
('sv4-186', 'Magby', illustration_rare_probability),
('sv4-190', 'Vanillish', illustration_rare_probability),
('sv4-185', 'Toedscruel', illustration_rare_probability),
('sv4-187', 'Iron Moth', illustration_rare_probability),
('sv4-189', 'Mantyke', illustration_rare_probability),
('sv4-191', 'Wimpod', illustration_rare_probability),
('sv4-193', 'Plusle', illustration_rare_probability),
('sv4-188', 'Snorunt', illustration_rare_probability),
('sv4-194', 'Minun', illustration_rare_probability),
('sv4-192', 'Veluza', illustration_rare_probability),
('sv4-197', 'Espathra', illustration_rare_probability),
('sv4-203', 'Slither Wing', illustration_rare_probability),
('sv4-213', 'Swablu', illustration_rare_probability),
('sv4-218', 'Armarouge ex', ultra_rare_probability),
('sv4-216', 'Iron Jugulis', illustration_rare_probability),
('sv4-226', 'Hoopa ex', ultra_rare_probability),
('sv4-220', 'Tsareena ex', ultra_rare_probability),
('sv4-227', 'Toxtricity ex', ultra_rare_probability),
('sv4-225', 'Iron Valiant ex', ultra_rare_probability),
('sv4-228', 'Sandy Shocks ex', ultra_rare_probability),
('sv4-230', 'Aegislash ex', ultra_rare_probability),
('sv4-232', 'Altaria ex', ultra_rare_probability),
('sv4-196', 'Joltik', illustration_rare_probability),
('sv4-200', 'Mienshao', illustration_rare_probability),
('sv4-201', 'Minior', illustration_rare_probability),
('sv4-204', 'Garbodor', illustration_rare_probability),
('sv4-205', 'Yveltal', illustration_rare_probability),
('sv4-209', 'Ferrothorn', illustration_rare_probability),
('sv4-210', 'Aegislash', illustration_rare_probability),
('sv4-211', 'Aipom', illustration_rare_probability),
('sv4-212', 'Loudred', illustration_rare_probability),
('sv4-219', 'Garchomp ex', ultra_rare_probability),
('sv4-223', 'Iron Hands ex', ultra_rare_probability),
('sv4-224', 'Cofagrigus ex', ultra_rare_probability),
('sv4-195', 'Blitzle', illustration_rare_probability),
('sv4-198', 'Gimmighoul', illustration_rare_probability),
('sv4-199', 'Groudon', illustration_rare_probability),
('sv4-202', 'Garganacl', illustration_rare_probability),
('sv4-206', 'Morpeko', illustration_rare_probability),
('sv4-207', 'Brute Bonnet', illustration_rare_probability),
('sv4-208', 'Steelix', illustration_rare_probability),
('sv4-214', 'Porygon-Z', illustration_rare_probability),
('sv4-215', 'Cyclizar', illustration_rare_probability),
('sv4-217', 'Froslass ex', ultra_rare_probability),
('sv4-221', 'Golisopod ex', ultra_rare_probability),
('sv4-222', 'Tapu Koko ex', ultra_rare_probability),
('sv4-229', 'Roaring Moon ex', ultra_rare_probability),
('sv4-231', 'Gholdengo ex', ultra_rare_probability),
('sv4-233', 'Maushold ex', ultra_rare_probability),
('sv4-237', 'Norman', ultra_rare_probability),
('sv4-234', 'Bombirdier ex', ultra_rare_probability),
('sv4-235', 'Larry', ultra_rare_probability),
('sv4-236', 'Mela', ultra_rare_probability),
('sv4-238', 'Parasol Lady', ultra_rare_probability),
('sv4-239', 'Professor Sada\'s Vitality', ultra_rare_probability),
('sv4-240', 'Professor Turo\'s Scenario', ultra_rare_probability),
('sv4-241', 'Rika', ultra_rare_probability),
('sv4-242', 'Roark', ultra_rare_probability),
('sv4-247', 'Tapu Koko ex', special_illustration_rare_probability),
('sv4-249', 'Iron Valiant ex', special_illustration_rare_probability),
('sv4-250', 'Sandy Shocks ex', special_illustration_rare_probability),
('sv4-248', 'Iron Hands ex', special_illustration_rare_probability),
('sv4-243', 'Shauntal', ultra_rare_probability),
('sv4-245', 'Garchomp ex', special_illustration_rare_probability),
('sv4-246', 'Golisopod ex', special_illustration_rare_probability),
('sv4-251', 'Roaring Moon ex', special_illustration_rare_probability),
('sv4-244', 'Tulip', ultra_rare_probability),
('sv4-252', 'Gholdengo ex', special_illustration_rare_probability),
('sv4-257', 'Professor Turo\'s Scenario', special_illustration_rare_probability),
('sv4-262', 'Roaring Moon ex', hyper_rare_probability),
('sv4-265', 'Luxurious Cape', hyper_rare_probability),
('sv4-256', 'Professor Sada\'s Vitality', special_illustration_rare_probability),
('sv4-261', 'Iron Valiant ex', hyper_rare_probability),
('sv4-263', 'Beach Court', hyper_rare_probability),
('sv4-258', 'Rika', special_illustration_rare_probability),
('sv4-259', 'Tulip', special_illustration_rare_probability),
('sv4-260', 'Garchomp ex', hyper_rare_probability),
('sv4-253', 'Altaria ex', special_illustration_rare_probability),
('sv4-254', 'Mela', special_illustration_rare_probability),
('sv4-255', 'Parasol Lady', special_illustration_rare_probability),
('sv4-264', 'Counter Catcher', hyper_rare_probability),
('sv4-266', 'Reversal Energy', hyper_rare_probability),
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
    cur.execute('SELECT date FROM paradox_rift_cards WHERE card_id = ?', (card_id,))
    result = cur.fetchone()

    if result and result[0] == current_date:
        continue  # Skip update if the card is already updated today

    # Retrieve the current price
    current_price = get_current_price(card_id)

    # Update or insert card information
    cur.execute('''
    INSERT INTO paradox_rift_cards (card_id, card_name, probability, price, date)
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
    cur.execute('SELECT price, probability FROM paradox_rift_cards')
    paradox_rift_cards = cur.fetchall()

    # Calculate the total value
    for price, probability in paradox_rift_cards:
        total_value += price * probability

    # Close the database connection
    conn.commit()
    conn.close()

    return total_value


# Example usage of the function

