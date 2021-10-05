var alloGeoRecall = true;

function getLocation() {   
    console.log('getLocation was called') 
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, positionError);
    } else {
        hideLoadingDiv()
        console.log('Geolocation is not supported by this device')
    }
}

function positionError() {    
    console.log('Geolocation is not enabled. Please enable to use this feature')

    if(allowGeoRecall) getLocation()
}

function showPosition(){
    console.log('posiiton accepted')
    allowGeoRecall = false
}

