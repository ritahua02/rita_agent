#!/usr/bin/env bash
#
# Rita 项目一键环境构造脚本
# 作用：生成配置文件 + 构建后端虚拟环境与依赖 + 安装前端依赖
# 用法：在项目根目录执行  bash setup.sh
#
# 执行完后唯一还需手动做的事：编辑根目录 .env，填入真实的 LLM_API_KEY / LLM_MODEL。
#

set -euo pipefail

# 切到脚本所在目录（即项目根目录），保证任意位置调用都正确
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log()  { printf "\033[1;36m[setup]\033[0m %s\n" "$1"; }
warn() { printf "\033[1;33m[warn ]\033[0m %s\n" "$1"; }
err()  { printf "\033[1;31m[error]\033[0m %s\n" "$1" >&2; }

# ---------------------------------------------------------------------------
# 0. 环境检查
# ---------------------------------------------------------------------------
log "检查运行环境 ..."

if ! command -v python3 >/dev/null 2>&1; then
  err "未找到 python3，请先安装 Python 3.11+（macOS: brew install python@3.11）"
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  err "未找到 node，请先安装 Node.js 20+（macOS: brew install node@20，或用 nvm install 20）"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  err "未找到 npm，请随 Node.js 一并安装"
  exit 1
fi

PY_VER="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
NODE_VER="$(node -v)"
log "python3 = ${PY_VER} | node = ${NODE_VER}"

# 软性版本提示（不阻断）
PY_MAJOR="${PY_VER%%.*}"
PY_MINOR="${PY_VER##*.}"
if [ "${PY_MAJOR}" -lt 3 ] || { [ "${PY_MAJOR}" -eq 3 ] && [ "${PY_MINOR}" -lt 11 ]; }; then
  warn "建议 Python >= 3.11，当前 ${PY_VER}，可能出现兼容性问题"
fi

# ---------------------------------------------------------------------------
# 1. 生成配置文件（不覆盖已存在的）
# ---------------------------------------------------------------------------
log "准备配置文件 ..."

if [ -f .env ]; then
  log ".env 已存在，跳过"
elif [ -f .env.example ]; then
  cp .env.example .env
  log "已从 .env.example 生成 .env（记得填 LLM_API_KEY / LLM_MODEL）"
else
  warn "未找到 .env.example，无法生成 .env，请手动创建"
fi

if [ -f apps/web/.env.local ]; then
  log "apps/web/.env.local 已存在，跳过"
elif [ -f apps/web/.env.local.example ]; then
  cp apps/web/.env.local.example apps/web/.env.local
  log "已从模板生成 apps/web/.env.local"
else
  warn "未找到 apps/web/.env.local.example，跳过前端配置生成"
fi

# ---------------------------------------------------------------------------
# 2. 后端：虚拟环境 + 依赖
# ---------------------------------------------------------------------------
log "构建后端环境（apps/api）..."
(
  cd apps/api
  if [ ! -d .venv ]; then
    python3 -m venv .venv
    log "已创建虚拟环境 apps/api/.venv"
  else
    log "虚拟环境已存在，复用 apps/api/.venv"
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python3 -m pip install --upgrade pip >/dev/null
  pip install -r requirements.txt
  deactivate
)
log "后端依赖安装完成"

# ---------------------------------------------------------------------------
# 3. 前端：依赖
# ---------------------------------------------------------------------------
log "安装前端依赖（apps/web）..."
(
  cd apps/web
  npm install
)
log "前端依赖安装完成"

# ---------------------------------------------------------------------------
# 完成
# ---------------------------------------------------------------------------
printf "\n"
log "环境已就绪 ✅"
cat <<'EOF'

下一步：
  1) 编辑根目录 .env，填入真实的 LLM_API_KEY 和正确的 LLM_MODEL
  2) 启动后端（终端 1）：
       cd apps/api && source .venv/bin/activate && python3 -m uvicorn app.main:app --reload --port 8000
  3) 启动前端（终端 2）：
       cd apps/web && npm run dev
  4) 打开 http://localhost:3000

提示：每次修改根目录 .env 后都要重启后端才会生效。
EOF
