import pandas as pd
import json
import plotly
import plotly.express as px
import requests
def replaceEmptyImages(dictList, url):
	for d in dictList:
		if ("image_url" not in d or not d["image_url"]):
			d["image_url"]=url

def find_coffee(location1='Tacoma, Washington',returnLimit=50):
	api_key = 'pMWcYDMpXkTeeyWIb7AtpzRbcJ2PKRvHIzT7p0QAukPFge4IGKectozkpQBkZnTBKE9g3FwC7Os68MmQKgAwwucLgeMo0oMgagYENkYs-9TZKKJ8HXXMmwM1ZAaBYHYx'
	headers = {'Authorization': 'Bearer {}'.format(api_key)}
	search_api_url = 'https://api.yelp.com/v3/businesses/search'
	params = {'term': 'coffee shop', 
	          'location': location1,
	          'limit': returnLimit}
	response = requests.get(search_api_url, headers=headers, params=params, timeout=5)
	data=response.json()
	sortedbyRating=sorted(data["businesses"], key=lambda i: i['rating'], reverse=True)
	replaceEmptyImages(sortedbyRating,"localhost")
	return sortedbyRating

def graph_coffee(location1='Tacoma, Washington'):
    businesses=find_coffee(location1,returnLimit=20)
    unique_names=[]
    ratings=[]
    for i in range (len(businesses)):
        if businesses[i]['name'] not in unique_names:
            unique_names.append(businesses[i]['name'])
            ratings.append(businesses[i]['rating'])
    
    df = pd.DataFrame(
     {"Name" : unique_names,
      "Rating" : ratings
      }
    )
    fig = px.bar(df, x="Name", y="Rating")
    fig.update_yaxes(range=(0.0,5),tick0=0.0, dtick=.5)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)