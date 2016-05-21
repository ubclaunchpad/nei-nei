import {LISTINGS_ADD} from './types';

// listings {Array<Object>}
export const addListings = (listings) => ({listings, type: LISTINGS_ADD});
