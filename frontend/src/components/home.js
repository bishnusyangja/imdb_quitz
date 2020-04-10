import React from 'react';
import {useState, useEffect} from 'react';
import { Form, Icon, Input, Button, Checkbox } from 'antd';
import Request from '../api'

 const HomePage = () => {

    const [state, setState] = useState({
        data:null, start: false
    })

    useEffect(() => {
        getQuiz();
    },[])

    const getQuiz = () => {
        console.log("requesting quiz")
        Request().get('/quiz/', {})
          .then(function (response) {
            console.log("success response at quiz, ", response.data)
            setState({data: response.data, start: state.start})
          })
          .catch(function (error) {
            console.log("error at quiz")
          })
          .finally(function () {
            console.log('finally block at quiz')
        });
    }

    const startQuiz = () => {
        setState({data: state.data, start: true});
        getQuiz();
    }

    if (state.start)
        return (
            <div style={{align: 'center', margin: '100px'}}>
                Listing Quiz
            </div>
        );
    else
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2>After you click the button you can not go back.</h2>
                <Button type="primary" onClick={startQuiz}>Take The Movie Quiz</Button>
            </div>
        );
  }

export default HomePage