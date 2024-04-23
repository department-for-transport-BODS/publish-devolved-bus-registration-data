import { fetchAuthSession } from "aws-amplify/auth";
import Cookies from "universal-cookie";

const SetAccessType = () => {
const cookies = new Cookies();
fetchAuthSession().then((session) => {
         const groups: any = session?.tokens?.accessToken?.payload?.["cognito:groups"] ?? [];
         const accessType = cookies.get("access-type")?? undefined
         if (!accessType) {
         groups.map((group: string) => {
           if (group.includes("read-only")){
             cookies.set("access-type", "read-only");
           }
           if (group.includes("users-group")) {
             cookies.set("access-type", "operator");
           }
         });
      
          }
       });
}

export default SetAccessType;
