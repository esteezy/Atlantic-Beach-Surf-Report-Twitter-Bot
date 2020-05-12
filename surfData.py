# coding=utf-8
# Evan Mason
# May 9, 2020
# Get local (Oceanana Pier, Atlantic Beach NC) data pertaining to surf conditions (stormglass.io)
# Send tweets reflecting surf conditions (tweepy)
#   - Get JSON object from stormglass.io API
#   - Store attributes of swell and wind conditions
#   - Only concerned about data during hours with sunlight (6am-8pm)
#   - Process data and reflect comments on current conditions (use of local knowledge)
#   - Tweet of conditions for given day for hours listed above
#   - Daily report sent at midnight the night before

import arrow
import requests
import twitterbotdemo

# global
date = '2020-05-12'

# communicate with stormglass.io API
# *forcast only includes a 7-day report*
# return received JSON object
def getJSONResponse():
  start = arrow.get(date)
  try:
    response = requests.get(
      'https://api.stormglass.io/v2/weather/point',
      params={
        'lat': 34.6980784,
        'lng': -76.7290726,
        'params': ','.join(['windSpeed', 'windDirection', 'swellHeight', 'swellDirection', 'swellPeriod']),
        'start': start.to('UTC').timestamp,  # Convert to UTC timestamp // start date report
        'end': start.shift(days=1).to('UTC').timestamp,
      },
      headers={
        'Authorization': '*******'
      },
      data={
        'key': 'value'
      }
    )
    response.raise_for_status()

  # exception handling
  except requests.exceptions.HTTPError as err:  # This is the correct syntax
    print('Invalid Return Type - stormyglass.io')
    raise SystemExit(err)

  # do something with response data.
  # data in metric
  json_data = response.json()
  return json_data

# parse JSON object data
# return type is a 2D array with conditions from 6am to 8pm (typical daylight hours)
def parseResponse(response):
  # create 2D array of info
  # arr[6][15]
  # arr[0][i] = current hour
  # arr[1][i] = swell height
  # arr[2][i] = swell direction
  # arr[3][i] = swell period
  # arr[4][i] = wind speed
  # arr[5][i] = wind direction
  columns, rows = (6, 15)
  arr = []
  currHour = 6
  for i in range(rows):
    # json_data['hours'][0] returns data for first hour of day
    # second index specifies which hour
    resp = response['hours'][6+i]
    # cardinal coordinates - 0 degrees = true North
    swellDirection = resp['swellDirection']['noaa']
    windDirection = resp['windDirection']['noaa']
    # units: meters
    swellHeight = resp['swellHeight']['noaa']
    # units: seconds
    swellPeriod = resp['swellPeriod']['noaa']
    # units: meters per second
    windSpeed = resp['windSpeed']['icon']

    # conversions
    swellHeight = swellHeight * 3.28084
    windSpeed = windSpeed * 2.23694
    rows = []
    for j in range(columns):
      if j == 0:
        rows.append(currHour)
      if j == 1:
        rows.append(swellHeight)
      if j == 2:
        rows.append(swellDirection)
      if j == 3:
        rows.append(swellPeriod)
      if j == 4:
        rows.append(windSpeed)
      if j == 5:
        rows.append(windDirection)
    arr.append(rows)
    currHour = currHour + 1

  return arr

