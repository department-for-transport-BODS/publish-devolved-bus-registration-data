
    import React, { useState, useEffect } from "react";
    import { useLocation, useNavigate } from "react-router-dom";
    import axios from "axios";
    import { AxiosError } from "axios";
    import { FullColumnLayout } from "../Layout/Layout";
    import Footer from "../Layout/Footer";
    import SuccessfullyUpdated from '../components/SuccessfullyUpdated';

    const Uploading: React.FC = () => {
      const location = useLocation();
      const navigate = useNavigate();
      const [data, setData] = useState<any>(null);
      const [isLoading, setIsLoading] = useState<boolean>(true);
      const formData = new FormData();
      console.log({location})
      const submitData = async (formData: FormData) => {
        try {
          const response = await axios.post(
            "http://localhost:8000/uploadfile",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          );
          console.log("Upload successful:", response?.data);
          navigate("/successfullyuploaded", { state: response?.data });
          
        } catch (error) {
          const nowData = {
            message: (error as AxiosError).message,
            code: (error as AxiosError).code,
            data: (error as AxiosError).response?.data,
          };
          console.log(nowData);
          setData(nowData);
          navigate("/partlyuploaded", { state: nowData.data });
        } finally {
          setIsLoading(false);
        }
      };

      useEffect(() => {
        if (location.state?.form !== undefined) {
          console.log(location.state.form);
          formData.append("file", location.state.form);
          submitData(formData);
        }
      }, [location.state.form]);

      useEffect(() => {
        const requestOrigin = window.location.origin;
        console.log("Request origin:", requestOrigin);
      }, []);

      return (
        <>
          <FullColumnLayout title="Temp Page" description="Temp Page" hideCookieBanner={true}>
            {isLoading ? (
              <h1>Uploading...</h1>
            ) : (
              <SuccessfullyUpdated />
            )}
          </FullColumnLayout>
          <Footer />
        </>
      );
    };

    export default Uploading;
 