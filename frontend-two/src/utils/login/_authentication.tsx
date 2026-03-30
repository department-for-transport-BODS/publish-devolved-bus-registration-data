import { useAuthenticator } from '@aws-amplify/ui-react';
import { useNavigate } from 'react-router-dom';
import { useEffect,useState,useCallback } from 'react';

// Move the code inside a React function component or a custom React Hook function

const LocalAuthenticator =() => {


    const navigate = useNavigate();
    const [userSignedIn, setUserSignedIn] = useState(false);
    const { user, signOut } = useAuthenticator((context) => [context.user]);

    
    useEffect(() => {
            signOut()
            setUserSignedIn(false);
            navigate('/', {state: {isLoggedIn:userSignedIn}});
        // Your code here
    }, []);
    //     console.log("user had been changed: ", user);
    //     navigate('/');
    //     // navigate('/');
    // }, [userSignedIn]);

    // Rest of the component code...

    return (
    {userSignedIn, setUserSignedIn}
    );
};

export default LocalAuthenticator;
