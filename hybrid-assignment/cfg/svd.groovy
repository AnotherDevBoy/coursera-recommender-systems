import org.grouplens.lenskit.iterative.IterationCount
import org.grouplens.lenskit.iterative.LearningRate
import org.lenskit.api.ItemScorer
import org.lenskit.baseline.BaselineScorer
import org.lenskit.basic.TopNItemRecommender
import org.lenskit.bias.BiasItemScorer
import org.lenskit.bias.BiasModel
import org.lenskit.bias.UserItemBiasModel
import org.lenskit.data.dao.DataAccessObject
import org.lenskit.data.ratings.RatingSummary
import org.lenskit.mf.funksvd.FeatureCount
import org.lenskit.mf.funksvd.FunkSVDItemScorer
import org.lenskit.mooc.hybrid.LogisticItemScorer
import org.lenskit.mooc.hybrid.LogisticModel
import org.lenskit.mooc.hybrid.LogisticTrainingSplit

bind ItemScorer to FunkSVDItemScorer
set FeatureCount to 20
set IterationCount to 125
set LearningRate to 0.0015

bind (BaselineScorer, ItemScorer) to BiasItemScorer
bind BiasModel to UserItemBiasModel