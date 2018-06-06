import org.grouplens.lenskit.vectors.similarity.CosineVectorSimilarity
import org.grouplens.lenskit.vectors.similarity.VectorSimilarity
import org.lenskit.api.ItemScorer
import org.lenskit.bias.BiasModel
import org.lenskit.bias.ItemBiasModel
import org.lenskit.bias.UserBiasModel
import org.lenskit.knn.NeighborhoodSize
import org.lenskit.knn.item.ItemItemScorer
import org.lenskit.transform.normalize.BiasUserVectorNormalizer
import org.lenskit.transform.normalize.UserVectorNormalizer

for (nnbrs in [5, 10, 15, 20, 25, 30, 40, 50, 75, 100]) {
    algorithm("ItemItem") {
        attributes["NNbrs"] = nnbrs
        include 'fallback.groovy'
        bind ItemScorer to ItemItemScorer
        bind VectorSimilarity to CosineVectorSimilarity
        set NeighborhoodSize to nnbrs
        bind UserVectorNormalizer to BiasUserVectorNormalizer
        within(UserVectorNormalizer) {
            bind BiasModel to UserBiasModel
        }
    }

    algorithm("ItemItemBiasItem") {
        attributes["NNbrs"] = nnbrs
        include 'fallback.groovy'
        bind ItemScorer to ItemItemScorer
        bind VectorSimilarity to CosineVectorSimilarity
        set NeighborhoodSize to nnbrs
        bind UserVectorNormalizer to BiasUserVectorNormalizer
        within(UserVectorNormalizer) {
            bind BiasModel to ItemBiasModel
        }
    }
}
