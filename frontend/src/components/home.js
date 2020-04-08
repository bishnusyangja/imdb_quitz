import React from 'react';
import {useState, useEffect} from 'react';
import { Form, Icon, Input, Button, Checkbox } from 'antd';
import Request from '../api'

 const HomePage = () => {

    const [state,setState]=useState({
        data:null
    })

    useEffect(() => {
        getQuiz();
    },[])

    const getQuiz = () => {
        console.log("quiz");
        Request.get('/users/patient/')
          .then(function (response) {
            setState({data: response.data.results})
          })
          .catch(function (error) {
            console.log(error)
          })
          .finally(function () {
            console.log('finally block')
        });
    }

    return (
        <div style={{align: 'center', margin: '100px'}}>
            <Button type="primary">Start Quiz</Button>
        </div>
    )
  }

export default HomePage