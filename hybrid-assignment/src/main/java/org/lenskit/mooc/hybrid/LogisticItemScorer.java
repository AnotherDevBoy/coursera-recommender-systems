package org.lenskit.mooc.hybrid;

import it.unimi.dsi.fastutil.longs.LongSet;
import org.lenskit.api.ItemScorer;
import org.lenskit.api.Result;
import org.lenskit.api.ResultMap;
import org.lenskit.basic.AbstractItemScorer;
import org.lenskit.bias.BiasModel;
import org.lenskit.bias.UserBiasModel;
import org.lenskit.data.ratings.RatingSummary;
import org.lenskit.results.Results;
import org.lenskit.util.collections.LongUtils;

import javax.annotation.Nonnull;
import javax.inject.Inject;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * Item scorer that does a logistic blend of a subsidiary item scorer and popularity.  It tries to predict
 * whether a user has rated a particular item.
 */
public class LogisticItemScorer extends AbstractItemScorer {
    private final LogisticModel logisticModel;
    private final BiasModel biasModel;
    private final RecommenderList recommenders;
    private final RatingSummary ratingSummary;

    @Inject
    public LogisticItemScorer(LogisticModel model, UserBiasModel bias, RecommenderList recs, RatingSummary rs) {
        logisticModel = model;
        biasModel = bias;
        recommenders = recs;
        ratingSummary = rs;
    }

    @Nonnull
    @Override
    public ResultMap scoreWithDetails(long user, @Nonnull Collection<Long> items) {
        List<Result> results = new ArrayList<>();

        // TODO Implement item scorer
        List<ItemScorer> scorers = this.recommenders.getItemScorers();
        double[] x = new double[scorers.size() + 2];

        // Logistic Regression formula: Pr[yui = 1] = sigmoid(a + b1x1 + ... + bnxn)
        for (long itemId : items) {
            double bias = this.biasModel.getIntercept() + this.biasModel.getUserBias(user) + this.biasModel.getItemBias(itemId);

            // x1 is the bias bui from the bias model
            x[0] = bias;

            // x2 is the log popularity of the item, log10|Ui| (get this from the rating summary)
            x[1] = Math.log10(ratingSummary.getItemRatingCount(itemId));

            for (int i = 0; i < scorers.size(); ++i) {
                ItemScorer scorer = scorers.get(i);
                Result score = scorer.score(user, itemId);
                x[i+2] = score == null ? 0.0 : score.getScore();
            }

            results.add(Results.create(itemId, logisticModel.evaluate(1.0, x)));
        }

        return Results.newResultMap(results);
    }
}
