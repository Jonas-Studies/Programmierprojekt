const { Database_collection } = require('../database.js')

exports.get_many_by_searchCriteria = async function (searchCriteria) {
    let result = undefined

    let query = {
        $and: []
    }

    if (searchCriteria.keyphrase != undefined && searchCriteria.keyphrase != "") {
        query.$and.push(
            {
                $or: [
                    { 'names': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                    { 'iupac_names': { $regex: searchCriteria.keyphrase, $options: 'i' } },
                    { 'smiles': { $regex: searchCriteria.keyphrase, $options: 'i' } }
                ]
            }
        )
    }

    if (searchCriteria.molecular_mass.min != undefined && searchCriteria.molecular_mass.min > 0) {
        if (searchCriteria.molecular_mass.max != undefined && searchCriteria.molecular_mass.max > 0) {
            query.$and.push(
                { 'molecular_mass': { $gt: searchCriteria.molecular_mass.min, $lt: searchCriteria.molecular_mass.max } }
            )

            console.info('Added statement to restrict on min and max molecular mass to query')
        }
        else {
            query.$and.push(
                { 'molecular_mass': { $gt: searchCriteria.molecular_mass.min } }
            )

            console.info('Added statements to restrict on min molecular mass to query')
        }
    }
    else {   
        if (searchCriteria.molecular_mass.max != undefined && searchCriteria.molecular_mass.max > 0)
        query.$and.push(
            { 'molecular_mass': { $lt: searchCriteria.molecular_mass.max } }
        )

        console.info('Added statements to restrict on max molecular mass to query')
    }

    console.info('Finished the construction of the query statement')
    console.debug(query)

    const substances_collection = new Database_collection('substances')
    
    await substances_collection.with_connection(
        async (collection) => {
            result = await collection.find(query).skip(0).limit(10).toArray()
        }
    )

    console.info('Loaded substances by searchcriteria')
    console.debug(result)

    return result
}

exports.get_searchCriteria = function (new_keyphrase, new_molecularMass_minvalue, new_molecularMass_maxvalue) {
    const result = {
        keyphrase: new_keyphrase,
        molecular_mass: {
            min: Number(new_molecularMass_minvalue),
            max: Number(new_molecularMass_maxvalue)
        }
    }

    console.info('Created new searchcriteria')
    console.debug(result)

    return result
}