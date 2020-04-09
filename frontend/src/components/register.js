import React from 'react';
import {useState} from 'react';
import { Form, Icon, Input, Button, Checkbox, notification } from 'antd';
import Request from '../api'

const RegisterForm = () => {

    const [form, setForm] = useState({username: '', password: ''});

    const notify_success = () => {
      notification.open({
        message: 'Register Successful !!',
        description:
          'This is the content of the notification. This is the content of the notification. This is the content of the notification.',
        onClick: () => {
          console.log('Notification Clicked!');
        },
      });
    };

    const notify_error = () => {
        
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        Request.post('/api/auth-token/', form)
        .then(function (response) {
            localStorage.setItem('authToken', response.data.token)
            notify_success();
          })
          .catch(function (error) {
            console.log(error.response.data)
          })
          .finally(function () {
            console.log('finally block')
        });
    };

    return (
        <div style={{align: 'center', margin: '100px'}}>
        <h1>Register Form</h1>
            <Form className="register-form" style={{width: '400px', margin: '50px'}}>

            <Form.Item>
                <Input placeholder="username"/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="code" type="text"/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="password" type="password"/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="confirm password" type="password"/>
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit" className="login-form-button" onClick={handleSubmit}>
                    Register
                </Button>
            </Form.Item>

            </Form>
        </div>
    )
  }

 export default RegisterForm