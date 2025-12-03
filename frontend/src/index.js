import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Ignore benign ResizeObserver loop errors that come from React DevTools/ReactFlow
// window.addEventListener('error', (event) => {
//   if (event?.message && event.message.includes('ResizeObserver loop completed with undelivered notifications')) {
//     event.stopImmediatePropagation();
//   }
// });

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


