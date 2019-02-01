from selenium import webdriver
from datetime import datetime
import sys

MONTHS = {
	1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień',
	5: 'Maj', 6: 'Czerwiec', 7: 'Lipiec', 8: 'Sierpień',
	9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'
}

def displayUsage():
	print('Usage: {} date'.format(sys.argv[0]))
	print('Accepted date format: month-name-abbreviated day')
	print('\tExamples: Feb 21, Jun 3')



if len(sys.argv) != 2:
	displayUsage()
	exit(0)

# Read date.
try:
	datetime_object = datetime.strptime(sys.argv[1], '%b %d')
	MONTH_NAME = MONTHS[datetime_object.month]
	DAY_NUMBER = datetime_object.day
except ValueError as exc:
	displayUsage()
	exit(1)

# Initialize PhantomJS and read webpage.
driver = webdriver.PhantomJS()
driver.get('https://www.cinema-city.pl/kina/krakowplaza/1063#/buy-tickets-by-cinema?in-cinema=1063&at=2019-02-07&view-mode=list')

# Find and click button which opens the datepicker.
button = driver.find_element_by_class_name('datepicker-toggle')
button.click()

dpicker_outer = driver.find_element_by_class_name('quickbook-datepicker')
dpicker = dpicker_outer.find_element_by_class_name('datepicker-days')
dpicker_table = dpicker.find_element_by_class_name('table-condensed')
# Webscraper diary:
# <table class="table-condensed">
#   <thead>
#     <tr>
#       <th><button class="prev"/></th>
#       <th class="datepicker-switch">Month name</th>
#       <th><button class="next"/></th>
#     </tr>
#   </thead>
# </table>

# "Next month" button
next_month_button = dpicker_table.find_element_by_class_name('next')
get_current_month = lambda table: table.find_element_by_class_name('datepicker-switch').text.split()[0]

# Find desired month.
safety = 12
while get_current_month(dpicker_table) != MONTH_NAME:
	if safety == 0:
		print('Warning: month not found after 12 iterations. Exiting...')
		exit(1)
	next_month_button.click()
	safety -= 1

calendar_rows = dpicker_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

# Build a list of active days.
# Get tr elements from each row.
this_month = lambda day: day.get_attribute('class') == 'day active'
days = []
for row in calendar_rows:
	d = row.find_elements_by_tag_name('td')
	d = [i.text for i in d if this_month(i)]
	days += d

def day_print(arr):
	result = ''
	for i in arr:
		result += i + ' '
	return result

# print('Active days in {}: {}'.format(MONTH_NAME, day_print(days)))
print('{} {} is {}.'.format( DAY_NUMBER, MONTH_NAME, ('ACTIVE' if str(DAY_NUMBER) in days else 'inactive') ))
