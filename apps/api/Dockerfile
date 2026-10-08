# Rita API Dockerfile
#
# 重要：必须使用【项目根目录】作为构建上下文（build context），而不是 apps/api，
# 因为后端在运行时会读取仓库根目录下的 data/ 目录（自我模型、长期记忆等人格数据）。
#
# 构建示例（在项目根目录执行）：
#   docker build -f apps/api/Dockerfile -t rita-api .
#
# 运行示例：
#   docker run --rm -p 8000:8000 --env-file .env rita-api

FROM python:3.11-slim AS base

# /rita 对应仓库根目录，保持 apps/api/app 的相对层级，
# 以配合 app/config.py 中基于 __file__ 向上 3 层推导 PROJECT_ROOT 的逻辑。
WORKDIR /rita

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY apps/api/requirements.txt apps/api/requirements.txt
RUN pip install --no-cache-dir -r apps/api/requirements.txt

COPY apps/api/app apps/api/app
# 人格 / 记忆数据：以只读方式打进镜像；生产环境建议改用 volume 挂载，
# 这样更新 Rita 的人格文档时无需重新构建镜像（见 docker-compose.yml）。
COPY data data

RUN useradd --create-home --uid 1000 rita \
    && chown -R rita:rita /rita
USER rita

WORKDIR /rita/apps/api
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
