package org.lenskit.mooc.uu;

import it.unimi.dsi.fastutil.longs.Long2DoubleMap;
import it.unimi.dsi.fastutil.longs.Long2DoubleOpenHashMap;
import org.lenskit.util.math.Vectors;

import java.util.Map;

public class UserRatingData {
    private long userId;
    private Long2DoubleOpenHashMap userRatings;
    private double averageUserRating;

    public UserRatingData(long userId, Long2DoubleOpenHashMap userRatings) {
        this.userId = userId;
        this.userRatings = userRatings;

        this.calculateAverageUserRating();
    }

    public void addRating(long itemId, double value) {
        this.userRatings.addTo(itemId, value);
        this.calculateAverageUserRating();
    }

    public boolean hasRated(long itemId) {
        return this.userRatings.containsKey(itemId);
    }

    public Long2DoubleOpenHashMap getUserRatings() {
        return this.userRatings;
    }

    public double getAverageRating() {
        return this.averageUserRating;
    }

    public Long2DoubleMap getMeanCenteredUserRatings() {
        Long2DoubleMap meanCeneteredUserRatings = new Long2DoubleOpenHashMap();

        for (Map.Entry<Long, Double> rating : this.userRatings.entrySet()) {
            meanCeneteredUserRatings.put((long)rating.getKey(), rating.getValue() - this.averageUserRating);
        }

        return meanCeneteredUserRatings;
    }

    private void calculateAverageUserRating() {
        int ratingCount = 0;
        double ratingsSum = 0.0;

        for (long itemId : userRatings.keySet()) {
            ++ratingCount;
            ratingsSum += userRatings.get(itemId);
        }

        if (ratingCount > 0) {
            this.averageUserRating = ratingsSum / ratingCount;
        }
    }

    public static double calculateUserRatingsCosine(UserRatingData user1, UserRatingData user2) {
        Long2DoubleMap user1MeanCenteredRatings = user1.getMeanCenteredUserRatings();
        Long2DoubleMap user2MeanCenteredRatings = user2.getMeanCenteredUserRatings();

        return Vectors.dotProduct(user1MeanCenteredRatings, user2MeanCenteredRatings) /
                        (Vectors.euclideanNorm(user1MeanCenteredRatings) * Vectors.euclideanNorm(user2MeanCenteredRatings));
    }
}
