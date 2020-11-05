"use strict";

function ShopCat() {
    return (
        <React.Fragment>
            <p>TEST!!!!</p>
            <a href = "/home">Enter Now!</a>
        </React.Fragment>
    );
}

ReactDOM.render(<ShopCat />, document.querySelector('#app'));