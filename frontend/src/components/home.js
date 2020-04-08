import React from 'react';
import {useState} from 'react';
import { Form, Icon, Input, Button, Checkbox } from 'antd';
import Request from '../api'

 const HomePage = () => {
    return (
        <div style={{align: 'center', margin: '100px'}}>
            <Button type="primary">Start Quiz</Button>
        </div>
    )
  }

export default HomePage