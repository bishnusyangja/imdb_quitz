import React from 'react';
import {useState} from 'react';
import { Form, Icon, Input, Button, Checkbox, notification } from 'antd';
import Request from '../api'

const RegisterForm = () => {

    const [form, setForm] = useState({username: '', password: '', code: '', confirm_password: '', name: ''});

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

    const notify_error = (data) => {
        let message = () => {
            let msg = ''
            for (var key in data){
                msg += key + ':  ' + data[key] + '...'
            }
            return msg;
        }

        notification.open({
            message: 'Register Error !!',
            description:
              message(),
            onClick: () => {
              console.log('Notification Clicked!');
            },
      });

    }

    const handleSubmit = (e) => {
        e.preventDefault();
        Request().post('/user/register/', form)
        .then(function (response) {
//            localStorage.setItem('authToken', response.data.token)
            notify_success();
          })
          .catch(function (err) {
//            let error = err.response.data
//            notify_error(error);
            console.log(err.response);
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
                <Input placeholder="username" onChange={(e) => { e.preventDefault();
                        setForm({
                            username: e.target.value,
                            password: form.password,
                            code: form.code,
                            confirm_password: form.confirm_password,
                            name: form.name
                            })}
                        }/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="Name" type="text" onChange={(e) => { e.preventDefault();
                        setForm({
                            name: e.target.value,
                            password: form.password,
                            username: form.username,
                            confirm_password: form.confirm_password,
                            code: form.code
                            })}
                        }/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="code" type="text" onChange={(e) => { e.preventDefault();
                        setForm({
                            code: e.target.value,
                            password: form.password,
                            username: form.username,
                            confirm_password: form.confirm_password,
                            name: form.name
                            })}
                        }/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="password" type="password" onChange={(e) => { e.preventDefault();
                        setForm({
                            password: e.target.value,
                            username: form.username,
                            code: form.code,
                            confirm_password: form.confirm_password,
                            name: form.name
                            })}
                        }/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="confirm password" type="password" onChange={(e) => { e.preventDefault();
                        setForm({
                            confirm_password: e.target.value,
                            password: form.password,
                            code: form.code,
                            username: form.username,
                            name: form.name
                            })}
                        }/>
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