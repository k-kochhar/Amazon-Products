from bs4 import BeautifulSoup
import requests

'''
Install Commands

pip install bs4
pip install requests
'''

# Function to get Product Title
def getTitle(soup):    
	try:
		title = soup.find('span', attrs={'id':'productTitle'})
		titleValue = title.string
		titleString = titleValue.strip()

	except:
		titleString = 'Unavailable'	

	return titleString

# Function to get Product Price
def getPrice(soup):
	try:
		price = soup.find('span', attrs={'id':'priceblock_ourprice'}).string.strip()

	except AttributeError:

		try:
			price = soup.find('span', attrs={'id':'priceblock_dealprice'}).string.strip()

		except:		
			price = 'Unavailable'	

	return price

# Function to get Product Rating
def getRating(soup):
	try:
		rating = soup.find('i', attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()

	except AttributeError:
		try:
			rating = soup.find('span', attrs={'class':'a-icon-alt'}).string.strip()

		except:
			rating = 'Unavailable'

	return rating

# Function to get Number of User Reviews
def getReviewCount(soup):
	try:
		reviewCount = soup.find('span', attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except:
		reviewCount = 'Unavailable'

	return reviewCount

# Function to get Availability Status
def getAvailability(soup):
	try:
		available = soup.find('div', attrs={'id':'availability'})
		available = available.find('span').string.strip()

	except:
		available = 'Unavailable'	

	if available.isspace():
		return('Unavalable')

	else:
		return available	

if __name__ == '__main__':
	# Headers for request
	HEADERS = ({'User-Agent':
				'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
				'Accept-Language': 'en-US'})

	# Prompt for the product name
	productName = input('Enter the name of an Amazon Product: ').split(' ')
	resultAmount = int(input('Enter the amount of results you want (int): '))

	usefulName = ''

	for word in productName:
		usefulName += '+' + word
    
	usefulName = usefulName[1:]

	URL = f'https://www.amazon.com/s?k={usefulName}&ref=nb_sb_noss_2'

	print()

	# HTTP Request
	webpage = ''

	try:
		webpage = requests.get(URL, headers=HEADERS)

		soup = BeautifulSoup(webpage.content, 'lxml')

	    # Get links as List of Tag Objects
		links = soup.find_all('a', attrs={'class':'a-link-normal s-no-outline'})

	    # Store the links
		linksList = []

	    # Loop for extracting links from Tag Objects
		for i in range(resultAmount):
			linksList.append(links[i].get('href'))

		count = 1
		for link in linksList: 
        
			webpageURL = 'https://www.amazon.com' + link
            
			newWebpage = requests.get(webpageURL, headers=HEADERS)

			soup = BeautifulSoup(newWebpage.content, 'lxml')
		    
            # Function calls to display product information
			print('Item', count)
			print()
			print('Product Title =', getTitle(soup))
			print('Product Price =', getPrice(soup))
			print('Product Rating =', getRating(soup))
			print('Number of Product Reviews =', getReviewCount(soup))
			print('Availability =', getAvailability(soup))
			print()
			print('Product URL =', webpageURL)
			print()
			count += 1

	except:
		print('URL ERROR')