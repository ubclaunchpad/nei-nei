import App from './components/App';
import {createStore} from 'redux';
import {Provider} from 'react-redux';
import React from 'react';
import Reducer from './reducers';
import {render} from 'react-dom';

let store = createStore(Reducer);

render(
	<Provider store={store}><App /></Provider>,
	document.getElementById('app')
);
