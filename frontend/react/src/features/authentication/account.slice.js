import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { loginAccount, createAccount } from './account.network';

export const loginAccountThunk = createAsyncThunk('account/loginAccount', async ({ email, password }) => {
    const response = await loginAccount(email, password);
    return response;
});

export const createAccountThunk = createAsyncThunk('account/createAccount', async ({ name, email, password }) => {
    const response = await createAccount(name, email, password);
    return response;
});

const initialState= {
    status: 'idle',
    account: {},
    error: null,
}

const accountSlice = createSlice({
    name: 'account',
    initialState: initialState,
    reducers: {
        resetState: (state) => initialState,
    },
    extraReducers: (builder) => {
        builder
            .addCase(loginAccountThunk.pending, (state, action) => {
                state.status = 'loading';
            })
            .addCase(loginAccountThunk.fulfilled, (state, action) => {
                state.status = 'success';
                state.account = action.payload;
            })
            .addCase(loginAccountThunk.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action;
            })
            .addCase(createAccountThunk.pending, (state, action) => {
                state.status = 'loading';
            })
            .addCase(createAccountThunk.fulfilled, (state, action) => {
                state.status = 'success';
                state.account = action.payload;
            })
            .addCase(createAccountThunk.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action;
            })
    },
});

export const { resetState } = accountSlice.actions;
export default accountSlice.reducer;