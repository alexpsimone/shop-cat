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
            `<tr>
                <td class="meta">
                <input type="hidden" class="tool-order" name="order" value="${NUM_TOOLS}" />
                <input type="hidden" class="tool-id" name="tool-id-${NUM_TOOLS}" value="NEW" />
                <label>New Tool: </label>
                <select class="tool-name" name="tool-name-${NUM_TOOLS}" value="tool-${NUM_TOOLS}">
                <option value="">--Please select a tool--</option>
                ${str}
                <option value="other">Other (please specify)...</option>
                </select>
                <br /><label>If other, please specify: </label>
                <input type="text" class="tool-other-name" name="tool-other-name-${NUM_TOOLS}" />
                </td>
                <td class="img">
                <input type="hidden" class="tool-existing-img" name="tool-existing-img-${NUM_TOOLS}" value="toolbox.png" />
                <label>If other, add image (optional): </label>
                <input type="file" class="tool-img" name="tool-img-${NUM_TOOLS}" />
                </td>
                <td>
                <button class="remove-tool">Remove</button>
                </td>
            </tr>`
        );

        $('button.remove-tool').off();
        $('button.edit').off();
        $('button.del-img').off();
        $('button.remove-tool').on('click', removeTool);
        $('button.edit').on('click', enableEditField);
        $('button.del-img').on('click', restoreDefaultImg);

    });

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
    
}


function removeTool (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr');

    const nextLength = ($(thisRow).nextAll('tr')).length;

    for (let row = 0; row < nextLength; row += 1) {
        
        const nextRow = $(thisRow).nextAll('tr')[row];
        const nameOrderColumn = $(nextRow).children('td.name-order');
        console.log(`nameOrderColumn: ${nameOrderColumn}`);
        const orderInput = $(nameOrderColumn).children('input.tool-order');
        console.log(`orderInput: ${orderInput}`);
        const newOrder = Number($(orderInput).val()) - 1;
        console.log(`newOrder: ${newOrder}`);
        
        
        $(orderInput).attr('value', newOrder);

        const toolInputID = $(nameOrderColumn).children('input.tool-id');
        $(toolInputID).attr('name', `tool-id-${newOrder}`);
        const toolInputName = $(nameOrderColumn).children('input.tool-name');
        $(toolInputName).attr('name', `tool-name-${newOrder}`);
        const toolInputOtherName = $(nameOrderColumn).children('input.tool-other-name');
        $(toolInputOtherName).attr('name', `tool-other-name-${newOrder}`);

        const imgColumn = $(nextRow).children('td.img');
        const toolInputExistingImg = $(imgColumn).children('input.tool-existing-img');
        $(toolInputExistingImg).attr('name', `tool-existing-img-${newOrder}`)
        const toolInputImg = $(imgColumn).children('input.tool-img');
        $(toolInputImg).attr('name', `tool-img-${newOrder}`);


    };

    $(thisRow).remove();

    let NUM_TOOLS = Number($('#NUM_TOOLS').val());
    NUM_TOOLS -= 1;

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
                                    type="hidden" value="${NUM_TOOLS}" />`);
}


function removePart (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr');
    $(thisRow).remove();

    let NUM_PARTS = Number($('#NUM_PARTS').val());
    NUM_PARTS -= 1;

    $('#NUM_PARTS').replaceWith(`<input name="NUM_PARTS" id="NUM_PARTS" 
                                    type="hidden" value="${NUM_PARTS}" />`);
}


function addPart (evt) {

    evt.preventDefault();
    
    let NUM_PARTS = Number($('#NUM_PARTS').val());
    NUM_PARTS += 1;

    $.get('/get-parts.json', (res) => { 
       
        let str = '';
        for (const part of res) {
            str = str + `<option value="${part}">${part}</option>`;
        }
        $('#parts').append(
            `<tr>
                <td>
                    <label>New Part: </label>
                    <select name="part_req_${NUM_PARTS}" class="part-req" id="part${NUM_PARTS}">
                    <option value="">--Please select a part--</option>
                    ${str}
                    <option value="other">Other (please specify)...</option>
                    </select>
                    <br /><label>If other, please specify name: </label>
                    <input type="text" name="part_${NUM_PARTS}_other_name" />
                    <br /><label>If other, please specify P/N: </label>
                    <input type="text" name="part_${NUM_PARTS}_other_num" />
                    <br /><label>If other, please specify manuf: </label>
                    <input type="text" name="part_${NUM_PARTS}_other_manuf" />
                    <br /><label>If other, please specify if OEM: </label>
                    <input type="radio" name="oem_${NUM_PARTS}" value="True" />
                    <label for="is_oem_1">OEM</label>
                    <input type="radio" name="oem1" value="False" />
                    <label for="not_oem_1">Aftermarket</label>
                    <input type="radio" name="oem1" value="False" />
                    <label for="unsure_if_oem_1">Not Sure</label>
                    <br /><label>Part Image (optional):</label>
                    <input type="file" name="part-img" />
                    <button class="del-img">Restore Default Img</button>
                </td>
                <td>
                    <button class="remove-part">Remove</button>
                </td>
            </tr>`
        );
        $('button.remove-part').off();
        $('button.del-img').off();
        $('button.remove-part').on('click', removePart);
        $('button.del-img').on('click', restoreDefaultImg);
    });

    $('#NUM_PARTS').replaceWith(`<input name="NUM_PARTS" id="NUM_PARTS" 
                                    type="hidden" value="${NUM_PARTS}" />`);
}


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
                                style="display: none;"/>`);

    $('checkbox.car-remove').attr('disabled', false);
    $('#car-add-form').hide();
}


