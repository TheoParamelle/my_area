import React, { createContext, useState,useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import client from '../config'
import { generateBackgroundStyle } from 'react-native-user-avatar/lib/module/helpers';
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [userInfo, setUserInfo] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [splashLoading, setSplashLoading] = useState(false);
  const [error, setError] = useState('');
  const [service, setService] = useState('')

  const  register= async(username, password, navigation)=>{
    try {
      const {data} =  await client.post(
        '/login',
        {
          username,
          password,
        },
        {
            headers: {
            'Content-Type': "application/json",
            'Accept': "application/json",
            },  
            body:JSON.stringify({"username": username, "password": password, "newAccount":true})   
        }
     );
    console.log(data);  
        
      if (data.username == false) {
        navigation.replace('Login');
      }else{
        data.message = "Erreur compte déjà existant"
        alert(data.message);
        setIsLoading(false);
      }
    } catch (e) {
      console.log(e);
        console.log(`register error ${e}`);
        setIsLoading(false);
    }
  }
  

  const login= async(username, password, navigation)=>{
    try {
      const {data} =  await client.post(
        '/login',
        {
          username,
          password,
        },
        {
            headers: {
            'Content-Type': "application/json",
            'Accept': "application/json",
            },  
            body:JSON.stringify({"username": username, "password": password, "newAccount":true})   
        }
     );
    console.log(data);  
        
      if (data.username == true && data.password == true) {
        navigation.replace('Home');
      }else{
        data.message = "Compte non connu"
        alert(data.message);
        setIsLoading(false);
      }
    } catch (e) {
      console.log(e);
        console.log(`Login error ${e}`);
        setIsLoading(false);
    }
  }

  const logout = () => {
    setIsLoading(true);
    client.post(
      '/logout',
      {},
      
    {      headers: {
            headers: {Authorization: `Bearer ${userInfo.token}`}  ,
      } }  
   ).then(res => {
    console.log(res.data);
    AsyncStorage.removeItem('userInfo');
    setUserInfo({});
    setIsLoading(false);
    setError(null)
  })
  .catch(e => {
    console.log(`logout error ${e}`);
    setIsLoading(false);
  });      
  };

  const isLoggedIn = async () => {
    try {
      setSplashLoading(true);

      let userInfo = await AsyncStorage.getItem('userInfo');
      userInfo = JSON.parse(userInfo);

      if (userInfo) {
        setUserInfo(userInfo);
      }

      setSplashLoading(false);
    } catch (e) {
      setSplashLoading(false);
      console.log(`is logged in error ${e}`);
    }
  };

  const sendToBack = async(dict, route) => {
    try{
      const {data} = await client.post(route,
      dict
      )
      console.log(data)
    }
    catch(e) {
        console.log(e)
      }
  }

  const sendArea = async(intitialAreas) => {
    try {
      const {data} =  await client.post(
        '/addArea',
        {"action": intitialAreas.action, "reaction": intitialAreas.reaction})
    console.log(data);
    } catch (e) {
      console.log(e);
        console.log("Reaction error ${e}");
        setIsLoading(false);
    }
  }


  useEffect(() => {
    isLoggedIn();
  }, []);
  return (
    <AuthContext.Provider
    value={{
      isLoading,
      userInfo,
      splashLoading,
      error,
      register,
      login,
      logout,
      service,
      setService,
      sendArea,
      sendToBack
    }}>
    {children}
  </AuthContext.Provider>
  );
};
