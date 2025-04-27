import axios from 'axios';

const readAccount = async (user) => {
    let config = {
        method: 'get',
        url: `${import.meta.env.VITE_URL}/account/readAccount`,
        headers: {
            'cl-x-token': user['cl-x-token'],
            'cl-x-refresh': user['cl-x-refresh']
        },
        data: {}
    };
    const response = await axios.request(config);
    return response;
};

const createTodo = async (user, title, description, status) => {
    let config = {
        method: 'post',
        url: `${import.meta.env.VITE_URL}/todo/createTodo`,
        headers: {
            'cl-x-token': user['cl-x-token'],
            'cl-x-refresh': user['cl-x-refresh']
        },
        data: { title, description, status }
    };
    const response = await axios.request(config);
    return response;
};

const updateTodo = async (user, id, title, description, status) => {
    let config = {
        method: 'put',
        url: `${import.meta.env.VITE_URL}/todo/updateTodo`,
        headers: {
            'cl-x-token': user['cl-x-token'],
            'cl-x-refresh': user['cl-x-refresh']
        },
        data: { id, title, description, status }
    };
    const response = await axios.request(config);
    return response;
};

const readAllTodo = async (user, page, limit, filter) => {
    let config = {
        method: 'get',
        url: `${import.meta.env.VITE_URL}/todo/readAllTodo?page=${page}&limit=${limit}&status=${filter}`,
        headers: {
            'cl-x-token': user['cl-x-token'],
            'cl-x-refresh': user['cl-x-refresh']
        },
        data: {}
    };
    const response = await axios.request(config);
    return response;
};

const deleteTodo = async (user, id) => {
    let config = {
        method: 'delete',
        url: `${import.meta.env.VITE_URL}/todo/deleteTodo`,
        headers: {
            'cl-x-token': user['cl-x-token'],
            'cl-x-refresh': user['cl-x-refresh']
        },
        data: { id }
    };
    const response = await axios.request(config);
    return response;
};

export { readAccount, createTodo, updateTodo, readAllTodo, deleteTodo }