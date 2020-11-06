"use strict";

function Title() {

    return (
        <React.Fragment>
            <h1>Let's write a procedure!</h1>
            <br />
            <form action="/procedure">
                <label>Procedure Name: </label>
                <input type="text" name="name" required/>
                <input type="submit" />
            </form>
            <br />
        </React.Fragment>
    );
}


function Procedures() {

    return (
        <React.Fragment>
            <h1>Browse all the available procedures:</h1>

        </React.Fragment>
    );
}


ReactDOM.render(<Title />, document.querySelector('#app-title'));
ReactDOM.render(<Procedures />, document.querySelector('#app-procedures'));