# comment on current conditions
# send tweet containing conditions and comments on surfability
# rating system is 0-30, with each category being 0-5
# exceptions: swell size with 0-10 rating (can't surf ankle high!)
def makeTweet(dataTable):
  time = 'err'
  swellHeight = 'err'
  swellDirection = 'err'
  swellPeriod = 'err'
  windSpeed = 'err'
  windDirection = 'err'
  comment = "💩💩💩💩💩"

  rating = 0
  for i in range(15):
    for j in range(6):
      if j == 0:
        time = int(dataTable[i][0])
      # -------------------------------------------------------------------------------
      if j == 1:
        swellHeight = dataTable[i][1]
        # flat
        if swellHeight <= 1.0:
          rating += 0
        # minimal surf
        elif swellHeight <= 2.0:
          rating += 2
        # ~waist high
        elif swellHeight <= 3.0:
          rating += 6
        # waist - overhead
        elif swellHeight <= 10.0:
          rating += 10
        # 10ft+ too big, storm/hurricane, not worth it
        else:
          rating += 0
      # -------------------------------------------------------------------------------
      if j == 2:
        swellDirection = dataTable[i][2]
        # N
        if swellDirection < 11.25 or swellDirection > 348.75:
          rating += 0
          swellDirection = 'N'
        # NNE
        elif swellDirection < 33.75:
          rating += 0
          swellDirection = 'NNE'
        # NE
        elif swellDirection < 56.25:
          rating += 0
          swellDirection = 'NE'
        # ENE
        elif swellDirection < 78.75:
          rating += 0
          swellDirection = 'ENE'
        # E
        elif swellDirection < 101.25:
          rating += 0
          swellDirection = 'E'
        # ESE
        elif swellDirection < 123.75:
          rating += 1
          swellDirection = 'ESE'
        # SE
        elif swellDirection < 146.25:
          rating += 2
          swellDirection = 'SE'
        # SSE
        elif swellDirection < 168.75:
          rating += 3
          swellDirection = 'SSE'
        # S
        elif swellDirection < 191.25:
          rating += 5
          swellDirection = 'S'
        # SSW
        elif swellDirection < 213.75:
          rating += 3
          swellDirection = 'SSW'
        # SW
        elif swellDirection < 236.25:
          rating += 2
          swellDirection = 'SW'
        # WSW
        elif swellDirection < 258.75:
          rating += 1
          swellDirection = 'WSW'
        # W
        elif swellDirection < 281.25:
          rating += 1
          swellDirection = 'W'
        # WNW
        elif swellDirection < 303.75:
          rating += 0
          swellDirection = 'WNW'
        # NW
        elif swellDirection < 326.25:
          rating += 0
          swellDirection = 'NW'
        # NNW
        elif swellDirection <= 348.75:
          rating += 0
          swellDirection = 'NNW'
      # -------------------------------------------------------------------------------
      if j == 3:
        swellPeriod = dataTable[i][3]
        # windswell
        if swellPeriod < 5.0:
          rating += 2
        # lil groundswell/decent windswell
        elif swellPeriod < 8.0:
          rating += 3
        # sweet spot
        elif swellPeriod < 12.0:
          rating += 5
        # hurricane, might not hold but good period
        elif swellPeriod < 14.0:
          rating += 4
        # might be a tsunami lol GTFO
        else:
          rating += 0
      # -------------------------------------------------------------------------------
      if j == 4:
        windSpeed = dataTable[i][4]
        # glassy
        if windSpeed < 5.0:
          rating += 5
        # groomed
        elif windSpeed < 10.0:
          rating += 4
        # breezy
        elif windSpeed < 20.0:
          rating += 2
        # blowin
        elif windSpeed < 30.0:
          rating += 1
        # bloke its howling!
        else:
          rating += 0
      # -------------------------------------------------------------------------------
      if j == 5:
        windDirection = dataTable[i][5]
        # N
        if windDirection < 11.25 or windDirection > 348.75:
          rating += 5
          windDirection = 'N'
        # NNE
        elif windDirection < 33.75:
          rating += 5
          windDirection = 'NNE'
        # NE
        elif windDirection < 56.25:
          rating += 4
          windDirection = 'NE'
        # ENE
        elif windDirection < 78.75:
          rating += 3
          windDirection = 'ENE'
        # E
        elif windDirection < 101.25:
          rating += 1
          windDirection = 'E'
        # ESE
        elif windDirection < 123.75:
          rating += 1
          windDirection = 'ESE'
        # SE
        elif windDirection < 146.25:
          rating += 0
          windDirection = 'SE'
        # SSE
        elif windDirection < 168.75:
          rating += 0
          windDirection = 'SSE'
        # S
        elif windDirection < 191.25:
          rating += 1
          windDirection = 'S'
        # SSW
        elif windDirection < 213.75:
          rating += 0
          windDirection = 'SSW'
        # SW
        elif windDirection < 236.25:
          rating += 0
          windDirection = 'SW'
        # WSW
        elif windDirection < 258.75:
          rating += 1
          windDirection = 'WSW'
        # W
        elif windDirection < 281.25:
          rating += 1
          windDirection = 'W'
        # WNW
        elif windDirection < 303.75:
          rating += 3
          windDirection = 'WNW'
        # NW
        elif windDirection < 326.25:
          rating += 4
          windDirection = 'NW'
        # NNW
        elif windDirection <= 348.75:
          rating += 5
          windDirection = 'NNW'

    if rating <= 13:
      comment = '💩💩💩💩💩'
    elif rating <= 18:
      comment = '🌊💩💩💩💩'
    elif rating <= 22:
      comment = '🌊🌊💩💩💩'
    elif rating <= 25:
      comment = '🌊🌊🌊💩💩'
    elif rating <= 28:
      comment = '🌊🌊🌊🌊💩'
    else:
      comment = '🌊🌊🌊🌊🌊'
    hrs = 'am'
    if time > 12:
      time = time - 12
      hrs = 'pm'

    # Twitter mobile allows ~40 characters per line
    tweet = ('Time: ' + str(time) + hrs + '       Date: ' + date + '\n' 
             'Surf: %.1f' % (swellHeight) + 'ft  ' + str(swellDirection) + '  ' + str(swellPeriod) + 'sec\n'
             'Winds: %.2f' % (windSpeed) + 'mph  ' + str(windDirection) + '  \n'
             'Rating: ' + comment)
    twitterbotdemo.postTweet(tweet)
    print(tweet)
    print(' ')
    rating = 0

  return


def main():
  response = getJSONResponse()
  if response == -1:
    return 126

  dataTable = []
  dataTable = parseResponse(response)

  tweet = makeTweet(dataTable)

  return

if __name__ == "__main__":
    main()
