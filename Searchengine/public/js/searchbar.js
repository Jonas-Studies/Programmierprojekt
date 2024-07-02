function toggle_options () {
    const element = document.querySelector('.searchbar-options')

    console.info('Loaded the searchbar options element')
    console.debug(element)

    if (element.style.display === 'block') {
        element.style.display = 'none'
    }
    else {
        element.style.display = 'block'
    }

    return
}