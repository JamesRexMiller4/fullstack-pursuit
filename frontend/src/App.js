import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import './App.css';
import FormView from './components/FormView/FormView';
import QuestionView from './components/QuestionView/QuestionView';
import Header from './components/Header/Header';
import QuizView from './components/QuizView/QuizView';


const App = () => {
  return (
    <div className="App">
      <Header path={'/'} />
      <Router>
        <Switch>
          <Route path={'/'} exact render={() => <QuestionView/>} />
          <Route path={'/add'} render={() => <FormView/>} />
          <Route path={"/play"} render={() => <QuizView/>} />
          <Route component={QuestionView} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;