import React from "react";
import Footer from "../Layout/Footer";
import FullColumnLayout from "../Layout/Layout";
import UploadCsv from "../components/UploadCsv";
import DataProccessingWaiting  from "../components/DataProccessingWaiting";
type Props = {
  isLoggedIn?: boolean;
};

const UploadCsvPage: React.FC<Props> = ({isLoggedIn=false}) => {
const [isloading, setIsLoading] = React.useState<boolean>(false);

  return (
    <>
      <FullColumnLayout
        title="Upload CSV"
        description="Temp Page"
        hideCookieBanner={true}
        isLoggedIn={isLoggedIn}
      >
         {isloading && <DataProccessingWaiting />}
        {!isloading && <UploadCsv setIsLoading={setIsLoading} />}
      </FullColumnLayout>
      <Footer />
    </>
  );
};

export default UploadCsvPage;
