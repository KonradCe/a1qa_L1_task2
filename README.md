## Level 1 - task 2
> a1qa study project

Basic navigating through [store.steampowered.com](https://store.steampowered.com/ "store.steampowered.com") page with Selenium and python, implementing simple Page Object Model.

###### test case 1

|  step | expected result  |
| ------------ | ------------ |
|  Go to store.steampowered.com page | store.steampowered.com is open  |
| Click on ABOUT button  | About page is open  |
| Compare number of players online and in-game  | Number of in-game players is less than number of players online  |
| Click on STORE button  | Store page is open  |


###### test case 2

| step  | expected result   |
| ------------ | ------------ |
| navigate to store page  | Store page is open  |
| Select 'Top Sellers' from top dropdown menu	 | Page with Top Sellers products is open  |
|  In menu on the right choose Action', 'LAN Co-op' and 'SteamOS + Linux' checkboxes |  All three checkboxes are checked; Number of results matching your search equals to number of games in games list|
| From list get first game's name, release date and price  |  -  |
|  Click on the first game in the list |  page with game's description is open; Game's data (name, release date and price) are match those in step #6 |
