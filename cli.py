from app.steamdb_parser import SteamdbParser
def run_cli():
    while True:
        print('########################################################\n\
        what would you like to do:\n\
        1. get data from https://steamdb.info/topsellers\n\
        2. get data from https://steamdb.info/charts\n\
        3. cancel')

        option = input('>>')
        if option == '1':
            steamdb_parser = SteamdbParser()
            steamdb_parser.get_and_save_sellers()
        elif option == '2':
            steamdb_parser = SteamdbParser()
            steamdb_parser.get_and_save_charts()
        else:
            return
if __name__ == '__main__':
    run_cli()
