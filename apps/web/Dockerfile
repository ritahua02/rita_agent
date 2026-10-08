# Rita Web Dockerfile（多阶段构建，输出 Next.js standalone 产物）
#
# 构建上下文使用 apps/web 本身即可：
#   docker build -f apps/web/Dockerfile \
#     --build-arg NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com \
#     -t rita-web apps/web
#
# 运行：
#   docker run --rm -p 3000:3000 rita-web
#
# 注意：NEXT_PUBLIC_* 变量会在构建阶段被打进静态产物，
# 部署到新环境（API 域名变化）时需要重新构建镜像。

FROM node:20-slim AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund

FROM node:20-slim AS builder
WORKDIR /app
ARG NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-slim AS runner
WORKDIR /app
ENV NODE_ENV=production \
    PORT=3000

RUN useradd --create-home --uid 1000 rita

COPY --from=builder --chown=rita:rita /app/.next/standalone ./
COPY --from=builder --chown=rita:rita /app/.next/static ./.next/static

USER rita
EXPOSE 3000

CMD ["node", "server.js"]
