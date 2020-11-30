'use strict';



function getModels (evt) {
    
    evt.preventDefault();

    const formData = {
        make: $('#make').val(),
        modelYear: $('#model-year').val()
    };

    console.log(formData.make);
    console.log(formData.modelYear);

    $.get('/get-models.json', formData, (res) => {

        let str = '';
        for (const model of res) {
            str = str + `<option value="${model}">${model}</option>`;
        }
        $('#model-select').replaceWith(
            `<select id="model-select" name="model">
            <option value="">--Please select a Model--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>`
        );
    });

    $('#model-select').attr('disabled', false);
    $('#vehicle-submit').attr('disabled', false);
}


function getModelYears (evt) {

    evt.preventDefault();

    const formData = {
        make: $('#make').val(),
    };

    $.get('/get-model-years.json', formData, (res) => {

        let str = '';
        for (const model_year of res) {
            str = str + `<option value="${model_year}">${model_year}</option>`;
        }
        $('#model-year').replaceWith(
            `<select id="model-year" name="model-year">
            <option value="">--Please select a Model Year--</option>
            ${str}
            </select>`
        );

        $('#model-year').on('change', getModels);
    });

    
}


function submitVehicle (evt) {

    evt.preventDefault();

    const formData = {
        make: $('#make').val(),
        modelYear: $('#model-year').val(),
        model: $('#model-select').val()
    };
    console.log(formData);

    $.post('/vehicle-select.json', formData, (res) => {
        $('#selected-vehicle').replaceWith(`<p id="selected-vehicle">
                                            You selected a 
                                            ${res['model_year']}
                                            ${res['make']}
                                            ${res['model']}.
                                            </p>`)
    });

    $('#proc-title').attr('disabled', false);
    $('#proc-label').attr('disabled', false);
    $('#proc-img').attr('disabled', false);
    $('#proc-text').attr('disabled', false);
    $('#proc-submit').attr('disabled', false);
    $('#tool-adder').attr('disabled', false);
    $('#part-adder').attr('disabled', false);
    $('#step-adder').attr('disabled', false);
}

$('#make').on('change', getModelYears);
$('#vehicle-submit').on('click', submitVehicle);

