const { Database_collection } = require('../database.js')

exports.get_many_by_searchCriteria = async function (searchCriteria) {
    let result = undefined

    const substances_collection = new Database_collection('substances')
    
    await substances_collection.with_connection(
        async (collection) => {
            result = await collection.find(
                {
                    $or: [
                        { 'formula': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                        { 'iupac_names': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                        { 'cas_num': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                        { 'smiles': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                        { 'inchi': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                        { 'inchi_key': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                        { 'names': { $regex: searchCriteria.keyphrase, $options: 'i' } }
                    ]
                }
            ).skip(0).limit(10).toArray()
        }
    )

    console.info('Loaded substances by searchcriteria')
    console.debug(result)

    return result
}

exports.get_searchCriteria = function (new_keyphrase) {
    const result = {
        keyphrase: new_keyphrase
    }

    console.info('Created new searchcriteria')
    console.debug(result)

    return result
}