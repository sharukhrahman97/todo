import axios from 'axios';

const loginAccount = async (email, password) => {
    let config = {
        method: 'post',
        url: `${import.meta.env.VITE_URL}/account/loginAccount`,
        headers: {},
        data: { email, password }
    };
    const response = await axios.request(config);    
    return response;
};

const createAccount = async (name, email, password) => {
    let config = {
        method: 'post',
        url: `${import.meta.env.VITE_URL}/account/createAccount`,
        headers: {},
        data: { name, email, password }
    };
    const response = await axios.request(config);
    return response;
};

export { loginAccount, createAccount }