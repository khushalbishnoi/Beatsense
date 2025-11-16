# client Dockerfile (build + nginx)
FROM node:20-alpine AS build
WORKDIR /app
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}
COPY package*.json ./
RUN npm ci --silent
COPY . .
RUN npm run build

FROM nginx:stable-alpine AS runtime
LABEL maintainer="Your Name <you@example.com>"
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD wget -qO- http://localhost/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
