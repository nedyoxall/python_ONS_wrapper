# Notes on how to make this work!

* link to not completely useless Powerpoint presentation for broad overview of the ONS API [here](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwjrgqKJ4snNAhWj3YMKHckNAGMQFgglMAE&url=https%3A%2F%2Fweb.ons.gov.uk%2Fons%2Fapiservice%2Fdocuments%2F10854%2F19108%2FONS_API_Training_Course_S3.pptx%2F8dbe0978-063c-47db-94c9-b1cc7434e79d&usg=AFQjCNEhR8UrVb8A2Z6MnnYicfP38aRfag&sig2=WXW7_H-fEKQruYyfUltLVw&bvm=bv.125596728,d.amc).
* The base URL for any query is:  
  		
  		http://web.ons.gov.uk/ons/api/data/
  		
* This might be good for finding what exists in the first place:

		http://web.ons.gov.uk/ons/data/web/explorer
		http://web.ons.gov.uk/ons/data/dataset-finder
		
* Other handy sources:
		
		https://gist.github.com/sammachin/671f90c15ec6331598e5
		https://web.ons.gov.uk/ons/apiservice/web/apiservice/how-to-guides
		
* Shapefiles - scroll to the bottom of the page (for everything UK by the looks of it):  

		https://census.ukdataservice.ac.uk/use-data/guides/boundary-data
		
* For the future (particularly if want to do something with house prices):  
		
		http://developer.zoopla.com/docs/read/Home
		http://landregistry.data.gov.uk/
		https://data.police.uk/
		
* And other possible shapefile/background info:
		
		http://webarchive.nationalarchives.gov.uk/20160105160709/http://www.ons.gov.uk/ons/guide-method/geography/beginner-s-guide/census/index.html
		
* Files about ONS geographic codes:

		http://neighbourhood.statistics.gov.uk/dissemination/Info.do?m=0&s=1467345946422&enc=1&page=nessgeography/new-geography-codes-and-naming-policy-from-1-january-2011.htm&nsjs=true&nsck=false&nssvg=false&nswid=1280
		
* also check out jsonstat data type (a subset of json):
		
		http://www.slideshare.net/badosa/json-stat

/////////////////////////////////////////  

The datastore beneath the API is divided in 4 sections. These are known as **contexts**, and explicitly are *Census*, *Socio-Economic*, *Economic* and *Social*. The four contexts can be viewed via:

	http://web.ons.gov.uk/ons/api/data/contexts.json?apikey=<your_apikey>
		
where they appear as entries in the `contextList` section. Note that it is possible for the same name to appear in more than one context (although it will presumably be referring to different data!).