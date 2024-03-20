import React from "react";
import "./App.css";
import "./Sass/App.scss";
import Home from "./pages/home";
import UploadCsvPage from "./pages/uploadCsv";
import Basic from "./pages/basic";
import DefaultPage from "./pages/default";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PartlyUploading from "./pages/uploadConfirmation";
import SuccessfullyUploaded from "./pages/uploadConfirmationSuccessfully";
import LoginPage from "./pages/login";
import { Amplify } from "aws-amplify";
import AmplifyConfiguration from "./utils/login/AmplifyConfig";
import RequireAuth from "./utils/login/RequireAuth";
import Registration from "./pages/registrations";
import viewRegistrations from "./pages/viewRegistrations";
import ErrorPage from "./pages/errorPage";
import ContactUs from "./pages/contactUs";
function App() {
  Amplify.configure(AmplifyConfiguration);
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/upload-csv"
          element={<RequireAuth component={UploadCsvPage} />}
        />
        <Route path="/basic" element={<Basic />} />
        <Route path="/default" element={<DefaultPage />} />
        <Route
          path="/partly-uploaded"
          element={<RequireAuth component={PartlyUploading} />}
        />
        <Route
          path="/successfully-uploaded"
          element={<RequireAuth component={SuccessfullyUploaded} />}
        />
        <Route path="/registrations"
          element={<RequireAuth component={Registration} />}
        />
        <Route 
          path="/view-registrations"
          element={<RequireAuth component={viewRegistrations} />}
        />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/error" element={<ErrorPage />} />
        <Route path="/contact-us" element={<ContactUs />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
