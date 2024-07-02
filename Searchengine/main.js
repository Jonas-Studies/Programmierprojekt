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

        let keyphrase = undefined

        if (request.query.keyphrase != undefined && request.query.keyphrase != '') {
            keyphrase = request.query.keyphrase
        }

        let min_molecular_mass = undefined

        if (request.query.min_molecular_mass != undefined && request.query.min_molecular_mass != '') {
            min_molecular_mass = Number(request.query.min_molecular_mass)
        }

        let max_molecular_mass = undefined

        if (request.query.max_molecular_mass != undefined && request.query.max_molecular_mass != '') {
            max_molecular_mass = Number(request.query.max_molecular_mass)
        }

        if (keyphrase != undefined || min_molecular_mass != undefined || max_molecular_mass != undefined) {
            const substances_model = require('./models/substances')
    
            const searchCriteria = substances_model.get_searchCriteria(keyphrase, min_molecular_mass, max_molecular_mass)
    
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