## Pre-requisites
Anaconda suite installed

## How to run
1. Open cmd
2. Run `jupyter notebook`

# Supported Metrics
## Availability
For a given user, this metric reflects the average availability of the products the list of recommended products.

To do so, it uses the availability field from the item database.

## Serendipity
For a given user, this metrics reflects the percentage of **serendipitous** products in the list of recommended products.

The serendipity of an item within the recommended list is a combination two concepts:
- Popularity: the percentage of users that rated an item.
- Relevance: the interest of a user towards a given item. We will consider that an user is interested on an item if he already rated the item and the value of the rating is above the user rating average.

An item will be considered **serendipitous** if it is relevant for the user but it is **NOT** popular.

> Note: an item will be considered popular if it was rated by 15% of users or more.

# Sources
- [Recommender Systems — It’s Not All About the Accuracy](https://gab41.lab41.org/recommender-systems-its-not-all-about-the-accuracy-562c7dceeaff)
