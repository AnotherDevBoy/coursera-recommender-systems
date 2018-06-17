package org.lenskit.mooc.hybrid;

import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.RealVector;
import org.lenskit.api.ItemScorer;
import org.lenskit.api.Result;
import org.lenskit.api.ResultMap;
import org.lenskit.bias.BiasModel;
import org.lenskit.bias.UserBiasModel;
import org.lenskit.data.ratings.Rating;
import org.lenskit.data.ratings.RatingSummary;
import org.lenskit.inject.Transient;
import org.lenskit.util.ProgressLogger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.inject.Inject;
import javax.inject.Provider;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Trainer that builds logistic models.
 */
public class LogisticModelProvider implements Provider<LogisticModel> {
    private static final Logger logger = LoggerFactory.getLogger(LogisticModelProvider.class);
    private static final double LEARNING_RATE = 0.00005;
    private static final int ITERATION_COUNT = 100;

    private final LogisticTrainingSplit dataSplit;
    private final BiasModel baseline;
    private final RecommenderList recommenders;
    private final RatingSummary ratingSummary;
    private final int parameterCount;
    private final Random random;

    @Inject
    public LogisticModelProvider(@Transient LogisticTrainingSplit split,
                                 @Transient UserBiasModel bias,
                                 @Transient RecommenderList recs,
                                 @Transient RatingSummary rs,
                                 @Transient Random rng) {
        dataSplit = split;
        baseline = bias;
        recommenders = recs;
        ratingSummary = rs;
        parameterCount = 1 + recommenders.getRecommenderCount() + 1;
        random = rng;
    }

    @Override
    public LogisticModel get() {
        List<ItemScorer> scorers = recommenders.getItemScorers();
        double intercept = 0;
        double[] params = new double[parameterCount];

        LogisticModel current = LogisticModel.create(intercept, params);

        List<Rating> ratings = this.dataSplit.getTuneRatings();

        long[] users = ratings.stream().mapToLong(rating -> rating.getUserId()).distinct().toArray();
        List<Long> items = ratings.stream().map(rating -> rating.getItemId()).distinct().collect(Collectors.toList());

        Map<Long, Map<Long,RealVector>> scoresByUser = new HashMap<>();

        for (long userId : users) {
            double[] x = new double[recommenders.getRecommenderCount()+2];

            Map<Long, RealVector> scoresForItem = new HashMap<>();

            for (long itemId : items) {
                double bias = this.baseline.getIntercept() + this.baseline.getUserBias(userId) + this.baseline.getItemBias(itemId);

                // x1 is the bias bui from the bias model
                x[0] = bias;

                // x2 is the log popularity of the item, log10|Ui| (get this from the rating summary)
                x[1] = Math.log10(ratingSummary.getItemRatingCount(itemId));

                for (int i = 0; i < scorers.size(); ++i) {
                    ItemScorer scorer = scorers.get(i);
                    Result score = scorer.score(userId, itemId);
                    x[i+2] = score == null ? 0.0 : score.getScore();
                }

                scoresForItem.put(itemId, new ArrayRealVector(x));
            }

            scoresByUser.put(userId, scoresForItem);
        }

        RealVector coefficients = current.getCoefficients();

        for (int iteration = 0; iteration < ITERATION_COUNT; iteration++) {
            Collections.shuffle(ratings, random);

            for (Rating rating : ratings) {
                RealVector  allScores = scoresByUser.get(rating.getUserId()).get(rating.getItemId());
                double delta_intercept = LEARNING_RATE*rating.getValue()*current.evaluate(-rating.getValue(), allScores);

                intercept += delta_intercept;

                for(int i = 0; i < params.length; i++) {
                    params[i] += delta_intercept * allScores.getEntry(i);
                    coefficients.setEntry(i, params[i]);
                }

                current = new LogisticModel(intercept, coefficients);
            }
        }

        return current;
    }

}
