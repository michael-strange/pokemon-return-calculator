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
import constants

import evolving_skies
import paldea_evolved
import onefiftyone
import paldeanFates
import paradox_rift
import temporal_forces
import twilight_masquerade

RestClient.configure(constants.API_KEY)



# Create the table if it does not exist


current_date = datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    print("Starting")
    paldea_evolved_return = paldea_evolved.get_value()
    onefiftyone_return = onefiftyone.get_value()
    paldean_fates_return = paldeanFates.get_value()
    paradox_rift_return = paradox_rift.get_value()
    temporal_forces_return = temporal_forces.get_value()
    twilight_masquerade_return = twilight_masquerade.get_value()
    evolving_skies_return = evolving_skies.get_value()

    conn = sqlite3.connect("alpha.db")
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS returns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            set_name TEXT NOT NULL,
            return REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()




    cur.execute('''
           INSERT INTO returns (set_name, return, date) 
           VALUES (?, ?, ?)
       ''', ('Paldea Evolved', paldea_evolved_return, current_date))
    cur.execute('''
           INSERT INTO returns (set_name, return, date) 
           VALUES (?, ?, ?)
       ''', ('151', onefiftyone_return, current_date))
    cur.execute('''
               INSERT INTO returns (set_name, return, date) 
               VALUES (?, ?, ?)
           ''', ('Paldean Fates', paldean_fates_return, current_date))
    cur.execute('''
               INSERT INTO returns (set_name, return, date) 
               VALUES (?, ?, ?)
           ''',('Paradox Rift', paradox_rift_return, current_date))
    cur.execute('''
                INSERT INTO returns (set_name, return, date) 
                VALUES (?, ?, ?)
            ''', ('Temporal Forces', temporal_forces_return, current_date))
    cur.execute('''
                   INSERT INTO returns (set_name, return, date) 
                   VALUES (?, ?, ?)
               ''', ('Twilight Masquerade', twilight_masquerade_return, current_date))
    cur.execute('''
                   INSERT INTO returns (set_name, return, date) 
                   VALUES (?, ?, ?)
               ''', ('Evolving Skies', evolving_skies_return, current_date))

    conn.commit()
    conn.close()


