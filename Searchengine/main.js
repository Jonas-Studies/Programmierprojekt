console.info("Started the App")

const express = require("express")
const app = express()
const PORT = 3000

app.set('views', './views')
app.set('view engine', 'pug')

app.use(express.static('./public'))

app.use(
    '/search',
    async function (request, response, next) {
        console.info('Recieved request to display the search page')

        response.status(200).render('search_page')
    }
)

app.use(
    '/searchresults',
    async function (request, response, next) {
        console.info('Recieved request to display the search-results page')

        const substances_model = require('./models/substances')

        const searchCriteria = {
            keyphrase: request.query.keyphrase
        }

        const substances = await substances_model.get_many_by_searchCriteria(
                {
                    $text: { $search: searchCriteria.keyphrase }
                }
        )

        console.info(substances)

        response.status(200).render(
            'searchresults_page',
            { searchCriteria: searchCriteria, substances: substances }
        )
    }
)

app.use(
    '/',
    async function (request, response, next) {
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