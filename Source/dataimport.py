from Source import webscraper
from Source.database import database

def main ():
    scraped_substances = webscraper.get_substances_from_caymenchem()

    # ToDo: validated_substances = validate_substances()

    database.set_substances(scraped_substances)

    return

main()