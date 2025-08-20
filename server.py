from configparser import ConfigParser
import os 
import sys

# append tools folder to path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(f'{__location__}/tools')

# get the tools from that folder
from google_tools import sheet_handler
from onecard_tools import get_transactions
from grouping_tools import *

# get dates from the conf file
config = ConfigParser()
config.read(f'{__location__}/didobs.conf')
from_date, to_date = (config['Settings'][option].split("/") for option in ('from_date','to_date'))

# pull all of the transaction data from onecard
expenses = get_transactions(from_date,to_date)

# figure out how many d$ were available
total_funds = find_income(expenses)

print(total_funds)
exit()


output = by_time_of_day(expenses,.5)[1]
#output = by_categories(expenses)[1] # get output version of grouped


# start the Sheets session
session = sheet_handler()

# send the data
session.write("",output)