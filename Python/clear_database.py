from database import database

import logging

if __name__ == '__main__':
    database.clear_substances()
    logging.info("Cleared substances from the database.")
    