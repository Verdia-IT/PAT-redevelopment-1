


$(document).ready(function () {
    // styleDatatable();
    // showAllPrograms();
    var $ProgramForm = $('#modal_form_new_program');
    $ProgramForm.submit(function (event) {
        event.preventDefault();
        saveNewProgram();
    });
    $(".btn-close-new-program").click(closeNewProgram);

});



function styleDatatable() {
    $('#myTable').DataTable({
        "dom": 'Blfrtip',

        "buttons": [
            {
                extend: 'copy',
                className: 'btn btn-info btn-sm copyButton border ',
                text: '<i class = "fa fa-clone"></i> Copy'
            },
            {
                extend: 'csv',
                className: 'btn btn-info btn-sm copyButton border ',
                text: '<i class = "fa fa-file-excel-o"></i> CSV'
            },
            {
                extend: 'excel',
                className: 'btn  btn-info btn-sm copyButton border ',
                text: '<i class = "fa fa-file-excel-o"></i> Excel',
                title: 'Program Table'
            },
            {
                extend: 'pdf',
                className: 'btn btn-info btn-sm copyButton border ',
                text: '<i class = "fa fa-file-pdf-o"></i> PDF'
            },
            {
                extend: 'print',
                className: 'btn btn-info btn-sm copyButton border ',
                text: '<i class = "fa fa-print"></i> PRINT'
            },
            {
                className: 'btn btn-info btn-sm copyButton border ',
                text: '<i class = "fa fa-print"></i> Custom button',
                action: function () {
                    alert('Hi')
                }
            },


        ],
        "ordering": true,
        "searching": true,
        "paging": true,
        "scrollY": 500,
        "columnDefs": [
            {
                // column target is not searchable
                "targets": 0,
                "searchable": true,
                "sortable": true,
                "visible": true,
            }
        ],
        // "order": [[1,"desc"]]
    });
    $(".copyButton").removeClass("dt-button")
    $(".copyButton").removeClass("buttons-html5")
    $(".copyButton").removeClass("buttons-copy")
    $(".copyButton").removeClass("buttons-csv")
    $(".copyButton").css("margin-right", "0px")
    $(".copyButton").css("margin-left", "0px")
    $(".dt-buttons").addClass("col-12")
    $(".dt-buttons").css("margin-bottom", "20px")
    // $("select").addClass( "selectpicker" )
    // $("select").formSelect();
    // $("#myTable_length").addClass( "row" )
    $(".dataTables_scrollHeadInner").css("width", "100%")
    $(".table").css("width", "100%")
}


function saveNewProgram(){
    var url = '/programs/save_new_program/'
    var $ProgramForm = $('#modal_form_new_program');   
    programId = "" 
    var $formData = $ProgramForm.serialize() + '&programId=' + programId;
    console.log($formData);
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    console.log(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == "Success") {                        
                        clearNewProgramModal();
                        $('#modal-new-program').modal("hide"); 
                        window.location.reload()                       
                    }
                    else {

                        if ("program_name" in data.message) {
                            createErrorMessage("error_new_program_modal_program_name", data.message.program_name)
                        }
                        else {
                            deleteErrorMessage("error_new_program_modal_program_name")
                        }
                        if ("salesforce_id" in data.message) {
                            createErrorMessage("error_new_program_modal_salesforce_id", data.message.salesforce_id)
                        }
                        else {
                            deleteErrorMessage("error_new_program_modal_salesforce_id")
                        }
                        if ("contact_name" in data.message) {
                            createErrorMessage("error_new_program_modal_contact_name", data.message.contact_name)
                        }
                        else {
                            deleteErrorMessage("error_new_program_modal_contact_name")
                        }
                        if ("contact_title" in data.message) {
                            createErrorMessage("error_new_program_modal_contact_title", data.message.contact_title)
                        }
                        else {
                            deleteErrorMessage("error_new_program_modal_contact_title")
                        }
                        if ("contact_email" in data.message) {
                            createErrorMessage("error_new_program_modal_contact_email", data.message.contact_email)
                        }
                        else {
                            deleteErrorMessage("error_new_program_modal_contact_email")
                        }
                        if ("contact_phone" in data.message) {
                            createErrorMessage("error_new_program_modal_contact_phone", data.message.contact_phone)
                        }
                        else {
                            deleteErrorMessage("error_new_program_modal_contact_phone")
                        }
                    }

                }
    }
    request.send($formData);
}

function clearNewProgramModal(){
    document.getElementById('modal_new_program_program_name').value = "";
    document.getElementById('modal_new_program_salesforce_id').value = "";
    document.getElementById('modal_new_program_contact_name').value = "";
    document.getElementById('modal_new_program_contact_title').value = "";
    document.getElementById('modal_new_program_contact_email').value = "";
    document.getElementById('modal_new_program_contact_phone').value = "";
    deleteErrorMessage("error_new_program_modal_program_name");
    deleteErrorMessage("error_new_program_modal_salesforce_id")
    deleteErrorMessage("error_new_program_modal_contact_name")
    deleteErrorMessage("error_new_program_modal_contact_title")
    deleteErrorMessage("error_new_program_modal_contact_email")
    deleteErrorMessage("error_new_program_modal_contact_phone")
}

function showAllPrograms(){
    var url = '/programs/show_programs/'
    var obj = new Object;
    obj.dummyVariable = "Dummy"

    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    console.log(this.responseText);
                    var data = JSON.parse(this.responseText);
                    if (data.message == 'Success') {
                        table_html = []
                        if (data.value.length > 0) {
                            for (i = 0; i < data.value.length; i++) {
                                table_html = table_html +
                                    (
                                        "<tr align='center'>" +
                                        "<td>" + (i + 1) + "</td>" +
                                        "<td>" + data.value[i].program_name + "</td>" +                                      
                                        "<td>" +
                                        "<form method='post' action='/programs/main_program/'>" + 
                                        "<input type='hidden' name='hidden_program_id' value='" + data.value[i].id + "'>" + 
                                        "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrfcookie() +"'>" +                                        
                                        "<button type='submit' class='btn text-secondary px-0'><i class='far fa-edit fa-lg'></i></button>" + 
                                        "</form>" +                
                                        "</td>" +
                                        "</tr>"
                                    )

                            }
                        }
                        document.getElementById("tbl_programs_body").innerHTML = table_html
                        deleteErrorMessage("div_programs_error")
                    }
                    else {
                        createErrorMessage("div_programs_error", data.message)
                    }



                }
    }
    request.send(params);

}


function closeNewProgram() {
    clearNewProgramModal();
    $('#modal-new-program').modal("hide");
}

