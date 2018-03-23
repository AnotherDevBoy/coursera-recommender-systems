package org.lenskit.mooc.uu;

import com.google.common.collect.Maps;
import it.unimi.dsi.fastutil.longs.Long2DoubleMap;
import it.unimi.dsi.fastutil.longs.Long2DoubleOpenHashMap;
import it.unimi.dsi.fastutil.longs.Long2DoubleSortedMap;
import org.lenskit.api.Result;
import org.lenskit.api.ResultMap;
import org.lenskit.basic.AbstractItemScorer;
import org.lenskit.data.dao.DataAccessObject;
import org.lenskit.data.entities.CommonAttributes;
import org.lenskit.data.ratings.Rating;
import org.lenskit.results.BasicResultMap;
import org.lenskit.results.Results;
import org.lenskit.util.ScoredIdAccumulator;
import org.lenskit.util.TopNScoredIdAccumulator;
import org.lenskit.util.collections.LongUtils;
import org.lenskit.util.math.Scalars;
import org.lenskit.util.math.Vectors;

import javax.annotation.Nonnull;
import javax.inject.Inject;
import java.util.*;

/**
 * User-user item scorer.
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleUserUserItemScorer extends AbstractItemScorer {
    private final DataAccessObject dao;
    private final int neighborhoodSize;

    /**
     * Instantiate a new user-user item scorer.
     * @param dao The data access object.
     */
    @Inject
    public SimpleUserUserItemScorer(DataAccessObject dao) {
        this.dao = dao;
        neighborhoodSize = 30;
    }

    @Nonnull
    @Override
    public ResultMap scoreWithDetails(long userId, @Nonnull Collection<Long> items) {
        List<Result> results = new LinkedList<>();

        Map<Long, UserRatingData> allUserRatings = this.getAllUserRatingVectors();

        for (long itemId: items) {
            UserRatingData userRatingData = allUserRatings.get(userId);

            Map<Long, Double> neighbourCosines = new HashMap<>();

            for (Map.Entry<Long, UserRatingData> userRating : allUserRatings.entrySet()) {
                long neighbourId = userRating.getKey();
                UserRatingData neighbourRatingData = allUserRatings.get(neighbourId);

                // Only consider users that have rated the item
                if (userId != neighbourId && neighbourRatingData.hasRated(itemId)) {
                    double cosine = UserRatingData.calculateUserRatingsCosine(userRatingData, neighbourRatingData);

                    neighbourCosines.put(neighbourId, cosine);
                }
            }

            SortedMap<Long, Double> sortedNeighboursByCosine = new TreeMap<>(new UserRatingCosineComparer(neighbourCosines));
            sortedNeighboursByCosine.putAll(neighbourCosines);

            int count = 0;

            double neighboursInfluence = 0.0;
            double sumOfAllCosines = 0.0;
            //System.out.println("**************Begin**************");
            for (Map.Entry<Long, Double> neighbourSortedByCosine : sortedNeighboursByCosine.entrySet()) {
                if (count < this.neighborhoodSize) {
                    long neighbourId = neighbourSortedByCosine.getKey();
                    double cosine = neighbourSortedByCosine.getValue();

                    //System.out.printf("Size: %d - Item: %d - Neighbour ID: %d - Cosine: %f\n", this.neighborhoodSize, itemId, neighbourId, cosine);
                    UserRatingData neighbourRatingData = allUserRatings.get(neighbourId);

                    double neighbourAverageRating = neighbourRatingData.getAverageRating();
                    double neighbourRatingForItem =neighbourRatingData.getUserRatings().get(itemId);

                    neighboursInfluence += cosine*(neighbourRatingForItem - neighbourAverageRating);
                    sumOfAllCosines += neighbourSortedByCosine.getValue();
                    ++count;
                }
            }
            //System.out.println("**************End**************");

            double prediction = userRatingData.getAverageRating() + (neighboursInfluence / sumOfAllCosines);
            results.add(Results.create(itemId, prediction));
        }

        return Results.newResultMap(results);
    }

    private Map<Long, UserRatingData> getAllUserRatingVectors() {
        List<Rating> allRatings = this.dao.query(Rating.class).get();

        Map<Long, UserRatingData> allUserRatings = new HashMap<>();

        for (Rating r: allRatings) {
            long userId = r.getUserId();
            UserRatingData userRatingData;

            if (allUserRatings.containsKey(userId)) {
                userRatingData = allUserRatings.get(userId);
            } else {
                userRatingData = new UserRatingData(userId, new Long2DoubleOpenHashMap());
                allUserRatings.put(userId, userRatingData);
            }

            userRatingData.addRating(r.getItemId(), r.getValue());
        }

        return allUserRatings;
    }

    private class UserRatingCosineComparer implements Comparator<Long> {
        private Map<Long, Double> neighbourCosines;

        public UserRatingCosineComparer(Map<Long, Double> neighbourCosines) {
            this.neighbourCosines = neighbourCosines;
        }

        @Override
        public int compare(Long userId1, Long userId2) {
            if (this.neighbourCosines.get(userId1) <= this.neighbourCosines.get(userId2)) {
                return 1;
            } else {
                return -1;
            }
        }
    }
}
