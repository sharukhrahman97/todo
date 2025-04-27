import { combineReducers } from 'redux';
import accountSlice from '../features/authentication/account.slice';
import todoSlice from '../features/home/todo.slice';

const rootReducer = combineReducers({
    account: accountSlice,
    todo: todoSlice
});

export default rootReducer;
