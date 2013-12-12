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
	
#Dependencies
[Beautiful Soup v4](http://www.crummy.com/software/BeautifulSoup/bs4/) is required for this script to run. You can install it using the following command:

	pip install beautifulsoup4
	
*Note: I'm open to any commits that make this project faster, more efficient, easier to use, or more functional.*
