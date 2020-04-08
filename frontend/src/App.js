import React from 'react';
import {useState} from 'react';
import { Form, Icon, Input, Button, Checkbox } from 'antd';
import './App.css';
import 'antd/dist/antd.css'
import { Row, Col } from 'antd';
import Request from './api'


function App() {
  let auth_token = localStorage.getItem('auth_token', '')
  const [isLoggedin, setIsLoggedin]=useState(false);

  const handleLogin = () => {
    console.log("Log in")
  }

  const handleRegister = () => {
    console.log("register")
  }

  const login_form = () => {
    return (
        <div style={{align: 'center', margin: '100px'}}>
        <h1>Login Form</h1>
            <Form onSubmit={handleLogin} className="login-form" style={{width: '400px', margin: '50px'}}>

            <Form.Item>
                <Input placeholder="username"/>
            </Form.Item>

            <Form.Item>
                <Input placeholder="password" type="password"/>
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit" className="login-form-button">
                    Log in
                </Button>
            </Form.Item>

            </Form>
        </div>
    )
  }

  const register_form = () => {
    return (
        <div style={{align: 'center', margin: '100px'}}>
        <h1>Register Form</h1>
            <Form onSubmit={handleRegister} className="register-form" style={{width: '400px', margin: '50px'}}>

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
                <Button type="primary" htmlType="submit" className="login-form-button">
                    Register
                </Button>
            </Form.Item>

            </Form>
        </div>
    )
  }


if (!isLoggedin)
  return (
      <>
      <Row>
          <Col span={10} >
               {login_form()}
          </Col>
          <Col span={14} >
            {register_form()}
          </Col>
      </Row>
      </>
  );

else
    return (<>

    </>);
}


export default App;
