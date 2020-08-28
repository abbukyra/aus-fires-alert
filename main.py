import urllib.request
import zipfile
import folium
import geopandas as gpd
import os
import slack

def downloadAndUnzip(file_path):
    print('Beginning file download...')
    url = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/shapes/zips/MODIS_C6_Australia_NewZealand_24h.zip'
    saving_path = file_path + '/' + 'aus.zip'
    urllib.request.urlretrieve(url, saving_path)
    print('Extracting zip file with zipfile...')
    with zipfile.ZipFile(saving_path, 'r') as zip_ref:
        zip_ref.extractall(file_path)
    return True

def dataVisualization(file_path):
    print('Beginning data visualization...')
    new_file_name = file_path + '/' + "MODIS_C6_Australia_NewZealand_24h.shp"
    aus_fires = gpd.read_file(new_file_name)
    map = folium.Map([-25.2744, 133.7751], zoom_start = 5) # sets view at australia
    for index, row in aus_fires.iterrows():
        folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup= "Date: " + row['ACQ_DATE']).add_to(map)
    map.save('australia-fires.html')
    return True

def slackNotifier():
    print('Notifying slack channel...')
    client = slack.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    response = client.chat_postMessage(
        channel='#australia-fires',
        text="FIRE ALERT! There is a new update on the fires in Australia.")
    return True

if __name__ == "__main__":
    file_path = input("Where do you want your files to be saved?\n(Hint: Locate the folder through the Terminal and run 'pwd')\n")
    print("Your files will be located in: " + file_path)
    downloadAndUnzip(file_path)
    print("Success!")
    dataVisualization(file_path)
    print("Success!")
    slackNotifier()
    print("You may now open australia-fires.html, located in %s." % file_path)
