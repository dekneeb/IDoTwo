const toggle = document.getElementById('toggle')
const nav = document.getElementById('nav')
const search = document.getElementById('search-field')
const button = document.getElementById('onebutton')

toggle.addEventListener('click', () => nav.classList.toggle('active'))

button.addEventListener('click', ()=> search.classList.toggle('active'))
button.addEventListener('click', ()=> button.classList.toggle('active'))


function showNotifications(){
    const container = document.getElementById('notification-container')

    if (container.classList.contains('d-none')){
        container.classList.remove('d-none')
    }else{
        container.classList.add('d-none')
    }
}

