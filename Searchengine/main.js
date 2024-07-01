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

        if (request.query.keyphrase != undefined) {
            const substances_model = require('./models/substances')
    
            const searchCriteria = substances_model.get_searchCriteria(request.query.keyphrase)
    
            const substances = await substances_model.get_many_by_searchCriteria(searchCriteria)
    
            console.info(substances)
    
            response.status(200).render(
                'searchresults_page',
                { searchCriteria: searchCriteria, substances: substances }
            )
        }
        else {
            response.status(200).render('search_page')
        }
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