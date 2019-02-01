from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get('https://www.cinema-city.pl/kina/krakowplaza/1063#/buy-tickets-by-cinema?in-cinema=1063&at=2019-02-07&view-mode=list')

button = driver.find_element_by_class_name('datepicker-toggle')
button.click()

dpicker_outer = driver.find_element_by_class_name('quickbook-datepicker')
dpicker = dpicker_outer.find_element_by_class_name('datepicker-days')
dpicker_table = dpicker.find_element_by_tag_name('table')


