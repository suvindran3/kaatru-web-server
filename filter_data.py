import pandas


def heatmap_data() -> list:
    data = pandas.read_csv('consolidated_data.csv')
    lat = data['latitude'].tolist()
    lng = data['longitude'].tolist()
    aod = data['aod'].tolist()
    return [[lat[i], lng[i], aod[i]] for i in range(len(aod))]
