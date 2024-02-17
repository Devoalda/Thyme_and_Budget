import axios from 'axios';
let refresh = false;

axios.interceptors.response.use(resp => resp, async error =>
{
    if (error.response.status === 401 && !refresh)
    {
        // check if user is authenticated
        const refresh_token = localStorage.getItem("refresh");
        if (refresh_token){
            refresh = true;
            console.log(localStorage.getItem("refresh"))
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/token/refresh/`,
                {
                    refresh: localStorage.getItem("refresh")
                }, { headers: { 'Content-Type': 'application/json' } }, { withCredentials: true });

            if (response.status === 200)
            {
                axios.defaults.headers.common['Authorization'] = `Bearer ${response.data['access']}`;
                localStorage.setItem("token", response.data.access);
                localStorage.setItem("refresh", response.data.refresh);
                console.log("refreshed");
                console.log(localStorage.getItem("access"))
                console.log(localStorage.getItem("refresh"))
                return axios(error.config);
            }
        }
    }
    refresh = false;
    return error;
});