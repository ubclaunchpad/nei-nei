import {render} from 'react-dom';
import {createStore} from 'redux';
import {Provider} from 'react-redux';
import App from './components/App';
import React from 'react';
import Reducer from './reducers';

let store = createStore(Reducer);

render(
	<Provider store={store}><App /></Provider>,
	document.getElementById('app')
);
