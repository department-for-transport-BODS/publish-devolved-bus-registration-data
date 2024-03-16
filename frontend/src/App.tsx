import React   from "react";
import "./App.css";
import "./Sass/App.scss";
import Home from "./pages/home";
import UploadCSVPage from "./pages/uploadcsv";
import Basic from "./pages/basic";
import DefaultPage from "./pages/default";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PartlyUploading from "./pages/uploadConfirmation";
import SuccessfullyUPloaded from "./pages/uploadConfirmationSuccessfully";
import LoginPage from "./pages/login";
import { Amplify } from "aws-amplify";
import AmplifyConfiguration from "./utils/login/AmplifyConfig";
import RequireAuth from "./utils/login/requireAuth";
import Registration from "./pages/registrations";
import viewRegistrations from "./pages/viewRegistrations";
import ErrorPage   from "./pages/errorPage";
function App() {
  Amplify.configure(AmplifyConfiguration);
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/uploadcsv"
          element={<RequireAuth component={UploadCSVPage} />}
        />
        <Route path="/basic" element={<Basic />} />
        <Route path="/default" element={<DefaultPage />} />
        <Route
          path="/partlyuploaded"
          element={<RequireAuth component={PartlyUploading} />}
        />
        <Route
          path="/successfullyuploaded"
          element={<RequireAuth component={SuccessfullyUPloaded} />}
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
      </Routes>
    </BrowserRouter>
  );
}

export default App;
