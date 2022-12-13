# Qatar22Sim  
###### A simple model for 2022 FIFA World Cup in Qatar  


### The Model  
The goal was to build a model of the 2022 FIFA World Cup in Qatar using real-world data derived 
from player's recent club performances. It would follow the pre-arranged determination of teams and 
groups and use the final squad rosters released the week before the competition starts. It would follow the 
standard World Cup format of three group stage matches, with the two leaders in points advancing to the 
knockout round, where the matches follow this arbitrary arrangement: <something.com>. Individual matches 
would be simulated by calculating a weighted probability based on some performance data of individual 
players.


### The Data  
I wanted to use data that reflected the recent performance of each individual player at the club level - 
ideally in the past 12 months. Given the nature of the competition, where players at world famous clubs 
might play against those in obscure clubs, a source would be required that included data on all players, 
not only the ones who play in famous leagues. Although data may not have been available for every single 
player, in order for the model to not be skewed against the more obscure players, it could only omit a 
statistically insignificant number of players. Additionally, all player data should come from the same 
source - in that case there would be some implicit standardization - no discrepancy between the way 
different websites or other sources codifed the data.

### The Results
The model would simulate this year's World Cup 10,000 times while recording the results of each individual
run - how many matches each team won, how many points they got in the group stage, and what stage of the 
competition they exited at. To evaluate the results, an average was calculated for the numerical metrics -
average wins and average points in the group stage. And to track the success of each team, a percentage 
distribution was calculated to show how often each team was eliminated at each stage of the competition.

### Other Notes
Mathematically, the model was quite basic. Rather than seeking to be truly predictive of the winner of 
this year's World Cup, it was meant to practice building the model and incorporating some real-world data 
to influence results. If I had been seeking to build a more authentic model, I would have collected and 
incorporated much more player data. I would also have found similar historical data from World Cup years, 
run the model with it and then honed the model by comparing the results of each run with the known 
historical results of that World Cup. I also could improve this model's utility by adding code to collect 
and save much more data during the simulations than this iteration will.


## Process

### Step 1a: Find the data  
The main obstacle of this project was to find appropriate data fitting the needs described above - if a 
minimum acceptable amount of player data was not available, there was no point in running a simulation. 
A Wikipedia page <https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads> contained the roster of each 
team fairly soon after each squad was released to the public and, as a static website, it was relatively 
simple to scrape. From this page I retrieved player name, position, and the club and country they play 
in professionally. After collecting this information I would be able to then collect match data for 
these specific players across the world, as soon as I found one source to get it from.

### Step 2: Build the model  
The model adheres to the standard format of the World Cup as described above with the following more 
specific design choices:

* *If the result of a tie is reached in the knockout stages, the exact same process repeats until a winner \
  is given by the draw.*

* *The group results are found by placing the team objects in a list and using the list sort function to \
  sort by points. In the case of a tie on points between the second and third teams, the first team of the \
  two, i.e. the second index in the list, is chosen (alphabetically) as the runner up regardless.*

* *The traditional third place match is not simulated or recorded in this model.*

* *No specific data is recorded from group stage matches besides adding points and registering a win.*

##### Match Simulation
The model derives a score for each team based on a calculation that makes use of a value from each player 
on that particular teams roster. The weighting of these values can be edited in the squads.py file to 
tweak the model. I later added a defense metric to the Team class which is also added to each team's 
score when simulating the match. After these scores have been calculated, as well as a value to represent 
the proportional chance of a tie, a random number is drawn to choose the winner according to the 
distribution of the aforementioned values. For more details see main.py.

### Step 1b: Find match data for players
Transfermarkt.us was the website I found that had a page for nearly all the players on my list. Using the 
initial data I got by scraping Wikipedia, I identified a handful of players who did not play in European 
leagues - these would be the more difficult players to find data on. I chose a handful of these players 
from the squads of Iran, Australia, Qatar, Japan and Costa Rica to manually query, thereby confirming
that this source was appropriate in that it would include some data for all players. I built a new method
into my scraper and ran it, saving results to one file and logging errors in another. My error file 
revealed 44 players for whom no data was found out of a total of 832 players.

### Step 3: Clean the data and make calculations for player influence
The first thing I noticed from the error file was that it included the entire South Korean team. I 
identified the problem with the scraper by manually querying some names and then wrote a new method to 
collect the data for Korean players specifically (see qatarsquadscraper.py). That left 18 remaining 
players without data. These I manually queried on Transfermarkt.us. Most of them had given errors due to 
a slight spelling difference or an unexpected order of query results which made my program scrape the 
wrong data for those entries. I found the correct page and manually added the data for those players, 
after which there were only 3 players for whom no data could be found, an amount which would have no 
affect on the outcome of the simulation.  

After all data was collected, I cleaned it in a spreadsheet, verifying that the values were formatted
uniformly in each column. I also noticed that for some players my scraper had retrieved career 
statistics instead of those only for the current year. I manually queried those to find that for some
players the career statistics were the only statistics available. Because the influence of players in the
model was going to be dictated by a rate derived from match data (i.e. Goals involvements per 90 
minutes), using the career statistics would not have any confounding affect on the results of the model.
I calculated the relevant rates in the spreadsheet and then saved it as a csv for use in the model.

### Step 4: Run simulations and tweak the match algorithm


 
