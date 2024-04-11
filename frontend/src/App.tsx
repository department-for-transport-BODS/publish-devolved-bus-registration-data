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
import ViewRegistrations from "./pages/viewRegistrations";
import ErrorPage from "./pages/errorPage";
import ContactUs from "./pages/contactUs";
import PrivacyStatement from "./pages/privacyStatement";
import AccessibilityStatment from "./pages/accessibilityStatement";
import CookiePage from "./pages/cookiePage";
import PreValidations from "./pages/preValidation";
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
        <Route path="/pre-validation" element={
          <RequireAuth component={PreValidations} />
        } />
        <Route 
          path="/view-registrations"
          element={<RequireAuth component={ViewRegistrations} />}
        />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/error" element={<ErrorPage />} />
        <Route path="/contact-us" element={<ContactUs />} />
        <Route path="/privacy-statement" element={<PrivacyStatement />} />
        <Route
          path="/accessibility-statement"
          element={<AccessibilityStatment />} />
        <Route path="/cookie-page" element={<CookiePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
