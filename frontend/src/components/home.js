import React from 'react';
import {useState, useEffect} from 'react';
import { Button, Radio, Table } from 'antd';
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
        data:[
            {question: 'Which of the following is abc ? ', key_id: 'sdff', option1: 'a dfaf', option2: 'b dfadf', option3: 'c fdfadf', option4: 'd eeee'},
            {question: 'Which of the following is dfdaf ? ', key_id: 'fdfsf', option1: 'a dfaf', optino2: 'b dfadf', option3: 'c ddd', option4: 'd dfafd'},
            {question: 'Which of the following is aaaaabc ? ', key_id: 'ffdsf', option1: 'a rrr', option2: 'b 000', option3: 'c ert', option4: 'd rrr'},
            {question: 'Which of the following is vvvv ? ', key_id: 'fdfas', option1: 'a yyyy', option2: 'b ooo', option3: 'c fdfadf', option4: 'd gggg'},
            {question: 'Which of the following is eeee ? ', key_id: 'fadfsaf', option1: 'a tttt', option2: 'b ccc', option3: 'c fdfadf', option4: 'd dfafd'},
            {question: 'Which of the following is rrrr ? ', key_id: 'dafdsaf', option1: 'a fdaf', option2: 'b dfadf', option3: 'c fdfadf', option4: 'd rrr'}
        ], start: true
    });

    const [is_submitted, setSubmitted] = useState(false);

    const [scoreBoard, setScoreBoard] = useState({data: [
        {'user_name': 'ramesh', 'user_username': 'Bishnu', 'score': 1},
        {'user_name': 'ram', 'user_username': 'yes', 'score': 5},
        {'user_name': 'hari', 'user_username': 'no', 'score': 4},
        {'user_name': 'sundar', 'user_username': 'heis', 'score': 3},
        {'user_name': 'santa', 'user_username': 'good', 'score': 9},
        {'user_name': 'ranju', 'user_username': 'handsome', 'score': 5},
        {'user_name': 'kamala', 'user_username': 'Bishnu', 'score': 52},
        {'user_name': 'dang', 'user_username': 'Bishnu', 'score': 5},
        ]
        });

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
        getQuiz();
    }

    const getScoreBoard = () => {
        Request().get('/score/list/', {page_size: pagination.pageSize})
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
        console.log(key_id);
        console.log(ans)
    }

    const radioStyle = {
      display: 'block',
      height: '30px',
      lineHeight: '30px',
    };

    const questionPage = (obj, index) => {
        return<> <div style={{marginTop: '40px'}} key={ans[obj.key_id]}><h2>{index+1}. {obj.question} </h2></div>
            <Radio.Group onChange={(e) => { onOptionChange(obj.key_id, e.target.value) }}
                    value={ans[obj.key_id]} >
                <Radio style={radioStyle} value='option1' > {obj.option1} </Radio>
                <Radio style={radioStyle} value='option2' > {obj.option2} </Radio>
                <Radio style={radioStyle} value='option3' > {obj.option3} </Radio>
                <Radio style={radioStyle} value='option4' > {obj.option4} </Radio>

            </Radio.Group>
      </>
    }

    const scorePage = (obj, index) => {
        return <>
            <div style={{marginTop: '20px'}}><h3>{index+1} {obj.user_name} {obj.user_username} {obj.score} </h3></div>
        </>
    }

    if (is_submitted && scoreBoard.data){
        return (
            <div style={{align: 'center', margin: '100px'}}>
                <h2> Your Score : {score}</h2>
                <h2> Top Score List</h2>
                    {state.data && <Table dataSource={scoreBoard.data} columns={columns} pagination={pagination}/>}
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