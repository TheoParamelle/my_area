# pull base image
FROM node:16.0.0
RUN apt-get update && apt-get install -y curl git

# set our node environment, either development or production
# defaults to production, compose overrides this to development on build and run
ARG NODE_ENV=production
ENV NODE_ENV $NODE_ENV

# default to port 19006 for node, and 19001 and 19002 (tests) for debug
ARG PORT=19006
ENV PORT $PORT
EXPOSE $PORT 19000 19004 8080

#ENV REACT_NATIVE_PACKAGER_HOSTNAME="172.19.0.15"

# install dependencies first, in a different location for easier app bind mounting for local development
# due to default /opt permissions we have to create the dir with root and change perms
RUN mkdir opt/mobile_app
WORKDIR /opt/mobile_app
#ENV PATH /opt/react_native_app/.bin:$PATH
COPY ./mobile_app/package.json ./
RUN yarn global add expo-cli
RUN yarn add react-native-safe-area-view react-native-safe-area-context
#RUN yarn add -D metro-react-native-babel-preset
RUN yarn install
#RUN yar install -g react-native-cli
RUN yarn add react-native-webview
RUN yarn add react-native-element-dropdown
RUN yarn add react-native-dropdown-picker@5.0.0
# RUN expo login -u latets -p kymgi3-romgon-jIwtym
#RUN react-native link @react-native-community/async-storage

#RUN update metro-react-native-babel-preset
#RUN Docker network connect NETWORK
#RUN eas build:configure

# copy in our source code last, as it changes the most
#WORKDIR /opt/react_native_app/app
# for development, we bind mount volumes; comment out for production
# COPY ./react_native_app .
COPY ./mobile_app ./

ENTRYPOINT ["yarn", "start"]
#RUN expo build:android