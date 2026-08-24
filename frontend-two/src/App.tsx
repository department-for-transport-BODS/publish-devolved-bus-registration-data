"use client";

import React from "react";
import Home from "./views/home";
import UploadCsvPage from "./views/uploadCsv";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PartlyUploading from "./views/uploadConfirmation";
import SuccessfullyUploaded from "./views/uploadConfirmationSuccessfully";
import LoginPage from "./views/login";
import { Amplify } from "aws-amplify";
import AmplifyConfiguration from "./utils/login/AmplifyConfig";
import RequireAuth from "./utils/login/RequireAuth";
import Registration from "./views/registrations";
import ViewRegistrations from "./views/viewRegistrations";
import ErrorPage from "./views/errorPage";
import ContactUs from "./views/contactUs";
import PrivacyStatement from "./views/privacyStatement";
import AccessibilityStatement from "./views/accessibilityStatement";
import CookiePage from "./views/cookiePage";
import PreValidations from "./views/preValidation";
import FindRegisteredServices from "./views/findRegisteredServices";
import RegistrationDetails from "./views/registrationDetails";
import HomeOptions from "./views/homeOptions";

Amplify.configure(AmplifyConfiguration);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/home-options' element={<HomeOptions />} />
        <Route
          path="/upload-csv"
          element={<RequireAuth component={UploadCsvPage} requiredAccess="operator"/>}
        />
        <Route
          path="/partly-uploaded"
          element={<RequireAuth component={PartlyUploading} requiredAccess="operator"/>}
        />
        <Route
          path="/successfully-uploaded"
          element={<RequireAuth component={SuccessfullyUploaded} requiredAccess="operator"/>}
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
          element={<AccessibilityStatement />} />
        <Route path="/cookie-page" element={<CookiePage />} />
        <Route path="/find-registered-services" element={<FindRegisteredServices />} />
        <Route path="/registration-details" element={<RequireAuth component={RegistrationDetails} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
