package org.lenskit.mooc;

import org.lenskit.LenskitRecommender;
import org.lenskit.api.Recommender;
import org.lenskit.api.Result;
import org.lenskit.api.ResultList;
import org.lenskit.data.dao.DataAccessObject;
import org.lenskit.data.entities.Entity;
import org.lenskit.eval.traintest.AlgorithmInstance;
import org.lenskit.eval.traintest.DataSet;
import org.lenskit.eval.traintest.TestUser;
import org.lenskit.eval.traintest.metrics.MetricColumn;
import org.lenskit.eval.traintest.metrics.MetricResult;
import org.lenskit.eval.traintest.metrics.TypedMetricResult;
import org.lenskit.eval.traintest.recommend.TopNMetric;
import org.lenskit.mooc.cbf.TagData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;
import java.util.*;

/**
 * Top N metric that will measure the diversity of recommendations. There are many ways to measure diversity, but for this assignment we will use the entropy of the tags of the items in a top-10 recommendation list. 
 * Entropy is, roughly, a measurement of how complicated it is to say which one of several possibilities has been picked. 
 * If there are many different tags represented among the movies, they will have high entropy; if there are very few tags, entropy will below. 
 * We will use high entropy as an indication that the set of movies is diverse.1 
 */
public class TagEntropyMetric extends TopNMetric<TagEntropyMetric.Context> {
    private static final Logger logger = LoggerFactory.getLogger(TagEntropyMetric.class);

    /**
     * Construct a new tag entropy metric metric.
     */
    public TagEntropyMetric() {
        super(TagEntropyResult.class, TagEntropyResult.class);
    }

    @Nonnull
    @Override
    public MetricResult measureUser(TestUser user, int expectedSize, ResultList recommendations, Context context) {
        if (recommendations == null || recommendations.isEmpty()) {
            return MetricResult.empty();
            // no results for this user.
        }

        int recommendationListSize = recommendations.size();

        // get tag data from the context so we can use it
        DataAccessObject dao = context.getDAO();
        double entropy = 0.0;

        Map<String, Double> tagProbabilities = new HashMap<>();

        for (Result recommendation : recommendations) {
            long movie = recommendation.getId();

            List<Entity> itemTags = dao.query(TagData.ITEM_TAG_TYPE)
                .withAttribute(TagData.ITEM_ID, movie)
                .get();

            Map<String, Integer> tagOccurrences = new HashMap();

            int totalTagOccurrences = 0;

            for (Entity itag: itemTags) {
                String tagString = itag.get(TagData.TAG);

                int tagCount = tagOccurrences.containsKey(tagString) ? tagOccurrences.get(tagString) : 0;
                tagOccurrences.put(tagString, tagCount + 1);

                ++totalTagOccurrences;
            }

            for (String candidateTag : tagOccurrences.keySet()) {
                double candidateTagProbability = 1.0 * tagOccurrences.get(candidateTag) / totalTagOccurrences / recommendationListSize;

                double newCandidateTagProbability = tagProbabilities.containsKey(candidateTag) ?
                        tagProbabilities.get(candidateTag) + candidateTagProbability :
                        candidateTagProbability;

                tagProbabilities.put(candidateTag, newCandidateTagProbability);
            }
        }

        for (double probability: tagProbabilities.values()) {
            entropy += -1.0 * probability * logInBase(probability, 2);
        }

        context.addUser(entropy);
        return new TagEntropyResult(entropy);
    }

    private static double logInBase(double number, int base) {
        return Math.log(number) / Math.log(base);
    }

    @Nullable
    @Override
    public Context createContext(AlgorithmInstance algorithm, DataSet dataSet, Recommender recommender) {
        return new Context((LenskitRecommender) recommender);
    }

    @Nonnull
    @Override
    public MetricResult getAggregateMeasurements(Context context) {
        return new TagEntropyResult(context.getMeanEntropy());
    }

    public static class TagEntropyResult extends TypedMetricResult {
        @MetricColumn("TopN.TagEntropy")
        public final double entropy;

        public TagEntropyResult(double ent) {
            entropy = ent;
        }

    }

    public static class Context {
        private LenskitRecommender recommender;
        private double totalEntropy;
        private int userCount;

        /**
         * Create a new context for evaluating a particular recommender.
         *
         * @param rec The recommender being evaluated.
         */
        public Context(LenskitRecommender rec) {
            recommender = rec;
        }

        /**
         * Get the recommender being evaluated.
         *
         * @return The recommender being evaluated.
         */
        public LenskitRecommender getRecommender() {
            return recommender;
        }

        /**
         * Get the DAO for the current recommender evaluation.
         */
        public DataAccessObject getDAO() {
            return recommender.get(DataAccessObject.class);
        }

        /**
         * Add the entropy for a user to this context.
         *
         * @param entropy The entropy for one user.
         */
        public void addUser(double entropy) {
            totalEntropy += entropy;
            userCount += 1;
        }

        /**
         * Get the average entropy over all users.
         *
         * @return The average entropy over all users.
         */
        public double getMeanEntropy() {
            return totalEntropy / userCount;
        }
    }
}
