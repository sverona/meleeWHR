# Background and problem description
_Super Smash Bros. Melee_ (hereafter _SSBM_,) a fighting game originally
released in 2001, has recently experienced a resurgence in competitive play.
Major tournament series such as Genesis and Evolution regularly attract
upwards of 1,000 entrants [1], a scale otherwise unheard of for decade-old
games incapable of online play.

Melee It On Me (_MIOM_), the competitive community's primary governing body,
produces annual ranking lists of the 100 most skilled players, established by
panel vote. The accuracy of these lists and their methodology are highly
debated within the community at large. There have been many attempts at using
existing rating systems such as Elo and Glicko to generate comparable rankings,
but few are still publicly maintained, partially due to the scattered nature of
the available data. Further, these rankings (like their MIOM counterparts) are
produced at infrequent intervals from aggregated resuls. Thus, since the scene
lacks a formal competitive circuit, the task of ranking the top players
attending an upcoming tournament (e.g., for seeding purposes) falls mainly on
that tournament's organizers.

# Objectives
I propose to

i. consolidate the available tournament data, dating as far back as 2003-4,
into a publicly maintained dataset;
ii. use this dataset and a maximum-likelihood estimation method such as Whole-
History Rating (_WHR_) [2] to reconstruct real-time ratings for the period
comprising the earliest MLG tournaments in 2005-6 to the present day;
iii. use D3.js [3] to visualize these time-series in a manner similar to [4].

# Basic data model and project workflow
The data will consist primarily of match metadata from tournament brackets, as
shown in the code snippet below. This data will be cleaned and reformatted into
a format more appropriate for storage in a relational database, most likely
JSON or CSV.

The baseline schema (omitting unnecessary attributes) has the following tables:
  - TOURNAMENTS, having attribute `ID` and `date`;
  - MATCHES, having attributes `ID`, `bracket_ID`, `winner_ID`, `loser_ID`;
  - PLAYERS, having attribute `ID`;
  - MATCHES_PLAYERS, join table.

At the basic level, within this database, tournaments are ordered temporally
by their `date` attributes, while their brackets are ordered temporally by the
match attributes `winner_ID` and `loser_ID`, which contain the IDs of the
matches the winner and loser of that match play next. `loser_ID` is `NULL` only
if the loser is eliminated from the tournament; `winner_ID` is `NULL` only if
the winner of the match is the winner of the tournament.

The primary question of interest is to derive a stable measure of player skill
from the sequence of match records. One method of doing so that has been
adopted by other e-sports communities is TrueSkill [5], which assumes that player
skill before any given match follows a Gaussian distribution. The probability
of one player defeating another is then the probability that a randomly
sampled value from the former's distribution exceeds one from the latter's.



# Sample data format
Currently, the data is primarily stored on sites such as Liquipedia [6] in a
markup format. The following snippet (sourced from [7]) contains the match data
from three sets between top-level players at the tournament Shine 2017:

```
|l1m1p1=PewPewU |l1m1p1flag=us |l1m1p1score=3
|l1m1p2=Trif |l1m1p2flag=es |l1m1p2score=2
|l1m1win=1
|l1m1p1char1=marth |l1m1p2char1=peach |l1m1p1stock1= |l1m1p2stock1=0 |l1m1win1=1 |l1m1stage1=Unknown
|l1m1p1char2=marth |l1m1p2char2=peach |l1m1p1stock2= |l1m1p2stock2=0 |l1m1win2=1 |l1m1stage2=Unknown
|l1m1p1char3=marth |l1m1p2char3=peach |l1m1p1stock3=0 |l1m1p2stock3=1 |l1m1win3=2 |l1m1stage3=Dream Land
|l1m1p1char4=marth |l1m1p2char4=peach |l1m1p1stock4=0 |l1m1p2stock4=1 |l1m1win4=2 |l1m1stage4=Yoshi's Story
|l1m1p1char5=marth |l1m1p2char5=peach |l1m1p1stock5=1 |l1m1p2stock5=0 |l1m1win5=1 |l1m1stage5=Pokémon Stadium
|l1m1date=August 26, 2017
|l1m1details={{BracketMatchDetails|reddit=|comment=|vod=}}

|l1m2p1=Westballz |l1m2p1flag=us |l1m2p1score=3
|l1m2p2=Lucky |l1m2p2flag=us |l1m2p2score=0
|l1m2win=1
|l1m2p1char1=falco |l1m2p2char1=fox |l1m2p1stock1=1 |l1m2p2stock1=0 |l1m2win1=1 |l1m2stage1=Battlefield
|l1m2p1char2=falco |l1m2p2char2=fox |l1m2p1stock2=2 |l1m2p2stock2=0 |l1m2win2=1 |l1m2stage2=Dream Land
|l1m2p1char3=falco |l1m2p2char3=fox |l1m2p1stock3=1 |l1m2p2stock3=0 |l1m2win3=1 |l1m2stage3=Pokémon Stadium
|l1m2details={{BracketMatchDetails|vod=https://www.youtube.com/watch?v=4bMa_nRjC3E|comment=}}

|l1m3p1=S2J |l1m3p1flag=us |l1m3p1score=3
|l1m3p2=HugS |l1m3p2flag=us |l1m3p2score=1
|l1m3win=1
|l1m3p1char1=cf |l1m3p2char1=samus |l1m3p1stock1=0 |l1m3p2stock1=1 |l1m3win1=2 |l1m3stage1=Yoshi's Story
|l1m3p1char2=cf |l1m3p2char2=samus |l1m3p1stock2=1 |l1m3p2stock2=0 |l1m3win2=1 |l1m3stage2=Pokémon Stadium
|l1m3p1char3=cf |l1m3p2char3=samus |l1m3p1stock3=2 |l1m3p2stock3=0 |l1m3win3=1 |l1m3stage3=Yoshi's Story
|l1m3p1char4=cf |l1m3p2char4=samus |l1m3p1stock4=3 |l1m3p2stock4=0 |l1m3win4=1 |l1m3stage4=Yoshi's Story
|l1m3date=August 26, 2017
|l1m3details={{BracketMatchDetails|reddit=|comment=|vod=https://www.youtube.com/watch?v=7zTSvNM-E1c}}
```

# References
[1] https://www.ssbwiki.com/List_of_largest_Smash_tournaments
[2] https://www.remi-coulom.fr/WHR/WHR.pdf
[3] https://d3js.org/
[4] https://www.youtube.com/watch?v=z2DHpW79w0Y
[5] http://liquipedia.net/smash/Main_Page
[6] http://liquipedia.net/smash/index.php?title=Shine/2017/Melee/Singles_Bracket&action=edit&section=4
[7] https://papers.nips.cc/paper/3331-trueskill-through-time-revisiting-the-history-of-chess.pdf
