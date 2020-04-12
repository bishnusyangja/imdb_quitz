import React from 'react';
import {useState, useEffect} from 'react';
import { Button, Radio } from 'antd';
import Request from '../api'

 const HomePage = () => {

    const defaultAnswer = (data) => {
        let ans_obj = {}
        for (let i in data){
            ans_obj[data[i].key_id] = '';
        }
        return ans_obj;
    }

    const [state, setState] = useState({
        data:null, start: false
    });

    const [is_submitted, setSubmitted] = useState(false);

    const [scoreBoard, setScoreBoard] = useState({data: null});

    const [score, setScore] = useState(0);

    const [ans, setAnswer] = useState({});

    const getQuiz = () => {
        Request().get('/quiz/')
          .then((response) => {
            console.log(response.data);
            setState({data: response.data, start: true});
            setAnswer(defaultAnswer(response.data));
          })
          .catch((error) => {
            console.log("error at quiz", error)
          })
          .finally(() => {
            console.log('finally block at quiz')
        });
    }

    const submitAnswer = () => {
        let quiz_id = 1;
        Request().post('/quiz/'+quiz_id+'/', ans)
          .then((response) => {
            setScore(response.data.score);
          })
          .catch((error) => {
            console.log("error in quiz submission")
          })
          .finally(() => {
            console.log('finally block at quiz')
        });
    }

    const startQuiz = () => {
        getQuiz();
    }

    const getScoreBoard = () => {
        Request().get('/quiz/')
          .then((response) => {
            setScoreBoard({data: response.data});
          })
          .catch((error) => {
            console.log("error at quiz", error)
          })
          .finally(() => {
            console.log('finally block at quiz')
        });
    }

    const onOptionChange = (key_id, value) => {
        ans[key_id] = value
        setAnswer(ans);
        console.log("working", key_id, value);
        console.log(ans);
    }

    const radioStyle = {
      display: 'block',
      height: '30px',
      lineHeight: '30px',
    };

    const questionPage = (obj, index) => {
        return<> <div style={{marginTop: '40px'}}><h2>{index+1}. {obj.question} </h2></div>
            <Radio.Group onChange={(e) => { onOptionChange(obj.key_id, e.target.value) }}
                    value={ans[obj.key_id]}>
                <Radio style={radioStyle} value='option1' > {obj.option1} </Radio>
                <Radio style={radioStyle} value='option2' > {obj.option2} </Radio>
                <Radio style={radioStyle} value='option3' > {obj.option3} </Radio>
                <Radio style={radioStyle} value='option4' > {obj.option4} </Radio>

            </Radio.Group>
      </>
    }

    const scorePage = (obj, index) => {
        return <>
            <div style={{marginTop: '20px'}}><h2>{index+1}. {obj.question} </h2></div>
        </>
    }

    if (is_submitted){
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2> Your Score : {score}</h2>
                    {scoreBoard.data.map((item, index) => (scorePage(item, index))) }
               <Button type="primary" onClick={submitAnswer}>Submit Answer</Button>
            </div>
        );

    } else if (state.start && state.data){
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2> Quiz Questions</h2>
                    {state.data.map((ques, index) => (questionPage(ques, index))) }

               <Button type="primary" onClick={submitAnswer}>Submit Answer</Button>
            </div>
        );
    } else
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2>After you click the button you can not go back.</h2>
                <Button type="primary" onClick={startQuiz}>Take The Movie Quiz</Button>
            </div>
        );
  }

export default HomePage