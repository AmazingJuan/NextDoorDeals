function toggleButtons(){
    if(document.getElementById("btn-next").style.display == "none"){
        document.getElementById("btn-next").style.display = "block"
    }
    if(document.getElementById("btn-previous").style.display == "none"){
        document.getElementById("btn-previous").style.display = "block"
    }
    if (current_id == 0){
        document.getElementById("btn-previous").style.display = "none"
    }
    else if(current_id == images.length - 1){
        document.getElementById("btn-next").style.display = "none"
        console.log("aca")
    }
    
}

function previousImage(){
    if (current_id > 0){
        current_id--
        document.getElementById("property-image").src = images[current_id]
        document.getElementById("current-image").innerText = current_id+1 
        toggleButtons()
    }
}

function nextImage(){
    if (current_id + 1  < images.length){
        current_id++
        document.getElementById("property-image").src = images[current_id]
        document.getElementById("current-image").innerText = current_id+1 
        toggleButtons()
    } 


}
