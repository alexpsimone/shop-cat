'use strict';

// Toggle the label change field to active/inactive for changes based on
// checkbox selection. Checked box means the user wishes to delete the label,
// so make the label unavailable for edits.
$('#label-remove').on('change', () => {
    if ($('#label-remove').is(':checked')) {
        $('#label').prop('disabled', true);
    } else {
        $('#label').prop('disabled', false);
    };
});


function removeTool (evt) {

    evt.preventDefault();

    const toolButton = evt.target;
    const toolName = toolButton['value'];

    $(`#row-${toolName}`).remove();

    let NUM_TOOLS = Number($('#NUM_TOOLS').val());
    NUM_TOOLS -= 1;

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
}

$('button.remove-tool').on('click', removeTool);


function addTool (evt) {

    evt.preventDefault();
    
    let NUM_TOOLS = Number($('#NUM_TOOLS').val());
    NUM_TOOLS += 1;

    $.get('/get-tools.json', (res) => { 
        
        let str = '';
        for (const tool of res) {
            str = str + `<option value="${tool}">${tool}</option>`;
        }

        $('#tools').append(
            `<br />
            <label>New Tool: </label>
            <select name="tool_req_${NUM_TOOLS}" class="tool-req" id="tool${NUM_TOOLS}">
            <option value="">--Please select a tool--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify: </label>
            <input type="text" name="tool_other_${NUM_TOOLS}" />
            <br />`
        );

    });

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
    
}

$('#tool-add').on('click', addTool);


function addVehicle (evt) {

    evt.preventDefault();
   
    $('#car-add-form').show()

}


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
    })

    $('#model-select').attr('disabled', false);
    $('#vehicle-submit').attr('disabled', false);
}


function selectAddlVehicle (evt) {

    evt.preventDefault();

    let numCars = Number($('#NUM_CARS').val());
    numCars += 1;

    const formData = {
        make: $('#make').val(),
        modelYear: $('#model-year').val(),
        model: $('#model-select').val()
    };

    $.post('/vehicle-select.json', formData, (res) => {
        $('#all-cars').append(`<li id="item-${res['model_year']}-${res['make']}-${res['model']}">
                                ${res['model_year']}
                                ${res['make']}
                                ${res['model']}
                                <input type="checkbox"
                                    class="car-remove"
                                    id="remove-${res['model_year']}-${res['make']}-${res['model']}"
                                    name="remove-${res['model_year']}-${res['make']}-${res['model']}" />
                                <label for="remove-${res['model_year']}-${res['make']}-${res['model']}">
                                    Remove This Vehicle
                                </label>
                                </li>`)
    });

    $('#NUM_CARS').replaceWith(`<input name="NUM_CARS" 
                                id="NUM_CARS" type="number" 
                                value="${numCars}" 
                                style="display: none;"/>`)

    $('checkbox.car-remove').attr('disabled', false);
    $('#car-add-form').hide()
}



$('#car-add').on('click', addVehicle);
$('#make').on('change', getModels);
$('#vehicle-submit').on('click', selectAddlVehicle);