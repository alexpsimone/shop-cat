"use strict";

function Title() {
    return (
        <React.Fragment>
            <p>Let's write a procedure!</p>
            <br />
            <form action="/procedure">
                <label>Procedure Name: </label>
                <input type="text" name="name" required/>
                <br />
                <input type="submit" />
            </form>
        </React.Fragment>
    );
}

function Tools() {
    return (
        <p>THIS IS A TOOL TEST.</p>
    );
}

function Parts() {
    return (
        <p>THIS IS A PART TEST.</p>
    );
}

function Steps() {
    return (
        <p>THIS IS A STEP TEST.</p>
    );
}
// const step_info ='<label>Step 1: </label><input type="text" name="name" /><button id="add-step">Add Step</button><br /><br />'

// document.querySelector('#add-step').addEventListener('click', (evt) => {
// 	 document.querySelector('#procedure-steps').insertAdjacentHTML('beforeend', step_info);
// });

ReactDOM.render(<Title />, document.querySelector('#app-title'));
ReactDOM.render(<Tools />, document.querySelector('#app-tools'));
ReactDOM.render(<Parts />, document.querySelector('#app-parts'));
ReactDOM.render(<Steps />, document.querySelector('#app-steps'));