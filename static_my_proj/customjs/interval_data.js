
Object.size = function (obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};


function createChart(data) {    
    startDate = data[0].Datetime;
    arr = breakExcelDate(startDate)
    startDay = arr[2];
    startMonth = arr[1];
    startYear = arr[0];
    startHour = arr[3];
    startMinutes = arr[4];
    intervalMinutes = 30;
    var dataMain = [];    
    var dataLength = Object.size(data); 
    for (i = 0; i < dataLength - 1; i = i + 1) {
        // dataMain.push([data.data[i].Datetime, data.data[i].kW, data.data[i].kVA]);
        dataMain.push([new Date(startYear, startMonth, startDay, startHour, startMinutes + i * intervalMinutes, 0), data[i].kW, data[i].kVA]);
    }
    console.log(dataMain)
    // window.setTimeout(donothing, 2000);

    new Dygraph(
        document.getElementById("noroll"),
        // [
        //     [1, 10, 100],
        //     [2, 20, 80],
        //     [3, 50, 60],
        //     [4, 70, 80]
        // ],
        dataMain,
        {
            labels: ["Datetime ", 'kVA', 'kW'],
            // customBars: true,
            title: 'Interval Data',
            ylabel: 'kW / kVA',
            legend: 'always',
            xlabel: 'Date',
            showRangeSelector: true,
            valueFormatString: "DD-MMM-YYYY HH:mm",
            labelAngle: -50,
            // axes: {
            //     x: {
            //         valueFormatter: function (x) {
            //             return 'text';
            //         },
            //         axisLabelFormatter: function (x) {
            //             return R2(x.getFullYear()) + '-' + R2(x.getMonth() + 1) + '-' +
            //                 R2(x.getDate()) + ' ' + R2(x.getHours()) + ':' + R2(x.getMinutes());
            //         },
            //     }
            // },
        }
    );
}

function handleFileSelect() {
    // evt.preventDefault();
    // var file = evt.target.files[0];
    var file = document.getElementById("interval_data_form_interval_data_file").files[0];
    console.log(file);
    Papa.parse(file, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            // createChart(results.data);
            data = results.data;
            createChart(data);            
            // var Datetime = [];
            // var kW = [];
            // var kVA = [];
            // for (i = 0; i < data.length - 1; i = i + 1) {
            //     Datetime[i] = data[i].Datetime;
            //     kW[i] = data[i].kW;
            //     kVA[i] = data[i].kVA;
            // }
            
        }
    });
}

// --------------------------

$('#interval_data_form_interval_data_file').on('change', function () {
    handleFileSelect();
});


// var $UploadForm = $('#form_upload');
// $UploadForm.submit(function (event) {
//     event.preventDefault();
//     uploadFunction();
// });

var $IntervalDataUploadForm = $('#form_interval_data_upload');
$IntervalDataUploadForm.submit(function (event) {
    event.preventDefault();
    intervalDataUploadFunction();
});

showIntervalDataList();

// function uploadFunction(){
//     var url = '/scenarios/upload/'
//     // var $UploadForm = $('#form_upload');    
//     var formData = new FormData();
//     var fileSelect = document.getElementById("document1")
//     var files = fileSelect.files;
//     var file = files[0];
//     formData.append('csv', file, file.name);
//     request = new ajaxRequest()
//     request.open("POST", url, true)
//     // request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//     request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
//     request.setRequestHeader('X-CSRFToken', csrfcookie());
//     request.onreadystatechange = function () {
//         if (this.readyState == 4)
//             if (this.status == 200)
//                 if (this.responseText != null) {                    
//                     var data = JSON.parse(this.responseText);
//                     // console.log(data)
//                     console.log(data.url)
//                     document.getElementById('upload_url').text = data.url;
//                     document.getElementById('upload_url').href = data.url;
//                 }
//     }
//     request.send(formData);
// }


