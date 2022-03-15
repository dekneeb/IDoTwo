const toggle = document.getElementById('toggle')
const nav = document.getElementById('nav')

toggle.addEventListener('click', () => nav.classList.toggle('active'))

function showNotifications(){
    const container = document.getElementById('notification-container')

    if (container.classList.contains('d-none')){
        container.classList.remove('d-none')
    }else{
        container.classList.add('d-none')
    }
}

