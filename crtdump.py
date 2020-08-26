#!/usr/bin/python3

import argparse
import mechanize
from bs4 import BeautifulSoup

# Function to get the HTML Document

def getPage(url):
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	webPage = browser.open(url)
	return webPage

# Function to parse the WebPage for domains and subdomains

def findData(webPage,domain):
	links 	    = []
	tempdomains = []
	subdomains  = []
	soup        = BeautifulSoup(webPage, 'html.parser')
	
	# Fetch all the elements with <td> tag
	for link in soup.find_all("table")[-1].findAll('td'):
		links.append(link)
	
	# Fetch all the elements that contain the data about the domain
	for text in links:
		if(domain in text.find(text=True)):
			tempdomains.append(text)

	# Create a list of all subdomains
	for subdomain in tempdomains:
		subdomains.append(subdomain.findAll(text=True))
	
	return subdomains

# Function to sort the list of lists to a single list with unique entries

def sortOutData(subdomains):
	domains = []
	uniqueNames = []
	for hosts in subdomains:
		for host in hosts:
			domains.append(host)
	uniqueNames = list(set(domains))
	return uniqueNames

# Function to print out the subdomains

def printResult(domains,domain):
    for host in domains:
        print(host)
    print()

# Main Function

def main():
	parser     = argparse.ArgumentParser()
	parser.add_argument("domain", help = "Specify the domain to hunt the subdomains")
	args       = parser.parse_args()

	url        = "https://crt.sh/?q="+args.domain
	webPage    = getPage(url)
	subdomains = findData(webPage, args.domain)
	result     = sortOutData(subdomains)
	printResult(result)

if(__name__ == '__main__'):
	main()
