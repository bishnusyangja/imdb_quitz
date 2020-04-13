import React from 'react';
import {useState, useEffect} from 'react';
import { Button, Radio, Table, Pagination } from 'antd';
import Request from '../api'

 const HomePage = () => {

    const pagination = {pageSize: 5, page: 1};

    const defaultAnswer = (data) => {
        let ans_obj = {}
        for (let i in data){
            ans_obj[data[i].key_id] = '';
        }
        return ans_obj;
    }

    const [state, setState] = useState({
        data:null, start: false, count: 0
    });

    const [is_submitted, setSubmitted] = useState(false);

    const [scoreBoard, setScoreBoard] = useState({data: null});

    const [score, setScore] = useState(0);

    const [ans, setAnswer] = useState({});

    const getQuiz = (page, pageSize) => {
        Request().get('/quiz/', {page: page, page_size: pageSize})
          .then((response) => {
            setState({data: response.data.results, count: response.data.count, start: true});
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
            setSubmitted(true);
            getScoreBoard();
          })
          .catch((error) => {
            console.log("error in quiz submission")
          })
          .finally(() => {
            console.log('finally block at quiz')
        });
    }

    const startQuiz = () => {
        getQuiz(1, pagination.pageSize);
    }

    const getScoreBoard = () => {
        Request().get('/score/list/', {page_size: pagination.pageSize})
          .then((response) => {
            setScoreBoard({data: response.data.results});
          })
          .catch((error) => {
            console.log("error at quiz", error)
          })
          .finally(() => {
            console.log('finally block at quiz')
        });
    }

    const columns = [
      {
        title: 'SN',
        dataIndex: '',
        key: 'patient_name',
        render: (text, record, index) =>  (pagination.page - 1) * pagination.pageSize + index+1,
      },
      {
        title: 'Name',
        dataIndex: 'user_name',
        key: 'name',
      },
      {
        title: 'UserName',
        dataIndex: 'user_username',
        key: 'username',
      },
      {
        title: 'Score',
        dataIndex: 'score',
        key: 'score',
      },
   ]

    const onOptionChange = (key_id, value) => {
        ans[key_id] = value
        setAnswer(ans);
    }

    const radioStyle = {
      display: 'block',
      height: '30px',
      lineHeight: '30px',
    };

    const questionPage = (obj, index) => {
        return<div key={obj.key_id}>
            <div style={{marginTop: '40px'}}><h2>{index+1}. {obj.question} </h2></div>
            <Radio.Group onChange={(e) => { onOptionChange(obj.key_id, e.target.value) }}
                    value={ans[obj.key_id]}>
                <Radio style={radioStyle} value='option1' checked={ans[obj.key_id]=='option1'} > {obj.option1} </Radio>
                <Radio style={radioStyle} value='option2' checked={ans[obj.key_id]=='option2'} > {obj.option2} </Radio>
                <Radio style={radioStyle} value='option3' checked={ans[obj.key_id]=='option3'} > {obj.option3} </Radio>
                <Radio style={radioStyle} value='option4' checked={ans[obj.key_id]=='option4'} > {obj.option4} </Radio>

            </Radio.Group>
      </div>
    }

    const scorePage = (obj, index) => {
        return <>
            <div style={{marginTop: '20px'}}><h3>{index+1} {obj.user_name} {obj.user_username} {obj.score} </h3></div>
        </>
    }

    const onPageChange = (page, pageSize) => {
        getQuiz(page, pageSize);
    }

    if (is_submitted && scoreBoard.data){
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2> Your Score : {score}</h2>
                <h2> Top Score List</h2>
                    {state.data && <Table dataSource={scoreBoard.data} columns={columns} pagination={false}/>}
                    <Pagination defaultCurrent={1}
                              pageSize={pagination.pageSize}
                              total={state.count}
                              onChange={onPageChange}/>
            </div>
        );

    } else if (state.start && state.data){
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2> Quiz Questions</h2>
                    {state.data.map((ques, index) => (questionPage(ques, index))) }
               <br/>
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