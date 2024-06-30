console.info("Started the App")

const express = require("express")
const app = express()
const PORT = 3000

app.set('views', './views')
app.set('view engine', 'pug')

app.use(express.static('./public'))

app.use(
    '/search',
    function (request, response, next) {
        console.info('Recieved request to display the search page')

        response.status(200).render('search_page')
    }
)

app.use(
    '/searchresults',
    function (request, response, next) {
        console.info('Recieved request to display the search-results page')

        const substances_model = require('./models/substances')

        const substances = substances_model.get_many_by_searchArguments(undefined)

        response.status(200).render(
            'searchresults_page',
            { substances: substances }
        )
    }
)

app.use(
    '/',
    function (request, response, next) {
        console.info('Recieved request to display the main page')

        response.redirect('/search')
    }
)

app.listen(
    PORT,
    function () {
        console.log(`App listening on port ${PORT}!`)
    }
)