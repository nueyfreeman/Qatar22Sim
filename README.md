# Qatar22Sim  
###### A simple model for 2022 FIFA World Cup in Qatar  


### The Model  
The goal was to build a model of the 2022 FIFA World Cup in Qatar using real-world data derived from 
player's recent club performances, following the pre-decided grouping of teams and using the final squad 
rosters released the week before the competition starts. (See this [link](https://www.foxsports.com/soccer/2022-fifa-world-cup/bracket) 
for more detail on the bracketing of matches after the group stage.) Individual matches would be simulated 
by calculating a weighted probability based on some performance data of individual players.


### The Data  
I wanted to use data that reflected the recent performance of each individual player at the club level - 
ideally in the past 12 months. Given the nature of the competition, where players at world famous clubs 
might play against those in obscure clubs, a source would be required that includes data on all players, 
not only the ones who play in famous leagues. Although data may not be available for every single player, 
in order for the model to not favor more famous players, it could only omit a statistically insignificant 
number of them. Additionally, all player data needed to come from the same source - in that case there 
would be some implicit standardization - no discrepancy between the way the data was codified in different
sources.

### The Results
The model would simulate this year's World Cup 10,000 times while recording the results each time - how 
many matches each team won, how many points they got in the group stage, and what stage of the competition 
they exited at. To evaluate the results, an average was calculated for the numerical metrics - average 
wins and average points in the group stage. And to track the overall success of each team, a percentage 
distribution was calculated to show how often each team made it to each stage of the competition.

### Other Notes
Mathematically, the model is basic. Rather than seeking to be truly predictive of the winner of this 
year's World Cup, or a rigorous academic exercise, it was meant to practice building a model and 
incorporating some real-world data to influence results. If I had been seeking to build a more advanced 
model, I would have collected and incorporated much more player data and used a more advanced method to 
simulate games. I would also have found similar historical data from World Cup years, run the model with 
it and then honed the model by comparing the results of each run with the known historical results of that 
World Cup. Another improvement would be to add code to collect and save much more data during the 
simulation than this iteration will and to do more complex analysis with the results.


## Process

### Step 1a: Find the data  
The main obstacle of this project was to find appropriate data fitting the needs described above - if a 
minimum amount of player data were not available, the results could not suggest how the current form of 
players could affect their teams success. A Wikipedia [page](https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads) 
contained the roster of each team fairly soon after each squad was released to the public and is 
relatively simple to scrape. From this page I retrieved player name, position, and the club and country 
they play in professionally. After collecting this information I would be able to then collect match data 
for these specific players across the globe, as soon as I found one source to get it from.

### Step 2: Build the model  
The model adheres to the standard format of the World Cup as described above with the following more 
specific design choices:

* *If the result of a tie is reached in the knockout stages, the exact same process repeats until a winner
  is given by the random draw (see Match Simulation below).*

* *The group results are found by placing the team objects in a list and using the list sort function to
  sort by points. In the case of a tie on points between the second and third teams, the first team of the
  two, i.e. the second index in the list, is chosen (alphabetically) as the runner up. A more authentic 
  model might simulate and store the scores of games so this can be decided by goal differential instead.*

* *The traditional third place match is not simulated or recorded in this model.*

* *No specific data is recorded from group stage matches besides adding points and registering a win.*

##### Match Simulation
The model derives a numerical value for each team using a calculation that includes data from each player 
on that particular teams roster. The weighting of these inputs can be edited in the `squads.py` file to 
adjust the model. I later added a defense metric to the Team class which is also combined in each team's 
value when simulating the match. After these have been calculated, as well as a value to represent the 
proportional chance of a tie, a random number is drawn to choose the winner according to the proportional 
distribution of the aforementioned values. For more details see `main.py`.

### Step 1b: Find match data for players
The website [Transfermarkt.us](https://www.transfermarkt.us/) had a page for nearly all the players on my 
list. Most players had a page dedicated to their match statistics which contained a table of their match 
data from all competitions in the 2022/2023 football season. Using the initial data I got by scraping 
Wikipedia, I identified a handful of players who did not play in European leagues - these would be the 
more difficult players to find data on. I chose a handful of these players from the squads of Iran, 
Australia, Qatar, Japan and Costa Rica to manually query, thereby confirming that this source was 
appropriate in that it would include data for all players regardless of their professional league. I built 
a new method into my webscraper and ran it, saving results to one file and logging errors in another. My 
error file revealed 44 players for whom no data was found out of a total of 832 players.

### Step 3: Clean the data and make calculations for player influence
The first thing I noticed from the error file was that it included the entire South Korean team. I 
identified the problem by manually querying some names and then wrote a new method to collect the data for 
Korean players specifically (see `qatarsquadscraper.py`). That left 18 remaining players without data. 
These I manually queried on Transfermarkt.us. Most of them had resulted in errors due to a slight spelling 
difference or an unexpected ordering of the results, which made my program find the wrong page for those 
entries. I found the correct page and manually added the data for those players, after which there were 
only 3 players for whom no data could be found, an amount which would not confound the outcome of the 
simulation.  

After all data was collected, I cleaned it in a spreadsheet, verifying that the values were formatted
uniformly in each column. I also noticed that for some players my webscraper had retrieved career 
statistics instead of those only for the current year. I manually queried those to find that for some
players the career statistics were the only statistics available. Because the influence of players in the
model was going to be dictated by match data given as a rate (i.e. Goal involvements per 90 minutes), 
using the career statistics would not have any confounding affect on the results of the simulation. I 
calculated the relevant rates in the spreadsheet and then saved it as a csv for use in `main.py`.

### Step 4: Run simulations
When I run the simulation I can save two files. One is for the results for each team (average wins, 
average points and exit stage). The other is to record the strength of each team and player with the
influence weighting that I used for that simulation. I used this second file to see exactly what values
were influencing the results of the simulation and on the basis of that, decided to add the data from 
the qualifying matches to the simulation to represent the influence of defense, as well as deemphasize 
the influence of players who had been in less than 5 games recently. For an example of this see 
`Influence_Example.png`.

### Step 5: Analyzing the results
The result file as it was initially configured (it can be changed of course) gives a distribution showing 
what percentage of the time each team exited at each stage of the competition. By opening this file in a 
spreadsheet and combining the appropriate fields, I can produce a chart showing the percentage chance that 
each team had of making it to each particular stage of the competition based on my model. For an example, 
see `Example_Results.png`. By reconfiguring the output of the results file, it would be possible to do 
much more robust analysis of the model using Python, R and/or SQL, but for the simple purpose of taking a 
look at how the model compares to the now finalized real-world results, it serves well - the teams with 
the highest chance of making it to a certain round are the teams predicted by the model to be in that 
round.

## Insights

Using the player data I scraped in this exercise, I had made a [simple graphic in Tableau](https://public.tableau.com/views/Qatar2022PlayerstoWatch/Top30PlayerstoWatch?:language=en-US&:display_count=n&:origin=viz_share_link) 
showing the most in-form players coming into the tournament. Unsurprisingly, this showed the expected 
excellence of top players like Lionel Messi and Kylian Mbappe, as well as foreshadowing the impact of 
some lesser known players who did well, like Enner Valencia and Cody Gakpo. In retrospect, it can deliver 
some ironic insights as well, such as highlighting Walid Cheddira, who failed to score in several 
one-on-ones with the goalkeeper in the latter stages of competition.

Based on the results of the model itself, it is fair to say that the current form of players can be a 
partial, but incomplete, predictor of World Cup success. Germany was the consistent favorite to win based 
on the model, but failed to make it out of the group stage in the real life competition. However, with the 
inclusion of defensive data from qualifying and appropriately weighting the influence of players, the top
performing teams in the model overall comprised most of the top performing teams in the actual competition. 
In the simulation that gave the results shown by `Example_Results.png`, the model failed to predict the 
winner, the final, and only found 1 out of 4 semifinalists, but it did accurately predict 10 out of 16 
teams in the Round of 16 and got 7 out of 8 quarterfinalists, including Morocco, who were the cinderella 
story of the real life tournament.

The organization of this model leaves the door open for much more advanced mathematical modeling of matches
and more complicated insights and data collection along the way. But for this year's World Cup, it predicted 
the real life champion, Argentina, to be the seventh most likely team to win it all. Congratulations Messi!
