package org.lenskit.mooc.cbf;

import org.lenskit.data.ratings.Rating;

import javax.annotation.Nonnull;
import javax.inject.Inject;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Build a user profile from all positive ratings.
 */
public class ThresholdUserProfileBuilder implements UserProfileBuilder {
    /**
     * The lowest rating that will be considered in the user's profile.
     */
    private static final double RATING_THRESHOLD = 3.5;

    /**
     * The tag model, to get item tag vectors.
     */
    private final TFIDFModel model;

    @Inject
    public ThresholdUserProfileBuilder(TFIDFModel m) {
        model = m;
    }

    @Override
    public Map<String, Double> makeUserProfile(@Nonnull List<Rating> ratings) {
        // Create a new vector over tags to accumulate the user profile
        Map<String, Double> profile = new HashMap<>();

        // Iterate over the user's ratings to build their profile
        for (Rating r : ratings) {
            if (r.getValue() >= RATING_THRESHOLD) {
                long itemId = r.getItemId();
                Map<String, Double> itemVector = model.getItemVector(itemId);

                for (String termKeyword : itemVector.keySet()) {
                    double newValue = profile.containsKey(termKeyword) ?
                            profile.get(termKeyword) + itemVector.get(termKeyword) :
                            itemVector.get(termKeyword);
                    profile.put(termKeyword, newValue);
                }
            }
        }

        // The profile is accumulated, return it.
        return profile;
    }
}
