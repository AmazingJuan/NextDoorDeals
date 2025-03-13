
function next(userType){
    console.log(userType)
    let form = document.getElementById("registerForm")
    let userTypeSelector = document.getElementById("userType")
    
    selectValidator(userTypeSelector, userType)

    let validity = form.checkValidity()
    if(validity){
        document.getElementById("regularForm").style.display = "none"
        document.getElementById("boton-next").style.display = "none"
        document.getElementById("boton-register").style.display = "block"
        changeVisibility(userType)
    }
    else{
        form.reportValidity()
    }
}

function selectValidator(element, value){
    if(value == "1"){
        element.setCustomValidity("The fuck is you doin' dawg. U selected a wrong option. Think a lil bit and do it again, pls.")
    }
    else{
        element.setCustomValidity("")
    }
}

function validateRole(userType){
    if(userType == "persona"){
        element = document.getElementById("id_role")    
    }
    else{
        element = document.getElementById("id_role")
    }
    value = element.value
    selectValidator(element, value)
}

function toggleRequiredPersona(isRequired){
    console.log(isRequired)
    if(isRequired){
        console.log("estoy aki")
        document.getElementById('id_firstName').required = true;
        document.getElementById('id_lastName').required = true;
        document.getElementById('id_role').required = true;
    }
    else{
        document.getElementById('id_firstName').required = false;
        document.getElementById('id_lastName').required = false;
        document.getElementById('id_role').required = false;
    }
}

function toggleRequiredBussines(isRequired){
    if(isRequired){
        document.getElementById('id_firstName').required = true;
        document.getElementById('id_lastName').required = true;
        document.getElementById('id_role').required = true;
    }
    else{
        document.getElementById('id_firstName').required = false;
        document.getElementById('id_lastName').required = false;
        document.getElementById('id_role').required = false;
    }
}

function changeVisibility(tipo) {
    console.log(tipo)
    let formPersona = document.getElementById("personForm")
    let formBussines = document.getElementById("businessForm")
    if(tipo == "persona"){
        personaVisbility = "block"
        toggleRequiredPersona(true)
        bussinesVisibility = "none"
    }
    else if(tipo == "business"){
        personaVisbility = "none"
        toggleRequiredPersona(false)
        bussinesVisibility = "block"
    }
    else{
        personaVisbility = "none"
        bussinesVisibility = "none"
    }
    formBussines.style.display = bussinesVisibility
    formPersona.style.display = personaVisbility
}
