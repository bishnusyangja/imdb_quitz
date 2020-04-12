import React from 'react';
import {useState, useEffect} from 'react';
import { Button, Radio } from 'antd';
import Request from '../api'
import 'antd/dist/antd.css'

 const HomePage = () => {

    const [state, setState] = useState({
        data:null, start: false, value: ''
    });

    const [score, setScore] = useState(0);

    const [ans, setAnswer] = useState({});

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

    const submitAnswer = () => {
        let quiz_id = 1;
        Request().get('/quiz/'+quiz_id+'/', ans)
          .then(function (response) {
            setScore(response.data.score);
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

    const onOptionChange = (id, value) => {
        ans['que_'+id] = value
        setAnswer(ans);
        console.log("working", index, value);
        console.log(ans);
    }

    const radioStyle = {
      display: 'block',
      height: '30px',
      lineHeight: '30px',
    };

    const questionPage = (obj) => {
        return<> <div style={{marginTop: '40px'}}><h2>{index+1}. {obj.question} </h2></div>
            <Radio.Group onChange={(e) => {e.preventDefault(); onOptionChange(obj.id, e.target.value) }}
                    value={ans['que_'+obj.id]}>
                <Radio style={radioStyle} value='option1'> {obj.option1} </Radio>
                <Radio style={radioStyle} value='option2'> {obj.option2} </Radio>
                <Radio style={radioStyle} value='option3'> {obj.option3} </Radio>
                <Radio style={radioStyle} value='option4'> {obj.option4} </Radio>
            </Radio.Group>
      </>
    }



    if (state.start && state.data){
        ans_obj = {}
        for (let i in state.data){
            ans_obj['que_'+state.data[i].id] = '';
        }
        setAnswer(ans_obj)
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2> Quiz Questions</h2>
                    {state.data.map((ques) => (questionPage(ques, index))) }

               <Button type="primary" onClick={submitAnswer}>Submit Answer</Button>
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