package org.lenskit.mooc.cbf;

import it.unimi.dsi.fastutil.longs.LongSet;
import org.lenskit.data.dao.DataAccessObject;
import org.lenskit.data.entities.CommonTypes;
import org.lenskit.data.entities.Entity;
import org.lenskit.inject.Transient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.inject.Inject;
import javax.inject.Provider;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Builder for computing {@linkplain TFIDFModel TF-IDF models} from item tag data.  Each item is
 * represented by a normalized TF-IDF vector.
 *
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class TFIDFModelProvider implements Provider<TFIDFModel> {
    private static final Logger logger = LoggerFactory.getLogger(TFIDFModelProvider.class);

    private final DataAccessObject dao;

    /**
     * Construct a model builder.  The {@link Inject} annotation on this constructor tells LensKit
     * that it can be used to build the model builder.
     *
     * @param dao The data access object.
     */
    @Inject
    public TFIDFModelProvider(@Transient DataAccessObject dao) {
        this.dao = dao;
    }

    /**
     * This method is where the model should actually be computed.
     * @return The TF-IDF model (a model of item tag vectors).
     */
    @Override
    public TFIDFModel get() {
        logger.info("Building TF-IDF model");

        // Create a map to accumulate document frequencies for the IDF computation
        Map<String, Double> documentFrequency = new HashMap<>();

        // We now proceed in 2 stages. First, we build a TF vector for each item.
        // While we do this, we also build the DF vector.
        // We will then apply the IDF to each TF vector and normalize it to a unit vector.

        // Create a map to store the item TF vectors.
        Map<Long, Map<String, Double>> itemVectors = new HashMap<>();

        // Iterate over the items to compute each item's vector.
        LongSet items = dao.getEntityIds(CommonTypes.ITEM);
        for (long item : items) {
            // Create a work vector to accumulate this item's tag vector.
            Map<String, Double> itemTermFrequencyVector = new HashMap<>();

            // Increment the document frequency vector once for each unique tag on the item.
            Set<String> seenTags = new HashSet<String>();
            for (Entity tagApplication : dao.query(TagData.ITEM_TAG_TYPE)
                                            .withAttribute(TagData.ITEM_ID, item)
                                            .get()) {
                String tag = tagApplication.get(TagData.TAG);

                double newTermFrequencyValue = itemTermFrequencyVector.containsKey(tag) ?
                        itemTermFrequencyVector.get(tag) + 1.0 :
                        1.0;

                itemTermFrequencyVector.put(tag, newTermFrequencyValue);

                if (!seenTags.contains(tag)) {
                    seenTags.add(tag);

                    double newFrequency = documentFrequency.containsKey(tag) ?
                            documentFrequency.get(tag) + 1.0 :
                            1.0;

                    documentFrequency.put(tag, newFrequency);
                }
            }

            itemVectors.put(item, itemTermFrequencyVector);
        }

        logger.info("Computed TF vectors for {} items", itemVectors.size());

        // Now we've seen all the items, so we have each item's TF vector and a global vector
        // of document frequencies.
        // Invert and log the document frequency.  We can do this in-place.
        final double logN = Math.log(items.size());
        for (Map.Entry<String, Double> e : documentFrequency.entrySet()) {
            e.setValue(logN - Math.log(e.getValue()));
        }

        // Now documentFrequency is a log-IDF vector.  Its values can therefore be multiplied by TF values.
        // So we can use it to apply IDF to each item vector to put it in the final model.
        // Create a map to store the final model data.
        Map<Long, Map<String, Double>> modelData = new HashMap<>();
        for (Map.Entry<Long, Map<String, Double>> entry : itemVectors.entrySet()) {
            Map<String, Double> itemTermFrequencyVector = new HashMap<>(entry.getValue());

            double sumOfSquares = 0.0;

            for (String term : itemTermFrequencyVector.keySet()) {
                double documentFrequencyForTerm = documentFrequency.get(term);
                double termFrequencyForTerm = itemTermFrequencyVector.get(term);

                double tfidf = termFrequencyForTerm * documentFrequencyForTerm;
                itemTermFrequencyVector.put(term, tfidf);
                sumOfSquares += Math.pow(tfidf, 2);
            }

            // Normalize it by dividing each element by its Euclidean norm, which is the
            // square root of the sum of the squares of the values.
            sumOfSquares = Math.sqrt(sumOfSquares);

            for (String term : itemTermFrequencyVector.keySet()) {
                double normalizedTfidfValue = itemTermFrequencyVector.get(term) / sumOfSquares;
                itemTermFrequencyVector.put(term, normalizedTfidfValue);
            }

            modelData.put(entry.getKey(), itemTermFrequencyVector);
        }

        // We don't need the IDF vector anymore, as long as as we have no new tags
        return new TFIDFModel(modelData);
    }
}
