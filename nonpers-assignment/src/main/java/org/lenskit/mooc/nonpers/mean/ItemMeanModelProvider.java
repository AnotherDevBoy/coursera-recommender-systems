package org.lenskit.mooc.nonpers.mean;

import it.unimi.dsi.fastutil.longs.Long2DoubleOpenHashMap;
import it.unimi.dsi.fastutil.longs.Long2IntOpenHashMap;
import org.lenskit.data.dao.DataAccessObject;
import org.lenskit.data.ratings.Rating;
import org.lenskit.inject.Transient;
import org.lenskit.util.io.ObjectStream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.inject.Inject;
import javax.inject.Provider;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * Provider class that builds the mean rating item scorer, computing item means from the
 * ratings in the DAO.
 */
public class ItemMeanModelProvider implements Provider<ItemMeanModel> {
    /**
     * A logger that you can use to emit debug messages.
     */
    private static final Logger logger = LoggerFactory.getLogger(ItemMeanModelProvider.class);

    /**
     * The data access object, to be used when computing the mean ratings.
     */
    private final DataAccessObject dao;

    /**
     * Constructor for the mean item score provider.
     *
     * <p>The {@code @Inject} annotation tells LensKit to use this constructor.
     *
     * @param dao The data access object (DAO), where the builder will get ratings.  The {@code @Transient}
     *            annotation on this parameter means that the DAO will be used to build the model, but the
     *            model will <strong>not</strong> retain a reference to the DAO.  This is standard procedure
     *            for LensKit models.
     */
    @Inject
    public ItemMeanModelProvider(@Transient DataAccessObject dao) {
        this.dao = dao;
    }

    /**
     * Construct an item mean model.
     *
     * <p>The {@link Provider#get()} method constructs whatever object the provider class is intended to build.</p>
     *
     * @return The item mean model with mean ratings for all items.
     */
    @Override
    public ItemMeanModel get() {
        Map<Long, List<Double>> ratingsPerItem = new HashMap<Long, List<Double>>();

        try (ObjectStream<Rating> ratings = this.dao.query(Rating.class).stream()) {
            for (Rating r: ratings) {
                if (!ratingsPerItem.containsKey(r.getItemId())) {
                    ratingsPerItem.put(r.getItemId(), new LinkedList<Double>());
                }

                List<Double> ratingsForItem = ratingsPerItem.get(r.getItemId());
                ratingsForItem.add(r.getValue());
            }
        }

        Long2DoubleOpenHashMap means = new Long2DoubleOpenHashMap();

        for (long itemId : ratingsPerItem.keySet()) {
            List<Double> ratingsForItem = ratingsPerItem.get(itemId);

            double sum = 0;
            for (double rating: ratingsForItem) {
                sum += rating;
            }

            double mean = sum / ratingsForItem.size();
            means.put(itemId, mean);
        }

        logger.info("computed mean ratings for {} items", means.size());
        return new ItemMeanModel(means);
    }
}
