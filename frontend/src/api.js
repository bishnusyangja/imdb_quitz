import axios from 'axios'
import {environment} from './settings'
const base_url = environment.REACT_APP_BACKEND_HOST
axios.defaults.baseURL = base_url
axios.defaults.crossDomain = true
axios.defaults.credentials = true


const getRequestObject = () => {
    let authToken = localStorage.getItem('authToken');
    console.log("token ", authToken)
    if (authToken != null && authToken != ''){
        axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
        axios.defaults.headers.common['Authorization'] = `Token ${authToken}`;
    }
    return axios;
}

export default Request = () => {

    let authToken = localStorage.getItem('authToken');
    return {
        get : (url, params) => {
            return getRequestObject().get(url, {params: params,
                headers: {'Authorization': 'Token '+authToken,
                    'Access-Control-Allow-Origin': '*'
                }
            });
        },

        post : (url, data) => {
            return getRequestObject().post(url, data)
        },

        patch : (url, data, params) => {
            return getRequestObject().patch(url, data, {params: params});
        },

        del : (url, params) => {
            return getRequestObject().delete(url, {params: params});
        }
    }
}
