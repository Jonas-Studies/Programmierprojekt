const { Database_collection } = require('../database.js')

exports.get_many_by_searchCriteria = async function (searchCriteria) {
    let result = undefined

    const substances_collection = new Database_collection('substances')
    
    await substances_collection.with_connection(
        async (collection) => {
            result = await collection.find(undefined).toArray()
        }
    )

    console.info('Loaded substances by searchcriteria')
    console.debug(result)

    return result
}