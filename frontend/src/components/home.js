import React from 'react';
import {useState, useEffect} from 'react';
import { Button, Radio } from 'antd';
import Request from '../api'

 const HomePage = () => {

    const [state, setState] = useState({
        data:null, start: false, value: ''
    })

    const getQuiz = () => {
        Request().get('/quiz/')
          .then(function (response) {
            setState({data: response.data, start: true})
          })
          .catch(function (error) {
            console.log("error at quiz")
          })
          .finally(function () {
            console.log('finally block at quiz')
        });
    }

    const startQuiz = () => {
        getQuiz();
    }

    const onOptionChange = () => {
        console.log("working");
    }

    const radioStyle = {
      display: 'block',
      height: '30px',
      lineHeight: '30px',
    };

    const questionPage = (obj, index) => {
        return<> <div style={{marginTop: '40px'}}><h2>{index+1}. {obj.question} </h2></div>
            <Radio.Group onChange={() => {onOptionChange(index) }} value=''>
                <Radio style={radioStyle} value='option1'> {obj.option1} </Radio>
                <Radio style={radioStyle} value='option2'> {obj.option2} </Radio>
                <Radio style={radioStyle} value='option3'> {obj.option3} </Radio>
                <Radio style={radioStyle} value='option4'> {obj.option4} </Radio>
            </Radio.Group>
      </>
    }

    if (state.start){
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2> Quiz Questions</h2>
                    {state.data.map((ques, index) => (questionPage(ques, index))) }
            </div>
        );
    }

    else
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2>After you click the button you can not go back.</h2>
                <Button type="primary" onClick={startQuiz}>Take The Movie Quiz</Button>
            </div>
        );
  }

export default HomePage