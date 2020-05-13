# Atlantic-Beach-Surf-Report-Twitter-Bot
Evan Mason
May, 2020

Function:
Daily updates on surf conditions in Atlantic Beach, North Carolina. Updates are in the form of tweets, where each tweet is an hour between 6am and 8pm, inclusive. Surf data was provided by the stormglass.io maritime API, and tweets were sent using the Tweepy API. 

https://stormglass.io/

http://www.tweepy.org/

Packages used:<br />
tweepy<br />
requests<br />
arrow<br />
datetime<br />

How projected was automated:<br />
1. Made python script into an executable<br />
2. Use cron jobs to schedule when to run executable<br />
3. crontab -e -> # schedule tweets to send at 5am every day<br />
0 5 * * * python /Users/evanmason/PycharmProjects/untitled/surfData.py >> ~/Desktop/archive.txt  <br />
4. Each batch of daily tweets is sent at 5a.m. the day of<br />

Executable running in terminal with auto-date feature:
https://user-images.githubusercontent.com/65209454/81752618-cda32500-947f-11ea-97fb-7356098adbb7.png

Actual Twitter Page:
https://user-images.githubusercontent.com/65209454/81752641-db58aa80-947f-11ea-9767-ad18b34324eb.png

(Possible) Modifications Needed:
Currently watching surf conditions to ensure 'Rating Metric' is justified and accurate.
