package org.lenskit.mooc.svd;

import it.unimi.dsi.fastutil.longs.LongSet;
import org.apache.commons.math3.linear.RealVector;
import org.lenskit.api.Result;
import org.lenskit.api.ResultMap;
import org.lenskit.basic.AbstractItemScorer;
import org.lenskit.bias.BiasModel;
import org.lenskit.data.dao.DataAccessObject;
import org.lenskit.results.Results;
import org.lenskit.util.collections.LongUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Nonnull;
import javax.inject.Inject;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * SVD-based item scorer.
 */
public class SVDItemScorer extends AbstractItemScorer {
    private static final Logger logger = LoggerFactory.getLogger(SVDItemScorer.class);
    private final SVDModel model;
    private final BiasModel baseline;
    private final DataAccessObject dao;

    /**
     * Construct an SVD item scorer using a model.
     * @param m The model to use when generating scores.
     * @param dao The data access object.
     * @param bias The baseline bias model (providing means).
     */
    @Inject
    public SVDItemScorer(SVDModel m, DataAccessObject dao,
                         BiasModel bias) {
        model = m;
        baseline = bias;
        this.dao = dao;
    }

    /**
     * Score items in a vector. The key domain of the provided vector is the
     * items to score, and the score method sets the values for each item to
     * its score (or unsets it, if no score can be provided). The previous
     * values are discarded.
     *
     * @param user   The user ID.
     * @param items The items to score
     */
    @Nonnull
    @Override
    public ResultMap scoreWithDetails(long user, @Nonnull Collection<Long> items) {
        RealVector userFeatures = model.getUserVector(user);
        if (userFeatures == null) {
            logger.debug("unknown user {}", user);
            return Results.newResultMap();
        }

        LongSet itemSet = LongUtils.asLongSet(items);

        RealVector featureWeights = model.getFeatureWeights();

        List<Result> results = new ArrayList<>();

        // TODO Compute the predictions
        // TODO Add the predicted offsets to the baseline score
        // TODO Store the results in 'results'
        for (long itemId : itemSet) {
            RealVector itemFeatures = model.getItemVector(itemId);

            double prediction = userFeatures
                    .ebeMultiply(featureWeights)
                    .dotProduct(itemFeatures);

            double score = this.baseline.getIntercept() + this.baseline.getUserBias(user) + this.baseline.getItemBias(itemId) + prediction;
            results.add(Results.create(itemId, score));
        }

        return Results.newResultMap(results);
    }
}
