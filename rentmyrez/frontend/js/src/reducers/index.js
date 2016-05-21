import Immutable from 'immutable';
import {LISTINGS_ADD} from './../actions/types';

const initialState = Immutable.fromJS({
	listings: []
});

export default function App (state = initialState, action) {
	switch (action.type) {
		case LISTINGS_ADD:
			return state.set('listings', state.get('listings').push(...action.listings));
		default:
			return initialState;
	}
}