function intervalDataUploadFunction() {
    var url = '/scenarios/interval_data_upload/'
    var formData = new FormData(document.getElementById("form_interval_data_upload"));
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    // var fileSelect = document.getElementById("interval_data_form_interval_data_file")
    // var files = fileSelect.files;
    // var file = files[0];
    // formData.append('csv', file, file.name);
    var obj = new Object();
    obj.scenarioId = scenarioId
    var JSONobj = JSON.stringify(obj);
    formData.append('JSONobj', JSONobj);
    request = new ajaxRequest()
    request.open("POST", url, true)
    // request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    console.log(data.message)
                    showIntervalDataList();
                    // Fill Interval Data choices
                    selected_interval_data_id = document.getElementById("simulation_parameter_interval_data").value
                    $("#simulation_parameter_interval_data").empty();
                    var sel = document.getElementById('simulation_parameter_interval_data');
                    // create new option element
                    console.log(data)
                    for (i=0;i<data.idList.length;i++){
                        var opt = document.createElement('option');
                        opt.appendChild( document.createTextNode(data.fileNameList[i]) );
                        opt.value = data.idList[i];
                        sel.appendChild(opt); 
                        if (opt.value == selected_interval_data_id){
                            opt.setAttribute("selected", "selected");
                        }
                    }

                }
    }
    request.send(formData);
}


function showIntervalDataList() {
    var url = '/scenarios/file_list/'
    // var $UploadForm = $('#form_upload');     
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var obj = new Object();
    obj.scenarioId = scenarioId
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    table_html = [];
                    if (data.urlList.length > 0) {
                        for (i = 0; i < data.urlList.length; i++) {
                            table_html = table_html +
                                (
                                    "<tr>" +
                                    "<td><a class='btn text-secondary px-0' onclick='graphIntervalData(" + data.idList[i] + ")';>" + data.fileNameList[i] + "</a></td>" +
                                    "<td>" +
                                    "<a class='btn text-secondary px-0' href='" + data.urlList[i] + "'><i class='fa fa-download fa-sm'></i></a>" +
                                    "<button class='btn d-inline' onclick='deleteIntervalData(" + data.idList[i] + ")';>" +
                                    "<i class='far fa-trash-alt fa-sm text-danger float-right'></i>" +
                                    "</button>" +
                                    "</td>" +
                                    "</tr>"
                                )
                        }
                    }
                    document.getElementById("tbl_file_list_body").innerHTML = table_html
                }
    }
    request.send(params);
}

function deleteIntervalData(intervalDataId) {
    var url = '/scenarios/delete_interval_data/'
    var scenarioId = document.getElementById("hidden_scenario_id").value;
    var obj = new Object();
    obj.scenarioId = scenarioId    
    obj.intervalDataId = intervalDataId;

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
                    var data = JSON.parse(this.responseText);
                    console.log(data)
                    if (data.message == "Success") {
                        showIntervalDataList();
                        deleteErrorMessage("error_interval_data");

                        // Fill Interval Data choices
                        selected_interval_data_id = document.getElementById("simulation_parameter_interval_data").value
                        $("#simulation_parameter_interval_data").empty();
                        var sel = document.getElementById('simulation_parameter_interval_data');
                        // create new option element
                        console.log(data)
                        for (i=0;i<data.idList.length;i++){
                            var opt = document.createElement('option');
                            opt.appendChild( document.createTextNode(data.fileNameList[i]) );
                            opt.value = data.idList[i];
                            sel.appendChild(opt); 
                            if (opt.value == selected_interval_data_id){
                                opt.setAttribute("selected", "selected");
                            }
                        }
                    }
                    else {
                        createErrorMessage("error_interval_data", data.message);
                    }

                }
    }
    request.send(params);
}

function graphIntervalData(intervalDataId) {

    var url = '/scenarios/graph_interval_data/'
    var obj = new Object();
    obj.intervalDataId = intervalDataId
    var JSONobj = JSON.stringify(obj);
    params = "JSONobj=" + JSONobj;
    request = new ajaxRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.setRequestHeader('X-CSRFToken', csrfcookie());
    request.onreadystatechange = function () {
        if (this.readyState == 4)
            if (this.status == 200)
                if (this.responseText != null) {
                    var data = JSON.parse(this.responseText);     
                    data = JSON.parse(data.data);                
                    createChart(data);
                }
    }
    request.send(params);

}


