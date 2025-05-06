
function next(userType){
    console.log(userType)
    let form = document.getElementById("registerForm")
    let userTypeSelector = document.getElementById("userType")
    
    selectValidator(userTypeSelector, userType)
    validateRole()

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

function validateRole(){
    element = document.getElementById("id_role")
    value = element.value
    selectValidator(element, value)
}

function toggleRequiredPersona(isRequired){
    document.getElementById('id_firstName').required = isRequired;
    document.getElementById('id_lastName').required = isRequired;
    document.getElementById('id_role').required = isRequired;
}

function toggleRequiredBussines(isRequired){
    document.getElementById('id_nit').required = isRequired;
    document.getElementById('id_name').required = isRequired;
}

function changeVisibility(tipo) {
    let formPersona = document.getElementById("personForm")
    let formBussines = document.getElementById("businessForm")
    if(tipo == "persona"){
        personaVisbility = "block"
        toggleRequiredPersona(true)
        bussinesVisibility = "none"
    }
    else if(tipo == "negocio"){
        console.log("estoy aka")
        personaVisbility = "none"
        toggleRequiredBussines(true)
        bussinesVisibility = "block"
    }
    else{
        personaVisbility = "none"
        bussinesVisibility = "none"
    }
    formBussines.style.display = bussinesVisibility
    formPersona.style.display = personaVisbility
}
