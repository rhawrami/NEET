# NEETs in the US

By Ravan Hawrami

## What is a NEET

A NEET, typically [defined as](https://en.wikipedia.org/wiki/NEET) a young individual who is "**not in education, employment or training**," has been a social subject that gained heightened interest fairly recently. There is a popular notion of a man in his 20's living in his mother's basement, grinding League of Legends (or CSGo or Valorant or COD or whatever other free-to-play online game you like) for hours on end, day after day ad infinitum, all the while somehow fairing fine financially (perhaps government aid or the benevolence of his mother, etc.). See the [recent comments](https://www.youtube.com/watch?v=cQb1JFwI9Uo) from U.S. Speaker of the House Mike Johnson on "29 year-old males sitting on their couches playing video games" using Medicaid to sustain their slovenly lifestyles. 

What is the number of young men sitting on their couches playing video games, and is this a current (and growing) issue that we should tackle in the U.S.? In this project, I set out to attempt solving this, at the least applying some basic rigor to this topic.

## Data

The data used in this project comes from the Integrated Public Use Microdata Series, or [IPUMS](https://www.ipums.org/). IPUMS hosts data from a number of national microdata series, namely the Census Current Population Survey and American Community Survey. Accessing the IPUMS API requires an API key. To get a key, first create an [account](https://uma.pop.umn.edu/cps/user/new), then generate [a key](https://account.ipums.org/api_keys). Set your key as an environmental variable.

## Research

Research is contained in the [notebooks](notebooks/) folder, which includes four chapters (as of this version):

- [Chapter 00: Preface](notebooks/ch00_preface.ipynb): a motivation for studying NEETs and a brief look at international NEET data
- [Chapter 01: Single-Year Analysis](notebooks/ch01_singleyear.ipynb): a first look at American NEETs, using Census Current Population Survey data from 2024
- [Chapter 02: Time Trends](notebooks/ch02_timetrends.ipynb): a similar format to the previous chapter, but now including time trends
- [Chapter 03: Characteristics](notebooks/ch03_characteristics.ipynb): a deeper look into the socioeconomic and other demographic characteristics and qualities of American NEETs.