function moveRow (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr');

    if ($(thisButton).hasClass('up')) {
        thisRow.prev().before(thisRow);
    } else {
        thisRow.next().after(thisRow);
    }
}


function removeStep (evt) {

    evt.preventDefault();

    let NUM_STEPS = Number($('#NUM_STEPS').val());
    NUM_STEPS -= 1;

    const thisButton = evt.target;
    const thisRow = $(thisButton).closest('tr');
    $(thisRow).remove();

    $('#NUM_STEPS').replaceWith(`<input name="NUM_STEPS" id="NUM_STEPS" 
                                    type="hidden" value="${NUM_STEPS}" />`);
   
}


function addStep (evt) {

    evt.preventDefault();

    let NUM_STEPS = Number($('#NUM_STEPS').val());
    NUM_STEPS += 1;

    $('#steps').append(
                `<tr>
                    <td>
                        <input name="step-text" value="Enter text here..." />
                    </td>
                    <td>
                        <input type="url" name="step_ref"
                            placeholder="https://example.com"
                            pattern="https://.*" disabled/>
                        <br />
                        <button class="edit ref">Edit Ref</button>
                        <button class="del-ref" disabled>Remove Ref</button>
                    </td>
                    <td>
                        <input name="step-img" type="file" value="/static/img/toolbox.png" disabled />
                        <br />
                        <button class="edit img">Edit Img</button>
                        <button class="del-img" disabled>Restore Default Img</button>
                    </td>
                    <td>
                        <button class="remove-step">Remove Step</button>
                    </td>
                    <td>
                        <button class="move up">UP</button>
                    </td>
                    <td>
                        <button class="move down">DOWN</button>
                    </td>
                </tr>`);

    $('#NUM_STEPS').replaceWith(`<input name="NUM_STEPS" id="NUM_STEPS" 
                                    type="hidden" value="${NUM_STEPS}" />`);

    
    $('button.move').off();
    $('button.remove-step').off();
    $('button.edit').off();
    $('button.del-ref').off();
    $('button.del-img').off();
    $('button.move').on('click', moveRow);
    $('button.remove-step').on('click', removeStep);
    $('button.edit').on('click', enableEditField);
    $('button.del-ref').on('click', removeReference);
    $('button.del-img').on('click', restoreDefaultImg);
}


function enableEditField (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisInput = $(thisButton).prevAll('input');
    const otherButton = $(thisButton).next('button');

    $(thisInput).attr('disabled', false);
    $(thisButton).attr('disabled', true);
    $(otherButton).attr('disabled', false);

}


function restoreDefaultImg (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisInput = $(thisButton).prevAll('input');
    const otherButton = $(thisButton).prevAll('button');
    $(thisInput).val('');
    $(thisInput).attr('disabled', true);
    $(thisButton).attr('disabled', true);
    $(otherButton).attr('disabled', false);
}


function removeReference (evt) {

    evt.preventDefault();

    const thisButton = evt.target;
    const thisInput = $(thisButton).prevAll('input');
    $(thisInput).val('');
}

// needs refactoring, but gets the job done
$('form').submit(function() {

    // const NUM_TOOLS = Number($('#NUM_TOOLS').val());
    // const NUM_PARTS = Number($('#NUM_PARTS').val());
    // const NUM_STEPS = Number($('#NUM_STEPS').val());

    $('input', this).prop('disabled', false);
});


$('#car-add').on('click', addVehicle);
$('#make').on('change', getModels);
$('#vehicle-submit').on('click', selectAddlVehicle);

$('button.remove-tool').on('click', removeTool);
$('#tool-add').on('click', addTool);

$('button.remove-part').on('click', removePart);
$('#part-add').on('click', addPart);

$('button.move').on('click', moveRow);
$('button.remove-step').on('click', removeStep);
$('#step-add').on('click', addStep);

$('button.edit').on('click', enableEditField);
$('button.del-img').on('click', restoreDefaultImg);
$('button.del-ref').on('click', removeReference);
