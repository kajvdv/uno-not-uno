FROM node:18 AS base
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

FROM base AS build
RUN npm run build

FROM nginx:alpine AS prod
COPY --from=build /app/dist /etc/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
