const { MongoClient } = require('mongodb')

exports.Database_collection = class {
    constructor(collectionName) {
        this.URI = 'mongodb://localhost:27017'
        this.databaseName = 'designerdrugdatabase'
        this.client = new MongoClient(this.URI)
        this.collection = this.client.db(this.databaseName).collection(collectionName)
    }

    async open_connection () {
        let result = false

        try {
            await this.client.connect()
            console.info('Opened connection to the database')

            result = true
        }
        catch (error) {
            console.error('Failed to open an database connection')
            console.debug(error)
        }

        return result
    }

    async close_connection () {
        try {
            await this.client.close()
            console.info('Closed connection to the database')
        }
        catch (error) {
            console.error('Failed to close the database connection')
            console.debug(error)
        }
    }

    async with_connection (callback) {
        if (await this.open_connection() === true) {

            try {
                await callback(this.collection)
            }
            catch (error) {
                console.error('Failed to execute database operation')
                console.debug(error)
            }
    
            await this.close_connection()
        }
        else {
            console.error('Failed to execute database operation')
        }
    }
}