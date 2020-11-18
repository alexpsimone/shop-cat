const Router = ReactRouterDOM.BrowserRouter;
const Route =  ReactRouterDOM.Route;
const Link =  ReactRouterDOM.Link;
const Prompt =  ReactRouterDOM.Prompt;
const Switch = ReactRouterDOM.Switch;
const Redirect = ReactRouterDOM.Redirect;
const useParams = ReactRouterDOM.useParams;
const useHistory = ReactRouterDOM.useHistory;
// same as the above but using destructing syntax 
// const { useHistory, useParams, Redirect, Switch, Prompt, Link, Route } = ReactRouterDOM;

function CreateAcct () {
    return (

    <React.fragment>
        <h2>Create a ShopCat Account!</h2>
    </React.fragment>

)}

function LogIn () {
    return <div>Log in.</div>
}

function Home () {
    return <div>Home.</div>
}


function App() {
    return (
      <Router>
        <div>
          <Switch>
            <Route path="/home">
              <Home />
            </Route>
            <Route path="/login">
              <LogIn />
            </Route>
            <Route path="/">
              <CreateAcct />
            </Route>
          </Switch>
        </div>
      </Router>
    );
}

ReactDOM.render(<App />, document.getElementById('root'))