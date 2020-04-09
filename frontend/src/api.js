import axios from 'axios'
import {environment} from './settings'
const base_url = environment.REACT_APP_BACKEND_HOST
axios.defaults.baseURL = base_url
//axios.defaults.crossDomain = true
axios.defaults.headers.common['Content-Type'] = 'application/json'


const getRequestObject = () => {
    let authToken = localStorage.getItem('authToken');
    if (authToken != null && authToken != ''){
        axios.defaults.headers.common['Authorization'] = `Token ${authToken}`;
//        axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
//        axios.defaults.headers.common['Access-Control-Allow-Methods'] = '*';
    }
    return axios;

}

export default Request = {

    get : (url, params) => {
        return getRequestObject().get(url, {params: params});
    },

    post : (url, data) => {
        return getRequestObject().post(url, data)
    },

    patch : (url, data, params) => {
        return getRequestObject().patch(url, data, {params: params});
    },

    del : (url, params) => {
        return getRequestObject().delete(url, {params: params});
    },
}
