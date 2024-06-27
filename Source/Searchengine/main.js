console.info("Started the App")

const express = require("express")
const app = express()
const PORT = 3000

app.use(
    '/',
    function (request, response, next) {
        console.info('Recieved request to display the search page')

        response.status(200).send('Moin')
    }
)

app.listen(
    PORT,
    function () {
        console.log(`App listening on port ${PORT}!`)
    }
)