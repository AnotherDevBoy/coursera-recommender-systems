import org.lenskit.api.ItemScorer
import org.lenskit.bias.BiasModel
import org.lenskit.bias.ItemBiasModel
import org.lenskit.knn.NeighborhoodSize
import org.lenskit.knn.item.ItemItemScorer
import org.lenskit.knn.item.ModelSize
import org.lenskit.transform.normalize.BiasUserVectorNormalizer
import org.lenskit.transform.normalize.UserVectorNormalizer

for (neighbours in [5, 10, 15, 20, 25, 30, 40, 50, 75, 100]) {
    algorithm("ItemItem") {
        // use the user-user rating predictor
        bind ItemScorer to ItemItemScorer

        attributes["Neighbours"] = neighbours
        set NeighborhoodSize to neighbours

        // I don't think I need this
        // set ModelSize to 5000

        include 'fallback.groovy'

        bind UserVectorNormalizer to BiasUserVectorNormalizer
        within (UserVectorNormalizer) {
            bind BiasModel to ItemBiasModel
        }
    }
}

