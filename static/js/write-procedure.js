'use strict';

let NUM_TOOLS = 0;
let NUM_PARTS = 0;
let NUM_STEPS = 0;


function requireOtherToolName (evt) {

    
    const thisSelect = evt.target;
    const otherName = $(thisSelect).siblings('input.tool-other-name');
    console.log(otherName);

    if ($(thisSelect).val() === 'other') {
        $(otherName).attr('required', true);
    } else {
        $(otherName).attr('required', false);
    };
}


function requireOtherPartName (evt) {

    const thisSelect = evt.target;
    const otherName = $(thisSelect).siblings('input.part-other-name');
    console.log(otherName);
    console.log($(thisSelect).val());

    if ($(thisSelect).val() === 'other') {
        $(otherName).attr('required', true);
    } else {
        $(otherName).attr('required', false);
    };
}


function getTools (evt) {

    evt.preventDefault();
    NUM_TOOLS += 1;

    $.get('/get-tools.json', (res) => { 
        
        let str = '';
        for (const tool of res) {
            str = str + `<option value="${tool}">${tool}</option>`;
        }

        $('#tool-list').append(
            `<div class="card sub-item">
                <label>Tool #${NUM_TOOLS}: </label>
                <select class="custom-select" name="tool_req_${NUM_TOOLS}" class="tool-req" id="tool${NUM_TOOLS}">
                <option value="">--Please select a tool--</option>
                ${str}
                <option value="other">Other (please specify)...</option>
                </select>
                <div class="card sub-other">
                    <label>If other, please specify: </label>
                    <input type="text" class="tool-other-name form-control" name="tool_other_${NUM_TOOLS}" />
                    <br />
                    <label>Other Tool Image (optional):
                    <input type="file" class="tool-other-img form-control-file" name="tool_img_${NUM_TOOLS}" />
                </div>
            </div>`
        );

        $('select.tool-req').off();
        $('select.tool-req').on('change', requireOtherToolName);

    });

    $('#NUM_TOOLS').replaceWith(`<input name="NUM_TOOLS" id="NUM_TOOLS" 
            type="number" value="${NUM_TOOLS}" style="display: none;"/>`);
    
}


function getParts (evt) {
    
    evt.preventDefault();

    $.get('/get-parts.json', (res) => { 
        
        NUM_PARTS += 1;
        let str = '';

        for (const part of res) {
            str = str + `<option value="${part}">${part}</option>`;
        }

        $('#part-list').append(
            `<div class="card sub-item">
                <label>Part #${NUM_PARTS}: </label>
                <select class="custom-select" name="part_req_${NUM_PARTS}" class="part-req" id="part${NUM_PARTS}">
                <option value="">--Please select a part--</option>
                ${str}
                <option value="other">Other (please specify)...</option>
                </select>
                <div class="card sub-other">
                    <label for="part-other-name">If other, please specify name: </label>
                    <input type="text" class="form-control part-other-name" name="part_${NUM_PARTS}_other_name" />
                    <label for="part-other-num">If other, please specify P/N: </label>
                    <input type="text" class="form-control part-other-num" name="part_${NUM_PARTS}_other_num" />
                    <label for="part-other-manuf">If other, please specify manuf: </label>
                    <input type="text" class="form-control part-other-manuf" name="part_${NUM_PARTS}_other_manuf" />
                    <label>If other, please specify if OEM: </label><br />
                    <input type="radio" class="form-check part-check part-other-isoem" name="oem_${NUM_PARTS}" value="True" />
                    <label for="part-other-isoem">OEM</label>
                    <input type="radio" class="form-check part-check part-other-notoem" name="oem1" value="False" />
                    <label for="part-other-not-oem">Aftermarket</label>
                    <input type="radio" class="form-check part-check part-other-unsure" name="oem1" value="False" />
                    <label for="part-other-unsure">Not Sure</label>
                    <label>Other Part Image (optional):
                    <input type="file" class="form-control-file" name="part_img_${NUM_PARTS}" />
                </div>
            </div>`
        );

        $('select.part-req').off();
        $('select.part-req').on('change', requireOtherPartName);

        $('#NUM_PARTS').replaceWith(`<input name ="NUM_PARTS" id="NUM_PARTS" 
            type="number" value="${NUM_PARTS}" style="display: none;"/>`);

    });   
}

 
// function enableURL(evt) {

//     const thisCheck = evt.target;
//     const thisURL = $(thisCheck).siblings('input.ref-url');

//     if ($(thisURL).attr('disabled', true)) {
//         $(thisURL).attr('disabled', false);
//     } else if ($(thisURL).attr('disabled', false)) {
//         $(thisURL).attr('disabled', true);
//     };
// }

function addStep (evt) {
    
    evt.preventDefault();
        
    NUM_STEPS += 1;

    $('#step-list').append(`<div class="card sub-item">
                            <p>Step ${NUM_STEPS}: </p>
                            <textarea class="form-control" name="step_text_${NUM_STEPS}"></textarea>
                            <label for="ref_text_${NUM_STEPS}">
                            Reference URL (optional, must start with https://): </label>
                            <input type="url" class="form-control ref-url" name="ref_text_${NUM_STEPS}"
                            placeholder="https://example.com"
                            pattern="https://.*" />
                            <label for="img_file_${NUM_STEPS}">
                            Image (optional): </label>
                            <input type="file" class="form-control-file" id="step_img_${NUM_STEPS}"
                            name="step_img_${NUM_STEPS}" />
                            </div>`);
    
    // $('input.ref-check').off(); 
    // $('input.ref-check').on('click', enableURL);

    $('#NUM_STEPS').replaceWith(`<input name ="NUM_STEPS" id="NUM_STEPS" 
        type="number" value="${NUM_STEPS}" style="display: none;"/>`);
 
}

$('#tool-adder').on('click', getTools);
$('#part-adder').on('click', getParts);
$('#step-adder').on('click', addStep);

function requireStep (evt) {

    if (NUM_STEPS === 0) {
        evt.preventDefault();
        alert('All procedures must have at least one step!');
    };
}

$('form').on('submit', requireStep)