import requests
from bs4 import BeautifulSoup
import csv
import gender_guesser.detector as gender
from multiprocessing.pool import ThreadPool

base_url = "http://av-info.faa.gov/DesigneeResults.asp?DsgnType=IA&Country=US&State=%25&City=&Page="
int_max = 1097

d = gender.Detector()

def scrape(i):
	parsed_entries = []
	print('Page: ', i)
	page = requests.get(base_url + str(i))
	soup = BeautifulSoup(page.text, features="lxml")
	entries = soup.select('.RowWhite')
	for entry in entries:
		row = [val.strip() for val in entry.text.strip().split('\n')]
		last_name, first_name = row[0].split(',')[0].strip(), row[0].split(',')[1].strip()
		faa_office = row[-1].split()[-1]
		try:
			sex = d.get_gender(first_name.split()[0].title())
		except:
			sex = "unknown"
		parsed_entries.append([first_name, last_name, faa_office, sex])
	with open('ia_list_2.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(parsed_entries)


def main():
	with open('ia_list.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		# writer.writerow(["FIRST_NAME", "LAST_NAME","FSDO OFFICE", "GENDER"])
	with ThreadPool(15) as p:
		p.map(scrape, range(1000, int_max))
	return


if __name__ == '__main__':
	main()
