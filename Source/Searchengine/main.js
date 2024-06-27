console.info("Started the App")

const express = require("express")
const app = express()
const PORT = 3000

app.set('views', './views')
app.set('view engine', 'pug')

app.use(express.static('./public'))

app.use(
    '/',
    function (request, response, next) {
        console.info('Recieved request to display the search page')

        response.status(200).render('search_page')
    }
)

app.listen(
    PORT,
    function () {
        console.log(`App listening on port ${PORT}!`)
    }
)