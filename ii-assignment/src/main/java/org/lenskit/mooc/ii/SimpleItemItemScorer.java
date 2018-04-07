package org.lenskit.mooc.ii;

import it.unimi.dsi.fastutil.longs.Long2DoubleMap;
import it.unimi.dsi.fastutil.longs.Long2DoubleOpenHashMap;
import org.lenskit.api.Result;
import org.lenskit.api.ResultMap;
import org.lenskit.basic.AbstractItemScorer;
import org.lenskit.data.dao.DataAccessObject;
import org.lenskit.data.entities.CommonAttributes;
import org.lenskit.data.ratings.Rating;
import org.lenskit.results.Results;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Nonnull;
import javax.inject.Inject;
import java.util.*;
import java.util.stream.Collectors;

/**
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleItemItemScorer extends AbstractItemScorer {
    private final SimpleItemItemModel model;
    private final DataAccessObject dao;
    private final int neighborhoodSize;
    private static final Logger logger = LoggerFactory.getLogger(SimpleItemItemScorer.class);

    @Inject
    public SimpleItemItemScorer(SimpleItemItemModel m, DataAccessObject dao) {
        model = m;
        this.dao = dao;
        neighborhoodSize = 20;
    }

    /**
     * Score items for a user.
     * @param user The user ID.
     * @param items The score vector.  Its key domain is the items to score, and the scores
     *               (rating predictions) should be written back to this vector.
     */
    @Override
    public ResultMap scoreWithDetails(long user, @Nonnull Collection<Long> items) {
        Long2DoubleMap itemMeans = this.model.getItemMeans();
        Long2DoubleMap ratings = this.getUserRatingVector(user);

        List<Result> results = new ArrayList<>();

        for (long candidateItem: items) {
            double candateItemMeanRating = itemMeans.get(candidateItem);

            double numerator = 0.0;
            double denominator = 0.0;

            Long2DoubleMap similaritiesWithNeighbours = this.model.getNeighbors(candidateItem);
            Long2DoubleMap similaritiesWithNeighboursThatUserHasRated = new Long2DoubleOpenHashMap();

            for (long neighbour: similaritiesWithNeighbours.keySet()) {
                if (ratings.containsKey(neighbour)) {
                    similaritiesWithNeighboursThatUserHasRated.put(neighbour, similaritiesWithNeighbours.get(neighbour));
                }
            }

            // Take the top 20 most similar neighbours
            List<Double> top20ItemSimilarities = similaritiesWithNeighboursThatUserHasRated
                .values()
                .stream()
                .sorted(Comparator.reverseOrder())
                .limit(this.neighborhoodSize)
                .collect(Collectors.toList());

            for (long neighbour: similaritiesWithNeighboursThatUserHasRated.keySet()) {
                double similarity = similaritiesWithNeighboursThatUserHasRated.get(neighbour);

                if (top20ItemSimilarities.contains(similarity)) {
                    double userRating = ratings.get(neighbour);
                    double otherIteamMeanRating = itemMeans.get(neighbour);

                    //logger.info(String.format("User Rating: %f, Similar Item Mean Rating: %f. Similarity: %f. Candidate Item ID: %d. Similar Item ID: %d", userRating, otherIteamMeanRating, similarity, candidateItem, neighbour));
                    numerator += (userRating - otherIteamMeanRating) * similarity;
                    denominator += Math.abs(similarity);
                }
            }

            if (denominator > 0.0) {
                double score = candateItemMeanRating + (numerator/denominator);
                //logger.info(String.format("Candidate Item: %d. Numerator: %f. Denominator: %f. MeanRating: %f. Score: %f", candidateItem, numerator, denominator, candateItemMeanRating, score));
                results.add(Results.create(candidateItem, score));
            }
        }

        return Results.newResultMap(results);
    }

    /**
     * Get a user's ratings.
     * @param user The user ID.
     * @return The ratings to retrieve.
     */
    private Long2DoubleOpenHashMap getUserRatingVector(long user) {
        List<Rating> history = dao.query(Rating.class)
                                  .withAttribute(CommonAttributes.USER_ID, user)
                                  .get();

        Long2DoubleOpenHashMap ratings = new Long2DoubleOpenHashMap();
        for (Rating r: history) {
            ratings.put(r.getItemId(), r.getValue());
        }

        return ratings;
    }
}
