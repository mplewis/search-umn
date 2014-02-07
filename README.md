search-umn
==========

[![tip for next commit](http://tip4commit.com/projects/189.svg)](http://tip4commit.com/projects/189)

#Purpose
To search the [UMN People Directory](http://search.umn.edu/) using a Python API.

#Example

The basic usage of the script is as follows:
	
	./search.py McKinney

To search for a person using their full name, enclose it in quotation marks like:

	./search.py "Nicholas McKinney"

To search by Internet ID instead of name, use `-t` or `--search_type`:

	./search.py -t id McKinney

To limit your search to a particular campus, use `-c` or `--campus`. The following campus codes are allowed:

	a	Any campus
	c	Crookston
	d	Duluth
	m	Morris
	r	Rochester
	t	Twin Cities
	o	Other
	
	Example:
	./search.py -c c
To limit your search to people in a particular role, use `-r` or `--role`. The following role codes are allowed:

	any		Any role
	sta		Faculty/Staff
	stu		Student
	alu		Alumni
	ret		Retired Faculty
	
	Example:
	./search.py -r stu

#Dependencies
[Beautiful Soup v4](http://www.crummy.com/software/BeautifulSoup/bs4/) is required for this script to run. You can install it using the following command:

	pip install beautifulsoup4
	
*Note: I'm open to any commits that make this project faster, more efficient, easier to use, or more functional.*
