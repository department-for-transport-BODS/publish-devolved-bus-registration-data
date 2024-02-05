import React from 'react';
import logo from './logo.svg';
import './App.css';
import './Sass/App.scss';
// import CookieBanner from './components/cookie-banner';
import Home from './pages/home';
import UploadCSV from './pages/upload';
import FormExample from './pages/formexample';
import TempPage from './pages/temp';
import Basic from './pages/basic';
import DefaultPage from './pages/default';
import Form from './pages/Form';
// import { Button } from 'govuk-react'
// import React from 'react';
// import { Button } from 'govuk-react';

// interface MyComponentProps {
//   title: string;
// }

// const MyComponent: React.FC<MyComponentProps> = ({ title }: MyComponentProps) => (
//   <div>
//     <h1>{title}</h1>
//     <Button />
//   </div>
// );

import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/uploadcsv" element={<UploadCSV />} />
        <Route path="/example" element={<FormExample />} />
        <Route path="/temp" element={<TempPage />} />
        <Route path="/basic" element={<Basic />} />
        <Route path="/default" element={<DefaultPage />} />
        <Route path="/form" element={<Form />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
