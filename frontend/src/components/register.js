import React from 'react';
import {useState} from 'react';
import { Form, Icon, Input, Button, Checkbox } from 'antd';
import Request from '../api'

const RegisterForm = () => {

    const handleSubmit = () => {
        console.log("Submitted");
    }

    return (
        <div style={{align: 'center', margin: '100px'}}>
        <h1>Register Form</h1>
            <Form onSubmit={handleSubmit} className="register-form" style={{width: '400px', margin: '50px'}}>

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

 export default RegisterForm