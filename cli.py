from app.steamdb_parser import SteamdbParser
import time

def run_cli():
    while True:
        print('########################################################\n\
        what would you like to do:\n\
        1. get data from https://steamdb.info/topsellers\n\
        2. get data from https://steamdb.info/charts\n\
        3. cancel')

        option = input('>>')
        if option == '1' or option == '2':
            steamdb_parser = SteamdbParser()
            for i in range(5): #5 attempt to parse page
                if option == '1':
                    status_code = steamdb_parser.get_sellers_data()
                    total_apps = len(steamdb_parser.data_sellers) - 1
                elif option == '2':
                    status_code = steamdb_parser.get_charts_data()
                    total_apps = len(steamdb_parser.data_charts) - 1
                if status_code == 200:
                    print('data received, total apps: {}'.format(total_apps))
                    if option == '1':
                        res_message = steamdb_parser.save_to_csv(steamdb_parser.file_sellers)
                    if option == '2':
                        res_message = steamdb_parser.save_to_csv(steamdb_parser.file_charts)
                    print(res_message)
                    break
                else:
                    print('status code: ', status_code)
                    print('waiting for the next attempt..')
                    time.sleep(8) # pause between atempts
                print('cant get data, try later')
        else:
            return

if __name__ == '__main__':
    run_cli()
