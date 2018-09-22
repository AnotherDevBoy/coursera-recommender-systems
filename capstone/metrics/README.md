# TODO
- [x] Implement Serendipity (Intersection of the unexpected items with the relevant items divided by the number of items recommended)
- [x] Implement nDCG
- [x] Item Relevance is based on user average rating
- [x] Implement Category Diversity metric
- [x] Refactor metrics into different files
- [ ] Output Top N per User/Algorithm to files
- [ ] Improve Price Category based on price distribution
- [ ] Implement personalization metric (average difference in top N lists across users)


# Supported Metrics
## Business driven constraints
### Average Product Availability
This metric goes through all the top-N list of recommended items for each users and:
- Calculates the average availability for the list.
- Uses that information to calculate the average of all the top-N lists.


# Sources
- [Recommender Systems — It’s Not All About the Accuracy](https://gab41.lab41.org/recommender-systems-its-not-all-about-the-accuracy-562c7dceeaff)
