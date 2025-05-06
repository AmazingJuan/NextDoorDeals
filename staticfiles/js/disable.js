function cambio(){
    const isChecked = document.getElementById("useRangeSES").checked
    console.log(isChecked)
    let single = document.getElementById("singleSESContainer")
    let range = document.getElementById("rangeSESContainer")
    if (isChecked){
        single.style.display = "none"
        range.style.display = "block"
    } else {
        single.style.display = "block"
        range.style.display = "none"
    }
}

document.getElementById("useRangeSES").addEventListener("change", cambio)