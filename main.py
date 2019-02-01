from selenium import webdriver

MONTH_NAME = "Luty"

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

# print('Current month: {}'.format(get_current_month(dpicker_table)))

calendar_rows = dpicker_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
# print('Discovered {} rows.'.format(len(calendar_rows)))

# Build a list of days - tuples (classname, day number).
# Get tr elements from each row.
this_month = lambda day: day.get_attribute('class') == 'day active'
days = []
for row in calendar_rows:
	d = row.find_elements_by_tag_name('td')
	d = [(i.get_attribute('class'), i.text) for i in d if this_month(i)]
	days += d

# print('Obtained {} days:\n{}'.format(len(days), days))

def day_print(arr):
	result = ''
	for i in arr:
		result += i[1] + ' '
	return result

print('Active days in {}: {}'.format(MONTH_NAME, day_print(days)))
