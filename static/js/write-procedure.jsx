'use strict';

function getTools (evt) {

    evt.preventDefault();

    $.get('/get-tools.json', (res) => { 

        let str = '';

        for (const tool of res) {
            str = str + `<option value="${tool}">${tool}</option>`;
        }

        $('#tool-list').append(
            `<br />
            <label>Tool Required: </label>
            <select name="tool_req">
            <option value="">--Please select a tool--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify: </label>
            <input type="text" name="tool_other" />`
        );

    });   
}


function getParts (evt) {
    
    evt.preventDefault();

    $.get('/get-parts.json', (res) => { 

        let str = '';

        for (const part of res) {
            str = str + `<option value="${part}">${part}</option>`;
        }

        $('#part-list').append(
            `<br />
            <label>Part Required: </label>
            <select name="part_req">
            <option value="">--Please select a part--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify: </label>
            <input type="text" name="part_other" />`
        );

    });   
}

$('#tool-adder').on('click', getTools);
$('#part-adder').on('click', getParts);