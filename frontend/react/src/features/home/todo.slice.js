import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { readAccount, createTodo, updateTodo, readAllTodo, deleteTodo } from './todo.network';

export const readAccountThunk = createAsyncThunk('account/readAccount', async ({user}) => {
    const response = await readAccount(user);
    return response;
});

export const createTodoThunk = createAsyncThunk('todo/createTodo', async ({ user, title, description, status }) => {
    const response = await createTodo(user, title, description, status);
    return response;
});

export const updateTodoThunk = createAsyncThunk('todo/updateTodo', async ({ user, id, title, description, status }) => {
    const response = await updateTodo(user, id, title, description, status);
    return response;
});

export const readAllTodoThunk = createAsyncThunk('todo/readAllTodo', async ({ user, page, limit,filter }) => {
    const response = await readAllTodo(user, page, limit,filter);
    return response;
});

export const deleteTodoThunk = createAsyncThunk('todo/deleteTodo', async ({ user, id }) => {
    const response = await deleteTodo(user, id);
    return response;
});
const initialState = {
    status: 'idle',
    account: {},
    cud:{},
    result: {},
    error: null,
}

const todoSlice = createSlice({
    name: 'todo',
    initialState: initialState,
    reducers: {
        resetState: (state) => initialState,
    },
    extraReducers: (builder) => {
        builder
            .addCase(readAccountThunk.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(readAccountThunk.fulfilled, (state, action) => {
                state.status = 'success';
                state.account = action.payload;
            })
            .addCase(readAccountThunk.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action;
            })
            .addCase(createTodoThunk.pending, (state, action) => {
                state.status = 'loading';
            })
            .addCase(createTodoThunk.fulfilled, (state, action) => {
                state.status = 'success';
                state.cud = action.payload
            })
            .addCase(createTodoThunk.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action
            })
            .addCase(updateTodoThunk.pending, (state, action) => {
                state.status = 'loading';
            })
            .addCase(updateTodoThunk.fulfilled, (state, action) => {
                state.status = 'success';
                state.cud = action.payload
            })
            .addCase(updateTodoThunk.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action
            })
            .addCase(readAllTodoThunk.pending, (state, action) => {
                state.status = 'loading';
            })
            .addCase(readAllTodoThunk.fulfilled, (state, action) => {
                state.status = 'success';
                state.result = action.payload
            })
            .addCase(readAllTodoThunk.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action
            })
            .addCase(deleteTodoThunk.pending, (state, action) => {
                state.status = 'loading';
            })
            .addCase(deleteTodoThunk.fulfilled, (state, action) => {
                state.status = 'success';
                state.cud = action.payload
            })
            .addCase(deleteTodoThunk.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action
            })
    },
});
export const { resetState } = todoSlice.actions;
export default todoSlice.reducer;