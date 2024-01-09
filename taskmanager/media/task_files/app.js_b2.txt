// eslint-disable-next-line
import React, { Component, useState, useRef } from 'react';
import './App.css';
import PersonList from './PersonList';


function Task1() {
  const result = 5 + 2;
  return (
    <div>
      <h2>Задание 1</h2>
      <p>Результат выражения 5 + 2: {result}</p>
    </div>
  );
}

function Task2() {
// eslint-disable-next-line
const [fullName] = useState('Жарылкасын Нуралы Ерланович');
// eslint-disable-next-line
const [age] = useState(17);

  const styles = {
    fontSize: '24px',
    color: 'blue',
    fontWeight: 'bold',
  };

  return (
    <div>
      <h2>Задание 2</h2>
      <p style={styles}>ФИО: {fullName}</p>
      <p style={styles}>Возраст: {age}</p>
    </div>
  );
}

class Calculator extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayValue: '0',
      prevValue: null,
      operator: null,
      waitingForOperand: false,
    };
    this.userInputRef = React.createRef(); // Для получения доступа к элементу input
  }

  inputDigit = (digit) => {
    const { displayValue, waitingForOperand } = this.state;

    if (waitingForOperand) {
      this.setState({
        displayValue: String(digit),
        waitingForOperand: false,
      });
    } else {
      this.setState({
        displayValue: displayValue === '0' ? String(digit) : displayValue + digit,
      });
    }
  };

  inputDecimal = () => {
    const { displayValue, waitingForOperand } = this.state;

    if (waitingForOperand) {
      this.setState({
        displayValue: '.',
        waitingForOperand: false,
      });
    } else if (displayValue.indexOf('.') === -1) {
      this.setState({
        displayValue: displayValue + '.',
      });
    }
  };

  clearDisplay = () => {
    this.setState({
      displayValue: '0',
    });
  };

  performOperation = (nextOperator) => {
    const { displayValue, operator, prevValue } = this.state;
    const inputValue = parseFloat(displayValue);

    if (prevValue == null) {
      this.setState({
        prevValue: inputValue,
        waitingForOperand: true,
        operator: nextOperator,
      });
    } else if (operator) {
      const currentValue = prevValue || 0;
      const computedValue = this.computeOperation(currentValue, inputValue, operator);

      this.setState({
        displayValue: String(computedValue),
        prevValue: computedValue,
        waitingForOperand: true,
        operator: nextOperator,
      });
    }
  };

  computeOperation = (prevValue, nextValue, operator) => {
    switch (operator) {
      case '+':
        return prevValue + nextValue;
      case '-':
        return prevValue - nextValue;
      case '×':
        return prevValue * nextValue;
      case '÷':
        return prevValue / nextValue;
      default:
        return nextValue;
    }
  };

  changeListColor = () => {
    const userInput = this.userInputRef.current;
    let lastPickedColor = userInput.value;
    const listItem = document.querySelectorAll('li');
    const p = document.getElementById('myHeading');

    for (let i = 0; i < listItem.length; i++) {
      listItem[i].style.color = lastPickedColor;
    }
    p.innerHTML = 'The list color is: ' + userInput.value;
  };

  addItem = () => {
    const list = document.querySelector('ul');
    const addItemInput = document.querySelector('.addItemInput');
    const li = document.createElement('li');
    li.textContent = addItemInput.value;
    li.style.color = this.state.displayValue;
    list.appendChild(li);
    addItemInput.value = '';
  };

  removeLastItem = () => {
    const list = document.querySelector('ul');
    const lastChild = list.lastElementChild;
    list.removeChild(lastChild);
  };

  handleMouseOver = (event) => {
    if (event.target.tagName === 'LI') {
      event.target.style.textTransform = 'uppercase';
    }
  };

  handleMouseOut = (event) => {
    if (event.target.tagName === 'LI') {
      event.target.style.textTransform = 'lowercase';
    }
  };

  render() {
    const { displayValue } = this.state;

    return (
      <div className="calculator">
        <input type="text" className="display" value={displayValue} readOnly />
        <div className="buttons">
          <div className="button-row">
            <button className="button" onClick={() => this.clearDisplay()}>C</button>
            <button className="button" onClick={() => this.inputDigit(7)}>7</button>
            <button className="button" onClick={() => this.inputDigit(8)}>8</button>
            <button className="button" onClick={() => this.inputDigit(9)}>9</button>
            <button className="button" onClick={() => this.performOperation('÷')}>÷</button>
          </div>
          <div className="button-row">
            <button className="button" onClick={() => this.inputDigit(4)}>4</button>
            <button className="button" onClick={() => this.inputDigit(5)}>5</button>
            <button className="button" onClick={() => this.inputDigit(6)}>6</button>
            <button className="button" onClick={() => this.performOperation('×')}>×</button>
          </div>
          <div className="button-row">
            <button className="button" onClick={() => this.inputDigit(1)}>1</button>
            <button className="button" onClick={() => this.inputDigit(2)}>2</button>
            <button className="button" onClick={() => this.inputDigit(3)}>3</button>
            <button className="button" onClick={() => this.performOperation('-')}>-</button>
          </div>
          <div className="button-row">
            <button className="button" onClick={() => this.inputDigit(0)}>0</button>
            <button className="button" onClick={() => this.inputDecimal()}>.</button>
            <button className="button" onClick={() => this.performOperation('+')}>+</button>
            <button className="button" onClick={() => this.performOperation('=')}>=</button>
          </div>
        </div>
      </div>
    );
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTask: null,
    };
  }

  renderTask(taskNumber) {
    switch (taskNumber) {
      case 1:
        return <Task1 />;
      case 2:
        return <Task2 />;
      case 3:
        return <Calculator />;
      case 4:
        return <PersonList />; // Добавьте PersonList для 4 задания
      default:
        return null;
    }
  }

  setActiveTask(taskNumber) {
    this.setState({ activeTask: taskNumber });
  }

  render() {
    const { activeTask } = this.state;

    return (
      <div className="App">
        <h1>React Задачи</h1>
        <div className="tasks">
          <div className="task-buttons">
            <button onClick={() => this.setActiveTask(1)}>Задание 1</button>
            <button onClick={() => this.setActiveTask(2)}>Задание 2</button>
            <button onClick={() => this.setActiveTask(3)}>Задание 3</button>
            <button onClick={() => this.setActiveTask(4)}>Задание 4</button>
          </div>
          <div className="task-display">
            {this.renderTask(activeTask)}
          </div>
        </div>
      </div>
    );
  }
}

export default App;