import React ,{useContext} from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import HomeScreen from '../screens/Homescreen';
import LoginScreen from '../screens/Loginsecreen';
import ServiceScreen from '../screens/ServiceConnection';
import SplashScreen from '../screens/SplashScreen';
//import AreaScreen from '../screens/Area';
import RegisterScreen from '../screens/Registersecreen';
import { AuthContext } from '../context/AuthContext.js';
import AddIdoles from '../adders/addIdoles';
import AddMessage from '../adders/addMessages';
import AddDefaultLabel from '../adders/addDefaultLabel';
import AddBoard from '../adders/addBoardToCheck';
import AddRepo from '../adders/addRepo';
import AddDefaultBoardList from '../adders/addDefaultBoardList';
import AddRepoTrello from '../adders/addRepoForTrello';
import AreaScreen from '../screens/Area';

const Stack = createNativeStackNavigator();

const Navigation = () => {
  const {userInfo, splashLoading} = useContext(AuthContext);
  return (
    <NavigationContainer>
      <Stack.Navigator>
      {splashLoading ? (
          <Stack.Screen
            name="Splash Screen"
            component={SplashScreen}
            options={{headerShown: false}}
          />
          ) : userInfo.token ? (
          <Stack.Screen 
            name="Home"
            component={HomeScreen} 
          />
          ) : (
            <>
            <Stack.Screen
              name="Login"
              component={LoginScreen}
              options={{headerShown: false}}
            />
            <Stack.Screen
              name="Register"
              component={RegisterScreen}
              options={{headerShown: false}}
            />
            <Stack.Screen 
              name="Home"
              component={HomeScreen} 
            />
            <Stack.Screen 
              name="Service Connection"
              component={ServiceScreen} 
            />
            <Stack.Screen 
              name="addIdole"
              component={AddIdoles} 
            />
            <Stack.Screen 
              name="addMessage"
              component={AddMessage} 
          />
            <Stack.Screen 
              name="addDefaultLabel"
              component={AddDefaultLabel}/>

            <Stack.Screen 
              name="addBoard"
              component={AddBoard} />
            
            <Stack.Screen 
              name="addRepo"
              component={AddRepo} />
            <Stack.Screen 
              name="addDefaultBoardList"
              component={AddDefaultBoardList} />
            <Stack.Screen 
              name="addRepoTrello"
              component={AddRepoTrello} />
            <Stack.Screen 
              name="Area"
              component={AreaScreen} 
          />
            
            </>
            
          )} 
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default Navigation;
