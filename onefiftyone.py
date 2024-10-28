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
12 Double Rare 1.11% (0.48%)
16 Ultra Rare 0.4% (0.29%)
16 Illustration Rare 0.53% (0.34%)
7 Special Illustration Rare 0.44% (0.31%)
3 Hyper Rare 0.65% (0.37%)
'''
double_rare_probability = 0.0111
ultra_rare_probability = 0.004
illustration_rare_probability = 0.0053
special_illustration_rare_probability = 0.0044
hyper_rare_probability = 0.0065

conn = sqlite3.connect("alpha.db")
cur = conn.cursor()

# Create the table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS onefiftyone_cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    probability REAL NOT NULL,
    price REAL,
    date TEXT)
''')

# Array of cards with id, name, and probability
cards = [
('sv3pt5-3', 'Venusaur ex', double_rare_probability),
('sv3pt5-6', 'Charizard ex', double_rare_probability),
('sv3pt5-9', 'Blastoise ex', double_rare_probability),
('sv3pt5-24', 'Arbok ex', double_rare_probability),
('sv3pt5-38', 'Ninetales ex', double_rare_probability),
('sv3pt5-40', 'Wigglytuff ex', double_rare_probability),
('sv3pt5-65', 'Alakazam ex', double_rare_probability),
('sv3pt5-76', 'Golem ex', double_rare_probability),
('sv3pt5-115', 'Kangaskhan ex', double_rare_probability),
('sv3pt5-124', 'Jynx ex', double_rare_probability),
('sv3pt5-145', 'Zapdos ex', double_rare_probability),
('sv3pt5-151', 'Mew ex', double_rare_probability),
('sv3pt5-166', 'Bulbasaur', illustration_rare_probability),
('sv3pt5-167', 'Ivysaur', illustration_rare_probability),
('sv3pt5-168', 'Charmander', illustration_rare_probability),
('sv3pt5-169', 'Charmeleon', illustration_rare_probability),
('sv3pt5-170', 'Squirtle', illustration_rare_probability),
('sv3pt5-171', 'Wartortle', illustration_rare_probability),
('sv3pt5-172', 'Caterpie', illustration_rare_probability),
('sv3pt5-173', 'Pikachu', illustration_rare_probability),
('sv3pt5-174', 'Nidoking', illustration_rare_probability),
('sv3pt5-175', 'Psyduck', illustration_rare_probability),
('sv3pt5-176', 'Poliwhirl', illustration_rare_probability),
('sv3pt5-177', 'Machoke', illustration_rare_probability),
('sv3pt5-178', 'Tangela', illustration_rare_probability),
('sv3pt5-179', 'Mr. Mime', illustration_rare_probability),
('sv3pt5-180', 'Omanyte', illustration_rare_probability),
('sv3pt5-181', 'Dragonair', illustration_rare_probability),
('sv3pt5-182', 'Venusaur ex', ultra_rare_probability),
('sv3pt5-183', 'Charizard ex', ultra_rare_probability),
('sv3pt5-184', 'Blastoise ex', ultra_rare_probability),
('sv3pt5-185', 'Arbok ex', ultra_rare_probability),
('sv3pt5-186', 'Ninetales ex', ultra_rare_probability),
('sv3pt5-187', 'Wigglytuff ex', ultra_rare_probability),
('sv3pt5-188', 'Alakazam ex', ultra_rare_probability),
('sv3pt5-189', 'Golem ex', ultra_rare_probability),
('sv3pt5-190', 'Kangaskhan ex', ultra_rare_probability),
('sv3pt5-191', 'Jynx ex', ultra_rare_probability),
('sv3pt5-192', 'Zapdos ex', ultra_rare_probability),
('sv3pt5-193', 'Mew ex', ultra_rare_probability),
('sv3pt5-194', 'Bill\'s Transfer', ultra_rare_probability),
('sv3pt5-195', 'Daisy\'s Help', ultra_rare_probability),
('sv3pt5-196', 'Erika\'s Invitation', ultra_rare_probability),
('sv3pt5-197', 'Giovanni\'s Charisma', ultra_rare_probability),
('sv3pt5-198', 'Venusaur ex', special_illustration_rare_probability),
('sv3pt5-199', 'Charizard ex', special_illustration_rare_probability),
('sv3pt5-200', 'Blastoise ex', special_illustration_rare_probability),
('sv3pt5-201', 'Alakazam ex', special_illustration_rare_probability),
('sv3pt5-202', 'Zapdos ex', special_illustration_rare_probability),
('sv3pt5-203', 'Erika\'s Invitation', special_illustration_rare_probability),
('sv3pt5-204', 'Giovanni\'s Charisma', special_illustration_rare_probability),
('sv3pt5-205', 'Mew ex', hyper_rare_probability),
('sv3pt5-206', 'Switch', hyper_rare_probability),
('sv3pt5-207', 'Basic Psychic Energy', hyper_rare_probability),

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
    cur.execute('SELECT date FROM onefiftyone_cards WHERE card_id = ?', (card_id,))
    result = cur.fetchone()

    if result and result[0] == current_date:
        continue  # Skip update if the card is already updated today

    # Retrieve the current price
    current_price = get_current_price(card_id)

    # Update or insert card information
    cur.execute('''
    INSERT INTO onefiftyone_cards (card_id, card_name, probability, price, date)
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
    cur.execute('SELECT price, probability FROM onefiftyone_cards')
    onefiftyone_cards = cur.fetchall()

    # Calculate the total value
    for price, probability in onefiftyone_cards:
        total_value += price * probability

    # Close the database connection

    conn.commit()
    conn.close()
    return total_value




