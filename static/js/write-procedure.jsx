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
            <select name="first_tool_req">
            <option value="">--Please select a tool--</option>
            ${str}
            <option value="other">Other (please specify)...</option>
            </select>
            <br /><label>If other, please specify: </label>
            <input type="text" name="first_tool_other" />`
        );

    });   
}

$('#tool-adder').on('click', getTools);