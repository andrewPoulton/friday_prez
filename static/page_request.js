
function switch_page(l){
    window.location.href = 'http://0.0.0.0:8080/' + l
}

var rotation = 90

function rotator(event){
    console.log(event)
    if (!!(event.key * 1)){
        var deg = (event.key * 90) % 360
        var george = document.getElementById('george')
        george.style.transform = "rotate(" + deg + "deg)"
    } else if (event.key == "Enter" || event.key == " ") {
        var r = Math.random()
        if (r<= 0.3 ){
            console.log(r)
            switch_page("george")
            return
        }
        switch_page(_next)
    } else if (event.key == "Backspace"){
        switch_page(_prev)
    }
}