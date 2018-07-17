# TODO
- [ ] Output Top N per User/Algorithm in files
- [x] Implement Category Diversity metric
- [ ] Improve Price Category based on price distribution
- [x] Refactor metrics into different files
- [ ] Implement personalization metric (average difference in top N lists across users)
- [x] Implement Serendipity (Intersection of the unexpected items with the relevant items divided by the number of items recommended)
- [x] Implement nDCG
- [x] Item Relevance is based on user average rating

# Current Results

| Algorithm         | Avg Availability | Avg Price Diversity | Coverage |      MAP |      MRR | RMSE.Predict | RMSE.TopN |
--------------------|------------------|---------------------|----------|----------|----------|--------------|-----------|
| cbf.csv           |         0.585363 |              0.4240 |    0.205 | 0.023444 | 0.240167 |     0.598984 |  0.358918 |
| item-item.csv     |         0.613373 |              0.3216 |    0.530 | 0.056258 | 0.542333 |     0.584113 |  0.328124 |
| mf.csv            |         0.521616 |              0.4440 |    0.045 | 0.009378 | 0.123667 |     0.688283 |  0.382229 |
| perbias.csv       |         0.566868 |              0.4800 |    0.025 | 0.009073 | 0.114500 |     0.695627 |  0.496585 |
| user-user.csv     |         0.695152 |              0.3384 |    0.755 | 0.181251 | 1.330833 |     0.551891 |  0.323100 |

# Sources
- [Recommender Systems — It’s Not All About the Accuracy](https://gab41.lab41.org/recommender-systems-its-not-all-about-the-accuracy-562c7dceeaff)