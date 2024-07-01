const { Database_collection } = require('./database')

console.info('Included the database module')
console.debug(Database_collection)

main()

async function main () {
    console.info('Started the install')

    await drop_indexes()

    await create_text_index()

    console.info('Ended the install')
}

async function create_text_index () {
    const substances_collection = new Database_collection('substances')

    try {
        await substances_collection.with_connection(
            async (collection) => {
                await collection.createIndex(
                    {
                       "$**": "text"
                    }
                )
            }
        )

        console.info('Created a text-search index')
    }
    catch (error) {
        console.error('Failed to create a text-search index')
        console.debug(error)
    }

    return
}

async function drop_indexes () {
    const substances_collection = new Database_collection('substances')

    const indexes = await get_indexes()

    try {
        // Zu jedem index werden zwei Objekte zurückgegeben. Jeweils nur das jeweil zweite wird benötigt
        for (let index_nr = 1; index_nr < indexes.length; index_nr += 2) {
            console.info('Selected index nr ' + index_nr)
            console.debug(indexes[index_nr])

            await drop_index(indexes[index_nr].name)
        }

        console.info('Dropped indexes')
    }
    catch (error) {
        console.error('Failed to drop indexes')
        console.debug(error)
    }
}

async function drop_index (index_name) {
    const substances_collection = new Database_collection('substances')

    try {
        await substances_collection.with_connection(
            async (collection) => {
                await collection.dropIndex(index_name)
            }
        )

        console.info('Dropped index')
    }
    catch (error) {
        console.error('Failed to drop index ' + index_name)
        console.debug(error)
    }
}

async function get_indexes () {
    let result = undefined

    const substances_collection = new Database_collection('substances')

    try {
        await substances_collection.with_connection(
            async (collection) => {
                result = await collection.indexes()
            }
        )

        console.info('loaded indexes')
        console.debug(result)
    }
    catch (error) {
        console.error('Failed to load indexes')
        console.debug(error)
    }

    return result
}