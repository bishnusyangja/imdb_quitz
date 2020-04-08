import React from 'react';
import {useState} from 'react';
import { Form, Icon, Input, Button, Checkbox } from 'antd';
import Request from '../api'

 const LoginForm = ({setIsLoggedin}) => {

    const [form, setForm] = useState({username: '', password: ''});

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("submited");
        console.log("form data", form)
        Request.post('/api/auth-token/', form)
        .then(function (response) {
            setIsLoggedin({status: true});
            localStorage.setItem('authToken', response.data.token)
          })
          .catch(function (error) {
            console.log(error)
          })
          .finally(function () {
            console.log('finally block')
        });
    };

    return (
        <div style={{align: 'center', margin: '100px'}}>
        <h1>Login Form</h1>
            <Form className="login-form" style={{width: '400px', margin: '50px'}}>

            <Form.Item>
                <Input placeholder="username" onChange={(e) => { e.preventDefault();
                        setForm({
                            username: e.target.value,
                            password: form.password})}
                        }/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="password" type="password" onChange={(e) => { e.preventDefault();
                        setForm({
                            username: form.username,
                            password: e.target.value})}
                        } />
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit" className="login-form-button" onClick={handleSubmit}>
                    Log in
                </Button>
            </Form.Item>

            </Form>
        </div>
    )
  }

 export default LoginForm
