import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const alertOptions = {
    position: "middle",
    timeout: 5000,
    offset: '40px',
    transition: 'scale'
}
ReactDOM.render(
    <React.StrictMode>
            <App/>
    </React.StrictMode>,
    document.getElementById('root')
);
reportWebVitals();
