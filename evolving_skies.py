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
15 Holo Vmax 1/18 rare_holo_vmax
Full Art V 1/56
Full Art Trainer 1/197
Rainbow Rare 1/82
Golden Rare 1/99
Alt Art V 1/82
Alt Art Vmax 1/283
'''
holo_vmax_probability = 1 / 18 / 14
full_art_v_probability = 1 / 56 / 22
full_art_trainer_probability = 1 / 197 / 5
rare_rainbow_probability = 1 / 82 / 16
rare_secret_probability = 1 / 99 / 12
alt_art_v_probability = 1 / 82 / 11
alt_art_vmax_probability = 1 / 283 / 6

conn = sqlite3.connect("alpha.db")
cur = conn.cursor()

# Create the table if it does not exist
cur.execute('''
CREATE TABLE IF NOT EXISTS evolving_skies_cards (
    card_id TEXT PRIMARY KEY,
    card_name TEXT NOT NULL,
    probability REAL NOT NULL,
    price REAL,
    date TEXT)
''')

# Array of cards with id, name, and probability
cards = [
    #Holo VMAX Count = 14
('swsh7-30', 'Vaporeon VMAX', holo_vmax_probability),
('swsh7-18', 'Flareon VMAX', holo_vmax_probability),
('swsh7-51', 'Jolteon VMAX', holo_vmax_probability),
('swsh7-92', 'Lycanroc VMAX', holo_vmax_probability),
('swsh7-123', 'Duraludon VMAX', holo_vmax_probability),
('swsh7-41', 'Glaceon VMAX', holo_vmax_probability),
('swsh7-111', 'Rayquaza VMAX', holo_vmax_probability),
('swsh7-8', 'Leafeon VMAX', holo_vmax_probability),
('swsh7-14', 'Trevenant VMAX', holo_vmax_probability),
('swsh7-59', 'Dracozolt VMAX', holo_vmax_probability),
('swsh7-29', 'Gyarados VMAX', holo_vmax_probability),
('swsh7-65', 'Espeon VMAX', holo_vmax_probability),
('swsh7-75', 'Sylveon VMAX', holo_vmax_probability),
('swsh7-95', 'Umbreon VMAX', holo_vmax_probability),
('swsh7-101', 'Garbodor VMAX', holo_vmax_probability),

#Full Art V Count = 22
('swsh7-166', 'Leafeon V', full_art_v_probability),
('swsh7-168', 'Trevenant V', full_art_v_probability),
('swsh7-169', 'Flareon V', full_art_v_probability),
('swsh7-170', 'Volcarona V', full_art_v_probability),
('swsh7-171', 'Gyarados V', full_art_v_probability),
('swsh7-172', 'Vaporeon V', full_art_v_probability),
('swsh7-173', 'Suicune V', full_art_v_probability),
('swsh7-174', 'Glaceon V', full_art_v_probability),
('swsh7-176', 'Arctovish V', full_art_v_probability),
('swsh7-177', 'Jolteon V', full_art_v_probability),
('swsh7-178', 'Dracozolt V', full_art_v_probability),
('swsh7-179', 'Espeon V', full_art_v_probability),
('swsh7-181', 'Golurk V', full_art_v_probability),
('swsh7-183', 'Sylveon V', full_art_v_probability),
('swsh7-185', 'Medicham V', full_art_v_probability),
('swsh7-187', 'Lycanroc V', full_art_v_probability),
('swsh7-188', 'Umbreon V', full_art_v_probability),
('swsh7-190', 'Garbodor V', full_art_v_probability),
('swsh7-191', 'Dragonite V', full_art_v_probability),
('swsh7-193', 'Rayquaza V', full_art_v_probability),
('swsh7-195', 'Noivern V', full_art_v_probability),
('swsh7-197', 'Duraludon V', full_art_v_probability),

#Alt art v count = 11
('swsh7-167', 'Leafeon V', alt_art_v_probability),
('swsh7-175', 'Glaceon V', alt_art_v_probability),
('swsh7-180', 'Espeon V', alt_art_v_probability),
('swsh7-182', 'Golurk V', alt_art_v_probability),
('swsh7-184', 'Sylveon V', alt_art_v_probability),
('swsh7-186', 'Medicham V', alt_art_v_probability),
('swsh7-189', 'Umbreon V', alt_art_v_probability),
('swsh7-192', 'Dragonite V', alt_art_v_probability),
('swsh7-194', 'Rayquaza V', alt_art_v_probability),
('swsh7-196', 'Noivern V', alt_art_v_probability),
('swsh7-198', 'Duraludon V', alt_art_v_probability),

#Full art trainer count = 5
('swsh7-199', 'Aroma Lady', full_art_trainer_probability),
('swsh7-200', 'Copycat', full_art_trainer_probability),
('swsh7-201', 'Gordie', full_art_trainer_probability),
('swsh7-202', 'Raihan', full_art_trainer_probability),
('swsh7-203', 'Zinnia\'s Resolve', full_art_trainer_probability),

#Rainbow rare count = 16
('swsh7-204', 'Leafeon VMAX', rare_rainbow_probability),
('swsh7-210', 'Dracozolt VMAX', rare_rainbow_probability),
('swsh7-221', 'Aroma Lady', rare_rainbow_probability),
('swsh7-225', 'Zinnia\'s Resolve', rare_rainbow_probability),
('swsh7-223', 'Gordie', rare_rainbow_probability),
('swsh7-207', 'Gyarados VMAX', rare_rainbow_probability),
('swsh7-208', 'Glaceon VMAX', rare_rainbow_probability),
('swsh7-213', 'Lycanroc VMAX', rare_rainbow_probability),
('swsh7-217', 'Rayquaza VMAX', rare_rainbow_probability),
('swsh7-224', 'Raihan', rare_rainbow_probability),
('swsh7-206', 'Trevenant VMAX', rare_rainbow_probability),
('swsh7-211', 'Sylveon VMAX', rare_rainbow_probability),
('swsh7-214', 'Umbreon VMAX', rare_rainbow_probability),
('swsh7-216', 'Garbodor VMAX', rare_rainbow_probability),
('swsh7-219', 'Duraludon VMAX', rare_rainbow_probability),
('swsh7-222', 'Copycat', rare_rainbow_probability),

#Alt art vmax count = 6
('swsh7-205', 'Leafeon VMAX', alt_art_vmax_probability),
('swsh7-209', 'Glaceon VMAX', alt_art_vmax_probability),
('swsh7-212', 'Sylveon VMAX', alt_art_vmax_probability),
('swsh7-215', 'Umbreon VMAX', alt_art_vmax_probability),
('swsh7-218', 'Rayquaza VMAX', alt_art_vmax_probability),
('swsh7-220', 'Duraludon VMAX', alt_art_vmax_probability),

#Rainbow rare count= 12
('swsh7-229', 'Boost Shake', rare_secret_probability),
('swsh7-233', 'Toy Catcher', rare_secret_probability),
('swsh7-231', 'Full Face Guard', rare_secret_probability),
('swsh7-237', 'Metal Energy', rare_secret_probability),
('swsh7-226', 'Froslass', rare_secret_probability),
('swsh7-228', 'Cresselia', rare_secret_probability),
('swsh7-227', 'Inteleon', rare_secret_probability),
('swsh7-230', 'Crystal Cave', rare_secret_probability),
('swsh7-235', 'Lightning Energy', rare_secret_probability),
('swsh7-234', 'Turffield Stadium', rare_secret_probability),
('swsh7-236', 'Darkness Energy', rare_secret_probability),
('swsh7-232', 'Stormy Mountains', rare_secret_probability)

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
    cur.execute('SELECT date FROM evolving_skies_cards WHERE card_id = ?', (card_id,))
    result = cur.fetchone()

    if result and result[0] == current_date:
        continue  # Skip update if the card is already updated today

    # Retrieve the current price
    current_price = get_current_price(card_id)

    # Update or insert card information
    cur.execute('''
    INSERT INTO evolving_skies_cards (card_id, card_name, probability, price, date)
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
    cur.execute('SELECT card_name, price, probability FROM evolving_skies_cards')
    evolving_skies_cards = cur.fetchall()

    # Calculate the total value
    for card_name, price, probability in evolving_skies_cards:
        total_value += price * probability

    # Close the database connection
    conn.commit()
    conn.close()

    return total_value


# Example usage of the function

