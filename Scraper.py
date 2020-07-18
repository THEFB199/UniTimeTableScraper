import string
import time
from selenium import webdriver
import re
import datetime
from ics import Calendar, Event
from selenium.webdriver.common.keys import Keys


def day_converter(day):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return days.index(day)


def month_converter(month):
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    return months.index(month) + 1


Username = "PUT USERNAME HERE"
Password = "PUT PASSWORD HERE"

calendar = Calendar()
calEvent = Event()

ModuleID = []
Title = []
Room = []
StartTimes = []
EndTimes = []
Type = []
Date = []

x = datetime.datetime(2020, month_converter('OCT'), 17)
i = 0
j=0
MonthoffSet = 0
driver = webdriver.Chrome()
driver.get("https://lucas.lboro.ac.uk/its_apx/f?p=250:LOGIN:14916774692854:")


time.sleep(2)
element = driver.find_element_by_id("P101_USERNAME")
time.sleep(1.3498)
element.send_keys(Username)
element = driver.find_element_by_id("P101_PASSWORD")
time.sleep(1.3498)
element.send_keys(Password)
time.sleep(1.3498)
element = driver.find_element_by_id("LOGIN")
element.click()
time.sleep(1)


element = driver.find_element_by_xpath("//select[@name='P2_MY_PERIOD']")
all_options = element.find_elements_by_tag_name("option")
try:
	for option in all_options:
		MonthoffSet = 0
		element = driver.find_element_by_xpath("//select[@name='P2_MY_PERIOD']")
		all_options = element.find_elements_by_tag_name("option")
		time.sleep(1.5)
		option = all_options[i]
		if (option.text == "Semester 1") or (option.text == "Semester 2"):
			print("Nope")
			i += 1
		else:

			WeekStartDate = re.findall("[0-9]{2}-[A-Z]{3}-[0-9]{4}", option.text)
			Month = re.findall("[A-Z]{3}", WeekStartDate[0])
			Month = Month[0]
			Day = re.findall("[0-9]{2}-", WeekStartDate[0])
			Day = Day[0][0:-1]
			Year = re.findall("-[0-9]{4}", WeekStartDate[0])
			Year = Year[0][1:]
			DateStart = datetime.datetime((int(Year)), month_converter(Month), int(Day))

			time.sleep(1.5)
			option.click()
			time.sleep(1.5)
			print("clicked")
			AllEvents = driver.find_elements_by_class_name("new_row_tt_info_cell")
			j = 0
			for event in AllEvents:
				try:
					time.sleep(1.33243)
					event = AllEvents[j]
					print("Event found!")
					event.click()
					time.sleep(1.3234)

					ModuleID = driver.find_element_by_id("module_id_str").text

					EventWindow = driver.find_element_by_xpath("//*[@id='action_page']")
					Link = EventWindow.get_attribute('data')
					driver.execute_script(("window.open( '%s' ,'_blank');" % Link))
					windows = driver.window_handles
					driver.switch_to.window(windows[1])

					Title = driver.find_element_by_xpath('//*[@id="report_R2352715728635810437"]/tbody/tr[2]/td/table/tbody/tr[2]/td/div/div[1]').text
					Room = driver.find_element_by_xpath('//*[@id="room_str_div"]').text
					TimeDay = driver.find_element_by_xpath('//*[@id="report_R2352715728635810437"]/tbody/tr[2]/td/table/tbody/tr[2]/td/div/div[3]/dl/dd[3]').text
					if not len(re.findall("[A-Z][a-z]{5,12}", TimeDay)):
						TimeDay = driver.find_element_by_xpath('//*[@id="report_R2352715728635810437"]/tbody/tr[2]/td/table/tbody/tr[2]/td/div/div[3]/dl/dd[4]').text
					Weekday = re.findall("[A-Z][a-z]{5,12}", TimeDay)
					Times = re.findall("[0-9]{2}:[0-9]{2}", TimeDay)
					StartTime = Times[0]
					EndTime = Times[1]
					try:
						TimeDayStart = datetime.datetime((int(Year)), month_converter(Month)+MonthoffSet, int(Day)+day_converter(Weekday[0]), int(StartTime[0:2]), int(StartTime[3:4]), 0)
					except Exception as error:
						#if error == "ValueError: day is out of range for month":
						currentMonth = month_converter(Month)
						Day = '0'
						if currentMonth + 1 == 13:
							MonthoffSet = -11
						else:
							MonthoffSet = 1
						TimeDayStart = datetime.datetime((int(Year)), month_converter(Month) + MonthoffSet,int(Day) + day_converter(Weekday[0]), int(StartTime[0:2]),int(StartTime[3:4]), 0)

					TimeDayEnd = datetime.datetime((int(Year)), month_converter(Month) + MonthoffSet, int(Day)+day_converter(Weekday[0]), int(EndTime[0:2]), int(EndTime[3:4]), 0)

					StartTimes.append(TimeDayStart)
					EndTimes.append(TimeDayEnd)

					Type = driver.find_element_by_xpath('//*[@id="report_R2352715728635810437"]/tbody/tr[2]/td/table/tbody/tr[2]/td/div/div[2]').text
					time.sleep(2)
					driver.close()
					driver.switch_to.window(windows[0])
					driver.find_element_by_xpath('//*[@id="action_div"]/div/div[1]/table/tbody/tr/td[2]/span').click()

					element = driver.find_element_by_xpath("//select[@name='P2_MY_PERIOD']")
					all_options = element.find_elements_by_tag_name("option")
					driver.refresh()
					AllEvents = driver.find_elements_by_class_name("new_row_tt_info_cell")
					time.sleep(0.52345)
					j+=1

					calendar = Calendar()
					calEvent = Event()
					calEvent.name = Title + Type
					calEvent.begin = TimeDayStart.isoformat()
					calEvent.end = TimeDayEnd.isoformat()
					calEvent.location = Room
					calendar.events.add(calEvent)
					calendar.events

					FileName = Title + TimeDayStart.isoformat()
					FileName = FileName.replace(':','')
					FileName = FileName.replace(' ', '')
					# [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
					with open('CalendarFiles/'+ FileName +'.ics', 'w') as my_file:
						my_file.writelines(calendar)


				except Exception as errors:
					print(errors)
					time.sleep(2)
					driver.close()
					driver.switch_to.window(windows[0])
					driver.find_element_by_xpath('//*[@id="action_div"]/div/div[1]/table/tbody/tr/td[2]/span').click()
					# driver.get(driver.getCurrentURL())
					element = driver.find_element_by_xpath("//select[@name='P2_MY_PERIOD']")
					all_options = element.find_elements_by_tag_name("option")
					driver.refresh()
					AllEvents = driver.find_elements_by_class_name("new_row_tt_info_cell")
					time.sleep(0.52345)
					j += 1

			i +=1
except Exception as err:
	print("Big Ol Problem")
	print(err)

driver.close()

