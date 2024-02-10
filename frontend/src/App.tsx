import React from 'react';
import logo from './logo.svg';
import './App.css';
import './Sass/App.scss';
// import CookieBanner from './components/cookie-banner';
import Home from './pages/home';
import FormExample from './pages/formexample';
import UploadCSVPage from './pages/uploadcsv';
import Basic from './pages/basic';
import DefaultPage from './pages/default';
import Form from './pages/Form';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PartlyUploading from './pages/uploadConfirmation';
import SuccessfullyUPloaded from './pages/uploadConfirmationSuccessfully';
import LoginPage from './pages/login';
// import Conrima
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


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/example" element={<FormExample />} />
        <Route path="/uploadcsv" element={<UploadCSVPage />} />
        <Route path="/basic" element={<Basic />} />
        <Route path="/default" element={<DefaultPage />} />
        <Route path="/form" element={<Form />} />
        <Route path="/partlyuploaded" element={<PartlyUploading />} />
        <Route path="/successfullyuploaded" element={<SuccessfullyUPloaded />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
