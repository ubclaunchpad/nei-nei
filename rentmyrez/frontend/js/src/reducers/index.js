import Immutable from 'immutable';
import {UPDATE_TEXT} from './../actions/types';

const initialState = Immutable.fromJS({text: ''});

export default function App (state = initialState, action) {
	switch (action.type) {
		case UPDATE_TEXT:
			return state.set('text', action.text);
		default:
			return initialState;
	}
}
