// General functions
var csrfcookie = function () {
    var cookieValue = null,
        name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function ajaxRequest() {
    try { var request = new XMLHttpRequest(); }
    catch (e1) {
        try { request = new ActiveXObject("Msxml2.XMLHTTP") }
        catch (e2) {
            try { request = new ActiveXObject("Microsoft.XMLHTTP") }
            catch (e3) {
                request = false;
            }
        }
    }
    return request;
}

function nullValidation(val) {
    if (val == "None" | val == null) {
        return "";
    } else {
        return val;
    };
}

function createErrorMessage(divId, message) {
    document.getElementById(divId).innerHTML = message;
    document.getElementById(divId).classList.add("alert");
    document.getElementById(divId).classList.add("alert-danger");
}

function deleteErrorMessage(divId) {
    document.getElementById(divId).innerHTML = "";
    document.getElementById(divId).classList.remove("alert");
    document.getElementById(divId).classList.remove("alert-danger");
}


function monthName(val) {
    var months = [ "January", "February", "March", "April", "May", "June", 
           "July", "August", "September", "October", "November", "December" ];
    return months[val];
  }


  function numberFormat(val, decimal_places, curr) {
    if (val < 0) {
        var negFlag = 1;
        val = Math.abs(val);
    }
    var newVal = val.toLocaleString(undefined, { maximumFractionDigits: decimal_places });
    if (curr == "yes") {
        newVal = "$" + newVal;
    }
    if (negFlag == 1) {
        newVal = "-" + newVal;
    }
    return newVal
}



function numberFormat2(val, decimal_places, curr) {
    num_scaler = Math.pow(10, decimal_places)
    val = Math.round(val*num_scaler)/num_scaler
    if (val < 0) {
        var negFlag = 1;
        val = Math.abs(val);
    }
    val = val.toLocaleString();
    if (curr == "yes") {
        val = "$" + val;
    }
    if (negFlag == 1) {
        val = "-" + val;
    }
    return val
}